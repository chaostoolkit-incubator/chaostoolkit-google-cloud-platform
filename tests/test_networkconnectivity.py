# Copyright 2024 Google LLC.
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, patch
from google.cloud import networkconnectivity_v1
from chaosgcp.networkconnectivity.actions import create_policy_based_route, delete_policy_based_route

@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.PolicyBasedRoutingServiceClient", autospec=True)
@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.CreatePolicyBasedRouteRequest", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_create_policy_based_route(Credentials, create_request, client):
    # Test create_policy_based_route
    parent_value = "projects/test-project/locations/global"
    name = "test-route"
    next_hop_ilb_ip = "10.0.0.1"
    network = "test-network"
    src_range = "192.168.1.0/24"
    dest_range = "10.0.0.0/24"
    priority = 100

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()

    # Call the function
    create_policy_based_route(
        parent_value, name, next_hop_ilb_ip, network, src_range, dest_range, priority
    )

    # Assert that the PolicyBasedRoutingServiceClient was initialized
    client.assert_called_once()

    # Initialize request argument(s)
    policy_based_route = networkconnectivity_v1.PolicyBasedRoute()
    policy_based_route.next_hop_ilb_ip = next_hop_ilb_ip
    policy_based_route.network = network
    policy_based_route.name= name
    policy_based_route.priority = priority
    policy_based_route.filter.protocol_version = "IPV4"
    policy_based_route.filter.src_range = src_range
    policy_based_route.filter.dest_range = dest_range

    # Assert that the CreatePolicyBasedRouteRequest was initialized with the correct arguments
    create_request.assert_called_once_with(
        parent = parent_value,
        policy_based_route_id= name,
        policy_based_route=policy_based_route,
    )

@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.PolicyBasedRoutingServiceClient", autospec=True)
@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.DeletePolicyBasedRouteRequest", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_delete_policy_based_route(Credentials, delete_request, client):
    # Test delete_policy_based_route
    name_value = "test-route"

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()

    # Call the function
    delete_policy_based_route(name_value)

    # Assert that the DeletePolicyBasedRouteRequest was initialized with the correct arguments
    delete_request.assert_called_once_with(name=name_value)

    # Assert that the delete_policy_based_route method of the client was called with the request
    client.return_value.delete_policy_based_route.assert_called_once_with(request=delete_request.return_value)
