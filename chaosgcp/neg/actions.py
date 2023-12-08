# -*- coding: utf-8 -*-
from typing import Dict, List, Optional

from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1

from chaosgcp import get_context, load_credentials, wait_on_extended_operation

__all__ = [
    "detach_network_endpoint_group",
    "attach_network_endpoint_group",
]


def detach_network_endpoint_group(
    network_endpoint_group: str,
    zone: str,
    endpoints: Optional[List[Dict[str, str]]] = None,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """
    Detach a list of network endpoints from the specified network endpoint
    group.

    See https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.types.NetworkEndpoint
    for the content of each network endpoint.
    """  # noqa E501
    ctx = get_context(
        configuration=configuration, project_id=project_id, region=region
    )
    credentials = load_credentials(secrets)

    client = compute_v1.NetworkEndpointGroupsClient(credentials=credentials)
    credentials = client.transport._credentials
    project = ctx.project_id or credentials.project_id

    params = dict(
        network_endpoint_group=network_endpoint_group,
        project=project,
        zone=zone,
    )

    if endpoints:
        params[
            "network_endpoint_groups_detach_endpoints_request_resource"
        ] = compute_v1.NetworkEndpointGroupsDetachEndpointsRequest(
            network_endpoints=[
                compute_v1.NetworkEndpoint(**e) for e in endpoints
            ]
        )

    request = compute_v1.DetachNetworkEndpointsNetworkEndpointGroupRequest(
        **params
    )

    operation = client.detach_network_endpoints(request=request)
    wait_on_extended_operation(operation=operation)


def attach_network_endpoint_group(
    network_endpoint_group: str,
    zone: str,
    endpoints: Optional[List[Dict[str, str]]] = None,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """
    Attach a list of network endpoints to the specified network endpoint
    group.

    See https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.types.NetworkEndpoint
    for the content of each network endpoint.
    """  # noqa E501
    ctx = get_context(
        configuration=configuration, project_id=project_id, region=region
    )
    credentials = load_credentials(secrets)

    client = compute_v1.NetworkEndpointGroupsClient(credentials=credentials)
    credentials = client.transport._credentials
    project = ctx.project_id or credentials.project_id

    params = dict(
        network_endpoint_group=network_endpoint_group,
        project=project,
        zone=zone,
    )

    if endpoints:
        params[
            "network_endpoint_groups_detach_endpoints_request_resource"
        ] = compute_v1.NetworkEndpointGroupsAttachEndpointsRequest(
            network_endpoints=[
                compute_v1.NetworkEndpoint(**e) for e in endpoints
            ]
        )

    request = compute_v1.AttachNetworkEndpointsNetworkEndpointGroupRequest(
        **params
    )

    operation = client.attach_network_endpoints(request=request)
    wait_on_extended_operation(operation=operation)
