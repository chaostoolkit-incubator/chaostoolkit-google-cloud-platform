# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1

from chaosgcp import get_context, load_credentials

__all__ = [
    "get_network_endpoint_group",
    "list_network_endpoint_groups",
]


def get_network_endpoint_group(
    network_endpoint_group: str,
    zone: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get a single network endpoint group.
    """
    ctx = get_context(
        configuration=configuration, project_id=project_id, region=region
    )
    credentials = load_credentials(secrets)

    client = compute_v1.NetworkEndpointGroupsClient(credentials=credentials)
    credentials = client.transport._credentials
    project = ctx.project_id or credentials.project_id

    request = compute_v1.GetNetworkEndpointGroupRequest(
        network_endpoint_group=network_endpoint_group,
        project=project,
        zone=zone,
    )

    response = client.get(request=request)

    return response.__class__.to_dict(response)


def list_network_endpoint_groups(
    zone: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List all network endpoint groups in the zone.
    """
    ctx = get_context(
        configuration=configuration, project_id=project_id, region=region
    )
    credentials = load_credentials(secrets)

    client = compute_v1.NetworkEndpointGroupsClient(credentials=credentials)
    credentials = client.transport._credentials
    project = ctx.project_id or credentials.project_id

    request = compute_v1.ListNetworkEndpointGroupsRequest(
        project=project,
        zone=zone,
    )

    response = client.list(request=request)

    return response.__class__.to_dict(response)
