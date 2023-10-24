# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1

from chaosgcp import load_credentials

__all__ = [
    "get_network_endpoint_group",
    "list_network_endpoint_groups",
]


def get_network_endpoint_group(
    network_endpoint_group: str,
    zone: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get a single network endpoint group.
    """
    credentials = load_credentials(secrets)
    project = credentials.project_id

    client = compute_v1.NetworkEndpointGroupsClient()

    request = compute_v1.GetNetworkEndpointGroupRequest(
        network_endpoint_group=network_endpoint_group,
        project=project,
        zone=zone,
    )

    response = client.get(request=request)

    return response.__class__.to_dict(response)


def list_network_endpoint_groups(
    zone: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List all network endpoint groups in the zone.
    """
    credentials = load_credentials(secrets)
    project = credentials.project_id

    client = compute_v1.NetworkEndpointGroupsClient()

    request = compute_v1.ListNetworkEndpointGroupsRequest(
        project=project,
        zone=zone,
    )

    response = client.list(request=request)

    return response.__class__.to_dict(response)
