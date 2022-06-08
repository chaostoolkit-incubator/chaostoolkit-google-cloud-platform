# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

import fixtures

from chaosgcp.gke.nodepool.actions import (
    create_new_nodepool,
    delete_nodepool,
    swap_nodepool,
)


@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_create_nodepool(Credentials, service_builder, wait_on_operation):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc
    create_np = MagicMock()
    nodepool_svc.create = create_np
    create_np.return_value.execute.return_value = {"name": "mynodepool"}

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    create_new_nodepool(
        body=fixtures.nodepool.body,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    create_np.assert_called_with(
        projectId=project_id,
        zone=zone,
        clusterId=cluster_name,
        body=fixtures.nodepool.body,
    )

    wait_on_operation.assert_called_with(
        ops_svc,
        projectId=fixtures.configuration["gcp_project_id"],
        zone=fixtures.configuration["gcp_zone"],
        operationId="mynodepool",
    )


@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_delete_nodepool(Credentials, service_builder, wait_on_operation):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc
    delete_np = MagicMock()
    nodepool_svc.delete = delete_np
    delete_np.return_value.execute.return_value = {"name": "mynodepool"}

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    delete_nodepool(
        node_pool_id="mynodepool",
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    delete_np.assert_called_with(
        projectId=project_id,
        zone=zone,
        clusterId=cluster_name,
        nodePoolId="mynodepool",
    )

    wait_on_operation.assert_called_with(
        ops_svc,
        projectId=fixtures.configuration["gcp_project_id"],
        zone=fixtures.configuration["gcp_zone"],
        operationId="mynodepool",
    )


@patch("chaosgcp.gke.nodepool.actions.drain_nodes", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_swap_nodepool(
    Credentials, service_builder, wait_on_operation, drain_nodes
):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc

    create_np = MagicMock()
    nodepool_svc.create = create_np
    create_np.return_value.execute.return_value = {"name": "default-pool"}

    delete_np = MagicMock()
    nodepool_svc.delete = delete_np
    delete_np.return_value.execute.return_value = {"name": "mynodepool"}

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    swap_nodepool(
        old_node_pool_id="mynodepool",
        new_nodepool_body=fixtures.nodepool.body,
        delete_old_node_pool=True,
        secrets=fixtures.secrets_with_k8s,
        configuration=fixtures.configuration,
    )

    create_np.assert_called_with(
        projectId=project_id,
        zone=zone,
        clusterId=cluster_name,
        body=fixtures.nodepool.body,
    )

    drain_nodes.assert_called_with(
        timeout=120,
        delete_pods_with_local_storage=False,
        secrets=fixtures.secrets_with_k8s,
        label_selector="cloud.google.com/gke-nodepool=mynodepool",
    )

    delete_np.assert_called_with(
        projectId=project_id,
        zone=zone,
        clusterId=cluster_name,
        nodePoolId="mynodepool",
    )

    wait_on_operation.assert_called_with(
        ops_svc,
        projectId=fixtures.configuration["gcp_project_id"],
        zone=fixtures.configuration["gcp_zone"],
        operationId="mynodepool",
    )


@patch("chaosgcp.gke.nodepool.actions.drain_nodes", autospec=False)
@patch("chaosgcp.gke.nodepool.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_swap_nodepool_without_delete(
    Credentials, service_builder, wait_on_operation, drain_nodes
):
    project_id = fixtures.configuration["gcp_project_id"]
    cluster_name = fixtures.configuration["gcp_gke_cluster_name"]
    zone = fixtures.configuration["gcp_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc

    create_np = MagicMock()
    nodepool_svc.create = create_np
    create_np.return_value.execute.return_value = {"name": "default-pool"}

    delete_np = MagicMock()
    nodepool_svc.delete = delete_np
    delete_np.return_value.execute.return_value = {"name": "mynodepool"}

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    swap_nodepool(
        old_node_pool_id="mynodepool",
        new_nodepool_body=fixtures.nodepool.body,
        delete_old_node_pool=False,
        secrets=fixtures.secrets_with_k8s,
        configuration=fixtures.configuration,
    )

    create_np.assert_called_with(
        projectId=project_id,
        zone=zone,
        clusterId=cluster_name,
        body=fixtures.nodepool.body,
    )

    drain_nodes.assert_called_with(
        timeout=120,
        delete_pods_with_local_storage=False,
        secrets=fixtures.secrets_with_k8s,
        label_selector="cloud.google.com/gke-nodepool=mynodepool",
    )

    delete_np.assert_not_called()
