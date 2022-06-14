# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosgcp import get_context, get_service

__all__ = ["list_nodepools", "get_nodepool"]


def list_nodepools(
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    List nodepools of a cluster.

    See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/list
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "container", configuration=configuration, secrets=secrets
    )
    np = service.projects().zones().clusters().nodePools()
    response = np.list(
        projectId=ctx.project_id,
        zone=ctx.zone,
        clusterId=ctx.cluster_name,
    ).execute()

    logger.debug("NodePool listing: {}".format(str(response)))

    return response


def get_nodepool(
    node_pool_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get a specific nodepool of a cluster.

    See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/get
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "container", configuration=configuration, secrets=secrets
    )
    np = service.projects().zones().clusters().nodePools()
    response = np.get(
        projectId=ctx.project_id,
        zone=ctx.zone,
        clusterId=ctx.cluster_name,
        nodePoolId=node_pool_id,
    ).execute()

    logger.debug("NodePool retrieved: {}".format(str(response)))

    return response
