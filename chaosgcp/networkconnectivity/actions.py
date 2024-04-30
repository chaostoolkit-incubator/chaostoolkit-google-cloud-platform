# Copyright 2024 Google LLC.
# SPDX-License-Identifier: Apache-2.0
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from google.cloud import networkconnectivity_v1

__all__ = [
    "create_policy_based_route", "delete_policy_based_route"
]

def delete_policy_based_route(
        name_value: str,
)-> Dict[str, Any]:
    """ Delete a policy based route
    Please refer to this: https://t.ly/VnEPU

    :param name_value: the name of the route,
    :return JSON Response which is in form of dictionary
    """

    # Create a client
    client = networkconnectivity_v1.PolicyBasedRoutingServiceClient()

    # Initialize request argument(s)
    request = networkconnectivity_v1.DeletePolicyBasedRouteRequest(
        name=name_value,
    )

    # Make the request
    response = client.delete_policy_based_route(request=request)

    return response.__class__.to_dict(response)


def create_policy_based_route(
    parent_value: str,
    name: str,
    next_hop_ilb_ip: str,
    network: str,
    src_range: str,
    dest_range: str,
    priority: int,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """ Create a policy based route
    Please refer to this: https://t.ly/soPz7

    :param parent_value: for example: "projects/${var.project_id}/locations/global",
    :param name: the name of the route,
    :param next_hop_ilb_ip: IP of the next hop internal load balancer,
    :param network: GCP network name,
    :param src_range: Source CIDR range,
    :param dest_range: Desination CIDR range,
    :param priority: the piority of the route,
    :return JSON Response which is in form of dictionary
    """

    # Create a client
    client = networkconnectivity_v1.PolicyBasedRoutingServiceClient()

    # Initialize request argument(s)
    policy_based_route = networkconnectivity_v1.PolicyBasedRoute()
    policy_based_route.next_hop_ilb_ip = next_hop_ilb_ip
    policy_based_route.network = network
    policy_based_route.name= name
    policy_based_route.priority = priority
    policy_based_route.filter.protocol_version = "IPV4"
    policy_based_route.filter.src_range = src_range
    policy_based_route.filter.dest_range = dest_range

    request = networkconnectivity_v1.CreatePolicyBasedRouteRequest(
        parent = parent_value,
        policy_based_route_id= name,
        policy_based_route=policy_based_route,
    )

    # Make the request
    response = client.create_policy_based_route(request=request)

    return response.__class__.to_dict(response)
