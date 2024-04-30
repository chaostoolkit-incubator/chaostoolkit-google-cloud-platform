# Copyright 2024 Google LLC.
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import MagicMock, patch
from google.cloud import networkconnectivity_v1
from chaosgcp.networkconnectivity.actions import create_policy_based_route, delete_policy_based_route

@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.CreatePolicyBasedRouteRequest", autospec=True)
@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.PolicyBasedRoutingServiceClient", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_create_policy_based_route(Credentials, client, create_route_req):
    parent_value = "projects/test-project/locations/global"
    name = "test-route"
    next_hop_ilb_ip = "10.0.0.1"
    network = "test-network"
    src_range = "192.168.0.0/24"
    dest_range = "10.1.0.0/16"
    priority = 100

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()

    request = networkconnectivity_v1.CreatePolicyBasedRouteRequest.return_value
    create_route_req.return_value = request

    response_mock = MagicMock()
    client.return_value.create_policy_based_route.return_value = response_mock

    response_mock_to_dict = MagicMock()
    response_mock.__class__.to_dict = MagicMock(return_value=response_mock_to_dict)


    result = create_policy_based_route(
        parent_value, name, next_hop_ilb_ip, network, src_range, dest_range, priority
    )

    assert result == response_mock_to_dict

    response_mock.__class__.to_dict.assert_called_once_with(response_mock)
    client.return_value.create_policy_based_route.assert_called_once_with(
        request=request
    )

@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.DeletePolicyBasedRouteRequest", autospec=True)
@patch("chaosgcp.networkconnectivity.actions.networkconnectivity_v1.PolicyBasedRoutingServiceClient", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_delete_policy_based_route(Credentials, client, delete_route_req):
    route_name = "test-route"

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()

    request = networkconnectivity_v1.DeletePolicyBasedRouteRequest.return_value
    delete_route_req.return_value = request

    response_mock = MagicMock()
    client.return_value.delete_policy_based_route.return_value = response_mock

    response_mock_to_dict = MagicMock()
    response_mock.__class__.to_dict = MagicMock(return_value=response_mock_to_dict)

    result = delete_policy_based_route(route_name)

    assert result == response_mock_to_dict

    response_mock.__class__.to_dict.assert_called_once_with(response_mock)
    delete_route_req.assert_called_once_with(
        name=route_name,
    )
    client.return_value.delete_policy_based_route.assert_called_once_with(
        request=request
    )
