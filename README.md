[![Discord](https://img.shields.io/badge/chat-on%20discord-7289da.svg?sanitize=true)](https://discord.gg/GUAy9wErNu)
[![](https://img.shields.io/discord/908084610158714900)](https://discord.gg/GUAy9wErNu)
[![Static Badge](https://img.shields.io/badge/github-assemblyline-blue?logo=github)](https://github.com/CybercentreCanada/assemblyline)
[![Static Badge](https://img.shields.io/badge/github-assemblyline_service_ancestry-blue?logo=github)](https://github.com/CybercentreCanada/assemblyline-service-ancestry)
[![GitHub Issues or Pull Requests by label](https://img.shields.io/github/issues/CybercentreCanada/assemblyline/service-ancestry)](https://github.com/CybercentreCanada/assemblyline/issues?q=is:issue+is:open+label:service-ancestry)
[![License](https://img.shields.io/github/license/CybercentreCanada/assemblyline-service-ancestry)](./LICENSE)

# Ancestry Service (BETA)

Signature-based Assemblyline service that focuses on file genealogy.

## Service Details

### Signatures

(BETA) Signatures are defined as service configuration and each signature follows the following format:

```yaml
config:
  signatures:
    exe_from_office_document: # Signature name
      pattern: "document/office/.+,ROOT\\|executable/windows/(?:pe|dll)(?:32|64),EXTRACTED" # Regex pattern
      score: 1000 # Score associated to signature hit
```

Depending on the capabilities we want this service to have, this will be prone change when ready for production.

#### What do signatures run on?

The signatures run on temporary information that the Assemblyline Dispatcher passes to the service. As such, for the time being, we've decided to format the data as pairs that include the filetype and it's relation to the parent file, if any, joined by `|`.

For example: A OneNote file that has an embedded PE with a RSA certificate will look like:
`document/office/onenote,ROOT|executable/windows/pe64,EXTRACTED|certificate/rsa,EXTRACTED`

## Image variants and tags

Assemblyline services are built from the [Assemblyline service base image](https://hub.docker.com/r/cccs/assemblyline-v4-service-base),
which is based on Debian 11 with Python 3.11.

Assemblyline services use the following tag definitions:

| **Tag Type** | **Description**                                                                                  |      **Example Tag**       |
| :----------: | :----------------------------------------------------------------------------------------------- | :------------------------: |
|    latest    | The most recent build (can be unstable).                                                         |          `latest`          |
|  build_type  | The type of build used. `dev` is the latest unstable build. `stable` is the latest stable build. |     `stable` or `dev`      |
|    series    | Complete build details, including version and build type: `version.buildType`.                   | `4.5.stable`, `4.5.1.dev3` |

## Running this service

This is an Assemblyline service. It is designed to run as part of the Assemblyline framework.

If you would like to test this service locally, you can run the Docker image directly from the a shell:

    docker run \
        --name Ancestry \
        --env SERVICE_API_HOST=http://`ip addr show docker0 | grep "inet " | awk '{print $2}' | cut -f1 -d"/"`:5003 \
        --network=host \
        cccs/assemblyline-service-ancestry

To add this service to your Assemblyline deployment, follow this
[guide](https://cybercentrecanada.github.io/assemblyline4_docs/developer_manual/services/run_your_service/#add-the-container-to-your-deployment).

## Documentation

General Assemblyline documentation can be found at: https://cybercentrecanada.github.io/assemblyline4_docs/

# Service Ancestry (BETA)

Service d'Assemblyline axé sur la généalogie des fichiers basée sur les signatures.

## Détails du service

### Signatures

(BETA) Les signatures sont définies en tant que configuration de service et chaque signature suit le format suivant:

```yaml
config:
  signatures:
    exe_from_office_document: # Nom de la signature
      pattern: "document/office/.+,ROOT\|executable/windows/(?:pe|dll)(?:32|64),EXTRACTED" # Motif Regex
      score: 1000 # Score associé à la signature hit
```

En fonction des capacités que nous voulons donner à ce service, ceci sera susceptible d'être modifié lorsqu'il sera prêt pour la production.

#### Sur quoi les signatures s'exécutent-elles ?

Les signatures sont exécutées sur les informations temporaires que le dispatcher d'Assemblyline transmet au service. Pour l'instant, nous avons décidé de formater les données sous forme de paires comprenant le type de fichier et sa relation avec le fichier parent, s'il y en a un, joint par `|`.

Par exemple : Un fichier OneNote contenant un PE avec un certificat RSA ressemblera à ceci :
`document/office/onenote,ROOT|executable/windows/pe64,EXTRACTED|certificate/rsa,EXTRACTED`

## Variantes et étiquettes d'image

Les services d'Assemblyline sont construits à partir de l'image de base [Assemblyline service](https://hub.docker.com/r/cccs/assemblyline-v4-service-base),
qui est basée sur Debian 11 avec Python 3.11.

Les services d'Assemblyline utilisent les définitions d'étiquettes suivantes:

| **Type d'étiquette** | **Description**                                                                                                |  **Exemple d'étiquette**   |
| :------------------: | :------------------------------------------------------------------------------------------------------------- | :------------------------: |
|   dernière version   | La version la plus récente (peut être instable).                                                               |          `latest`          |
|      build_type      | Type de construction utilisé. `dev` est la dernière version instable. `stable` est la dernière version stable. |     `stable` ou `dev`      |
|        série         | Détails de construction complets, comprenant la version et le type de build: `version.buildType`.              | `4.5.stable`, `4.5.1.dev3` |

## Exécution de ce service

Il s'agit d'un service d'Assemblyline. Il est optimisé pour fonctionner dans le cadre d'un déploiement d'Assemblyline.

Si vous souhaitez tester ce service localement, vous pouvez exécuter l'image Docker directement à partir d'un terminal:

    docker run \
        --name Ancestry \
        --env SERVICE_API_HOST=http://`ip addr show docker0 | grep "inet " | awk '{print $2}' | cut -f1 -d"/"`:5003 \
        --network=host \
        cccs/assemblyline-service-ancestry

Pour ajouter ce service à votre déploiement d'Assemblyline, suivez ceci
[guide](https://cybercentrecanada.github.io/assemblyline4_docs/fr/developer_manual/services/run_your_service/#add-the-container-to-your-deployment).

## Documentation

La documentation générale sur Assemblyline peut être consultée à l'adresse suivante: https://cybercentrecanada.github.io/assemblyline4_docs/
