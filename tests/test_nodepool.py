# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

import fixtures
from google.cloud import container_v1

from chaosgcp.gke.nodepool.actions import (
    create_new_nodepool,
    delete_nodepool,
    swap_nodepool,
)


@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.get_client", autospec=True)
@patch("chaosgcp.gke.nodepool.actions.get_parent", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_create_nodepool(
    Credentials, get_parent, get_client, wait_on_operation
):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    parent = f"projects/{project_id}/locations/{zone}/clusters/{cluster_name}"
    get_parent.return_value = parent

    client = MagicMock()
    get_client.return_value = client

    client.create_node_pool.return_value = container_v1.Operation(name="op1")

    create_new_nodepool(
        parent=parent,
        wait_until_complete=False,
        body=fixtures.nodepool.body,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    client.create_node_pool.assert_called_with(
        parent=parent,
        node_pool=fixtures.nodepool.body,
    )


@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.get_client", autospec=True)
@patch("chaosgcp.gke.nodepool.actions.get_parent", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_delete_nodepool(
    Credentials, get_parent, get_client, wait_on_operation
):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    parent = (
        f"projects/{project_id}/locations/{zone}/clusters"
        f"/{cluster_name}/nodePools/mynodepool"
    )
    get_parent.return_value = parent

    client = MagicMock()
    get_client.return_value = client

    client.delete_node_pool.return_value = container_v1.Operation(name="op1")

    delete_nodepool(
        node_pool_id="mynodepool",
        wait_until_complete=False,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    client.delete_node_pool.assert_called_with(name=parent)


@patch("chaosgcp.gke.nodepool.actions.drain_nodes", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.get_client", autospec=True)
@patch("chaosgcp.gke.nodepool.actions.get_parent", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_swap_nodepool(
    Credentials, get_parent, get_client, wait_on_operation, drain_nodes
):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    parent = f"projects/{project_id}/locations/{zone}/clusters/{cluster_name}"
    parent2 = (
        f"projects/{project_id}/locations/{zone}"
        f"/clusters/{cluster_name}/nodePools/mynodepool"
    )
    get_parent.side_effect = [parent, parent2]

    client = MagicMock()
    get_client.side_effect = [client, client]
    client.create_node_pool.return_value = container_v1.Operation(name="op1")

    client.delete_node_pool.return_value = container_v1.Operation(name="op2")

    swap_nodepool(
        old_node_pool_id="mynodepool",
        wait_until_complete=False,
        new_nodepool_body=fixtures.nodepool.body,
        delete_old_node_pool=True,
        secrets=fixtures.secrets_with_k8s,
        configuration=fixtures.configuration,
    )

    client.create_node_pool.assert_called_with(
        parent=parent,
        node_pool=fixtures.nodepool.body,
    )

    drain_nodes.assert_called_with(
        timeout=120,
        delete_pods_with_local_storage=False,
        secrets=fixtures.secrets_with_k8s,
        label_selector="cloud.google.com/gke-nodepool=mynodepool",
    )

    client.delete_node_pool.assert_called_with(name=parent2)


@patch("chaosgcp.gke.nodepool.actions.drain_nodes", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.get_client", autospec=True)
@patch("chaosgcp.gke.nodepool.actions.get_parent", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_swap_nodepool_without_delete(
    Credentials, get_parent, get_client, wait_on_operation, drain_nodes
):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    parent = f"projects/{project_id}/locations/{zone}/clusters/{cluster_name}"
    get_parent.return_value = parent

    client = MagicMock()
    get_client.return_value = client

    client.create_node_pool.return_value = container_v1.Operation(name="op1")

    swap_nodepool(
        parent=parent,
        wait_until_complete=False,
        old_node_pool_id="mynodepool",
        new_nodepool_body=fixtures.nodepool.body,
        delete_old_node_pool=False,
        secrets=fixtures.secrets_with_k8s,
        configuration=fixtures.configuration,
    )

    client.create_node_pool.assert_called_with(
        parent=parent,
        node_pool=fixtures.nodepool.body,
    )

    drain_nodes.assert_called_with(
        timeout=120,
        delete_pods_with_local_storage=False,
        secrets=fixtures.secrets_with_k8s,
        label_selector="cloud.google.com/gke-nodepool=mynodepool",
    )

    client.delete_node_pool.assert_not_called()
