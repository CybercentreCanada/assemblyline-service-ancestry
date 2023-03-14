from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.request import ServiceRequest
from assemblyline_v4_service.common.result import Heuristic, Result, ResultTimelineSection
from assemblyline.common.uid import get_id_from_data, SHORT


from ancestry.icon_map import AL_TYPE_ICON

import re
from typing import Dict, List


class AncestrySignature:
    def __init__(self, name, pattern, score=0) -> None:
        self.name = name
        self.pattern = pattern
        self.score = score

    def __str__(self) -> str:
        return f"{self.name}({self.score})"


class AncestryNode(object):
    def __init__(self, type=None, parent_relation=None, *args, **kwargs):
        self.file_type = type
        self.parent_relation = parent_relation
        self.score = 0
        self.signatures: List[AncestrySignature] = []

    def add_signature(self, signature: AncestrySignature):
        self.score += signature.score
        self.signatures.append(signature.name)

    def __str__(self):
        return f"{self.file_type},{self.parent_relation}"

    def to_timeline_node(self) -> Dict:
        icon, content = None, None

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

        return {
            'title': self.parent_relation,
            'content': content,
            'opposite_content': self.file_type,
            'icon': icon,
            'signatures': self.signatures,
            'score': self.score
        }


class Ancestry(ServiceBase):
    def __init__(self, config) -> None:
        super().__init__(config)

    def execute(self, request: ServiceRequest) -> None:
        result = Result()

        def add_to_section(result: Result, ancestry: list):
            chain = [AncestryNode(**ancester) for ancester in ancestry]
            tag = '|'.join([str(node)for node in chain])
            # Workaround for caching issue
            request.set_service_context(f"Ancestry: {get_id_from_data(tag, length=SHORT)}")

            title = ' → '.join([c.file_type.split('/')[-1].upper() for c in chain])
            timeline_result_section = ResultTimelineSection(title_text=title, tags={'file.ancestry': [tag]})

            # Iterate over detection signatures and start scoring ancestry nodes
            heur = None
            for sig_name, sig_details in self.config.get('signatures', {}).items():
                signature = AncestrySignature(name=sig_name, **sig_details)
                for match in re.finditer(signature.pattern, tag):
                    self.log.debug(f'MATCH: {signature} on {tag}')
                    match_group = match.group()
                    matched_group = tag.replace(match_group, f"**{match_group}**")

                    if not heur and match_group == tag:
                        heur = Heuristic(1)
                        # timeline_result_section.add_tag('file.rule.ancestry', signature.name)

                    if heur:
                        heur.add_signature_id(signature=signature.name, score=signature.score)

                    score_node = False
                    for i, node in enumerate(matched_group.split('|')):

                        # Use double asterisk as an on/off switch for scoring subgroups of chain
                        if node.startswith("**"):
                            score_node = True

                        if score_node:
                            chain[i].add_signature(signature)

                        if node.endswith("**"):
                            score_node = False

            [timeline_result_section.add_node(**c.to_timeline_node()) for c in chain]
            timeline_result_section.set_heuristic(heur)
            result.add_section(timeline_result_section)

        if request.task.depth > 0:
            for ancestry in request.task.temp_submission_data['ancestry']:
                add_to_section(result, ancestry)

        request.result = result
