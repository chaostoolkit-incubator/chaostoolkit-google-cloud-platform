# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaosk8s.node.actions import drain_nodes
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosgcp import context_from_parent_path, get_parent, to_dict
from chaosgcp.gke.nodepool import (
    convert_nodepool_format,
    get_client,
    wait_on_operation,
)

__all__ = [
    "create_new_nodepool",
    "delete_nodepool",
    "swap_nodepool",
    "rollback_nodepool",
]


def create_new_nodepool(
    body: Dict[str, Any],
    parent: str = None,
    wait_until_complete: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Create a new node pool in the given cluster/zone of the provided project.

    The node pool config must be passed a mapping to the `body` parameter and
    respect the REST API.

    If `wait_until_complete` is set to `True` (the default), the function
    will block until the node pool is ready. Otherwise, will return immediatly
    with the operation information.

    See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/create
    """  # noqa: E501
    parent = get_parent(parent, configuration=configuration, secrets=secrets)
    client = get_client(configuration, secrets)
    node_pool = convert_nodepool_format(body)
    response = client.create_node_pool(parent=parent, node_pool=node_pool)

    if wait_until_complete:
        logger.info("Waiting on node pool to be created...")
        ctx = context_from_parent_path(parent)
        response = wait_on_operation(client, response, ctx)

    logger.debug("NodePool creation: {}".format(str(response)))
    return to_dict(response)


def delete_nodepool(
    parent: str = None,
    node_pool_id: str = None,
    wait_until_complete: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Delete node pool from the given cluster/zone of the provided project.

    If `wait_until_complete` is set to `True` (the default), the function
    will block until the node pool is deleted. Otherwise, will return
    immediatly with the operation information.

    See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/create
    """  # noqa: E501
    parent = get_parent(parent, node_pool_id, configuration, secrets)
    client = get_client(configuration, secrets)
    response = client.delete_node_pool(name=parent)

    if wait_until_complete:
        logger.info("Waiting on node pool to be deleted...")
        ctx = context_from_parent_path(parent)
        response = wait_on_operation(client, response, ctx)

    logger.debug("NodePool deletion: {}".format(str(response)))
    return to_dict(response)


def swap_nodepool(
    old_node_pool_id: str,
    new_nodepool_body: Dict[str, Any],
    parent: str = None,
    wait_until_complete: bool = True,
    delete_old_node_pool: bool = False,
    drain_timeout: int = 120,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Create a new nodepool, drain the old one so pods can be rescheduled on the
    new pool. Delete the old nodepool only `delete_old_node_pool` is set to
    `True`, which is not the default. Otherwise, leave the old node pool
    cordonned so it cannot be scheduled any longer.

    Please ensure to provide the Kubernetes secrets as well when calling this
    action.
    See https://github.com/chaostoolkit/chaostoolkit-kubernetes#configuration
    """
    new_nodepool_response = create_new_nodepool(
        parent=parent,
        body=new_nodepool_body,
        wait_until_complete=wait_until_complete,
        configuration=configuration,
        secrets=secrets,
    )

    logger.debug("New nodepool '{}' created".format(new_nodepool_response))

    drain_nodes(
        timeout=drain_timeout,
        delete_pods_with_local_storage=False,
        secrets=secrets,
        label_selector="cloud.google.com/gke-nodepool={}".format(
            old_node_pool_id
        ),
    )

    logger.info("Old nodepool '{}' drained".format(old_node_pool_id))

    if delete_old_node_pool:
        logger.debug("Deleting now nodepool '{}'".format(old_node_pool_id))
        delete_nodepool(
            parent=parent,
            node_pool_id=old_node_pool_id,
            wait_until_complete=wait_until_complete,
            configuration=configuration,
            secrets=secrets,
        )

    return new_nodepool_response


def rollback_nodepool(
    node_pool_id: str,
    parent: str = None,
    wait_until_complete: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Rollback a previously Aborted or Failed NodePool upgrade.

    If `wait_until_complete` is set to `True` (the default), the function
    will block until the node pool is ready. Otherwise, will return immediatly
    with the operation information.

    See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/create
    """  # noqa: E501
    parent = get_parent(parent, node_pool_id, configuration, secrets)
    client = get_client(configuration, secrets)
    response = client.rollback_node_pool_upgrade(name=parent)

    logger.debug("NodePool upgrade rollback: {}".format(str(response)))

    if wait_until_complete:
        ctx = context_from_parent_path(parent)
        response = wait_on_operation(client, response, ctx)

    return response
