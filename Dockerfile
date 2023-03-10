ARG branch=latest
FROM cccs/assemblyline-v4-service-base:$branch

ENV SERVICE_PATH ancestry.ancestry.Ancestry

USER root

# Switch to assemblyline user
USER assemblyline

# Copy service code
WORKDIR /opt/al_service
COPY . .

# Patch version in manifest
ARG version=4.3.0.dev0
USER root
RUN sed -i -e "s/\$SERVICE_TAG/$version/g" service_manifest.yml

# Switch to assemblyline user
USER assemblyline
