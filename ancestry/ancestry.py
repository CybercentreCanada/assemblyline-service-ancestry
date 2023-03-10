from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.request import ServiceRequest
from assemblyline_v4_service.common.result import Result, ResultSection, ResultTimelineSection

from ancestry.icon_map import AL_TYPE_ICON

import re
from typing import Dict

SCORE_COLOR_MAP = {
    'green': (-10000, 0),
    None: (0, 300),  # Don't alter default coloring
    'yellow': (300, 700),
    'orange': (700, 1000),
    'red': (1000, 10000),
}


class AncestryNode(object):
    def __init__(self, type=None, parent_relation=None, *args, **kwargs):
        self.file_type = type
        self.parent_relation = parent_relation
        self.score = 0
        self.signatures = []

    def add_signature(self, name: str, score: int):
        self.score += score
        self.signatures.append((name, score))

    def __str__(self):
        return f"{self.file_type},{self.parent_relation}"

    def to_timeline_node(self) -> Dict:
        icon, content, color = None, None, 'white'

        # Detemine content
        if self.parent_relation == "EXTRACTED":
            content = "from parent file"
        elif self.parent_relation == "DOWNLOADED":
            content = "from url: {insert_url}"

        # Detemine icon
        for pattern, icon in AL_TYPE_ICON.items():
            if re.match(pattern, self.file_type):
                icon = icon
                break

        # Detemine color of icon
        for score_color, score_range in SCORE_COLOR_MAP.items():
            if score_range[0] <= self.score < score_range[1]:
                color = score_color
                break

        return {
            'title': self.parent_relation,
            'content': content,
            'opposite_content': self.file_type,
            'icon': icon,
            'signatures': [sig for sig, _ in self.signatures],
            'color': color
        }


class Ancestry(ServiceBase):
    def __init__(self, config) -> None:
        super().__init__(config)

    def execute(self, request: ServiceRequest) -> None:
        result = Result()
        section = ResultSection("Genealogy")

        def add_to_section(section: ResultSection, ancestry: list):
            chain = [AncestryNode(**ancester) for ancester in ancestry]
            tag = '|'.join([str(node)for node in chain])

            timeline_result_section = ResultTimelineSection(tag.replace('|', ' → '), tags={'file.ancestry': [tag]})

            # Iterate over detection signatures and start scoring ancestry nodes

            for signature, score in self.config.get('signatures').items():
                for match in re.finditer(signature, tag):
                    match_group = match.group()
                    matched_group = tag.replace(match_group, f"**{match_group}**")
                    score_node = False
                    for i, node in enumerate(matched_group.split('|')):

                        # Use double asterisk as an on/off switch for scoring subgroups of chain
                        if node.startswith("**"):
                            score_node = True

                        if score_node:
                            chain[i].add_signature(signature, int(score))

                        if node.endswith("**"):
                            score_node = False
                    timeline_result_section.add_tag('file.rule.ancestry', signature)

            [timeline_result_section.add_node(**c.to_timeline_node()) for c in chain]

            section.add_subsection(timeline_result_section)

        for ancestry in request.task.temp_submission_data['ancestry']:
            add_to_section(section, ancestry)
        result.add_section(section)
        self.log.info(request.task.temp_submission_data['ancestry'])

        request.result = result
