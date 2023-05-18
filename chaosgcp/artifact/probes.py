from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from google.cloud import artifactregistry_v1
from google.cloud.devtools import containeranalysis_v1
from grafeas.grafeas_v1 import Severity

from chaosgcp import get_context, load_credentials

__all__ = [
    "list_docker_image_tags",
    "get_most_recent_docker_image",
    "get_docker_image_version_from_tag",
    "get_container_most_recent_image_vulnerabilities_occurences",
    "list_severe_or_critical_vulnerabilities_in_most_recent_image",
    "has_most_recent_image_any_severe_or_critical_vulnerabilities",
]


def list_docker_image_tags(
    repository: str,
    package_name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List docker image tags of a package in the given repository.
    """
    context = get_context(configuration, secrets)
    client = artifactregistry_v1.ArtifactRegistryClient()

    parent = f"projects/{context.project_id}/locations/{context.region}/repositories/{repository}/packages/{package_name}"  # noqa

    request = artifactregistry_v1.ListTagsRequest(
        parent=parent,
    )

    response = client.list_tags(request=request)

    return list(
        map(
            lambda p: p.__class__.to_dict(p),
            response,
        )
    )


def get_most_recent_docker_image(
    repository: str,
    package_name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get most recent tag for a package in repository.
    """
    context = get_context(configuration, secrets)
    client = artifactregistry_v1.ArtifactRegistryClient()

    parent = f"projects/{context.project_id}/locations/{context.region}/repositories/{repository}/packages/{package_name}"  # noqa

    request = artifactregistry_v1.ListTagsRequest(
        parent=parent,
    )

    response = client.list_tags(request=request)
    *_, last = response  # python is nice
    return last.__class__.to_dict(last)


def get_docker_image_version_from_tag(
    repository: str,
    package_name: str,
    tag: str = "latest",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get image version (sha256) for most recent tag.
    """
    context = get_context(configuration, secrets)
    client = artifactregistry_v1.ArtifactRegistryClient()

    name = f"projects/{context.project_id}/locations/{context.region}/repositories/{repository}/packages/{package_name}/tags/{tag}"  # noqa

    request = artifactregistry_v1.GetTagRequest(name=name)

    response = client.get_tag(request=request)
    return response.__class__.to_dict(response)


def get_container_most_recent_image_vulnerabilities_occurences(
    repository: str,
    package_name: str,
    kind: str = "VULNERABILITY",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    List all occurrences for a given container image tag.
    """
    context = get_context(configuration, secrets)
    image = get_most_recent_docker_image(
        repository, package_name, configuration, secrets
    )
    _, version = image["version"].rsplit(":", 1)

    url = f"https://{context.region}-docker.pkg.dev/{context.project_id}/{repository}/{package_name}@sha256:{version}"  # noqa

    creds = load_credentials(secrets=secrets)
    client = containeranalysis_v1.ContainerAnalysisClient(credentials=creds)
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{context.project_id}"
    response = grafeas_client.list_occurrences(
        parent=project_name, filter=f'kind="{kind}" AND resourceUrl="{url}"'
    )

    return list(
        map(
            lambda p: p.__class__.to_dict(p),
            response,
        )
    )


def list_severe_or_critical_vulnerabilities_in_most_recent_image(
    repository: str,
    package_name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List all severe and critical vulnerabilities for the most recent tag.
    """
    vulnerabilities = (
        get_container_most_recent_image_vulnerabilities_occurences(  # noqa
            repository=repository,
            package_name=package_name,
            kind="VULNERABILITY",
            configuration=configuration,
            secrets=secrets,
        )
    )

    results = []
    for v in vulnerabilities:
        severity = v["vulnerability"]["effective_severity"]
        if severity in [Severity.HIGH, Severity.CRITICAL]:
            results.append(v)
    return results


def has_most_recent_image_any_severe_or_critical_vulnerabilities(
    repository: str,
    package_name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Has the most recent tag any severe or critical vulnerabilities.
    """
    return (
        len(
            list_severe_or_critical_vulnerabilities_in_most_recent_image(
                repository=repository,
                package_name=package_name,
                configuration=configuration,
                secrets=secrets,
            )
        )
        > 0
    )
