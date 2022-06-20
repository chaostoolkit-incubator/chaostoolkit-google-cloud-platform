# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from google.cloud import container_v1
from logzero import logger

from chaosgcp import get_parent, to_dict
from chaosgcp.gke.nodepool import get_client

__all__ = ["list_nodepools", "get_nodepool"]


def list_nodepools(
    parent: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    List nodepools of a cluster.

    The `parent` is following the form `projects/*/locations/*/clusters/*`
    and will override any settings in the configuration block. If not provided
    this action uses the configuration settings.

    See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/list
    """  # noqa: E501
    parent = get_parent(parent, configuration=configuration, secrets=secrets)
    client = get_client(configuration, secrets)
    response = client.list_node_pools(parent=parent)
    logger.debug("NodePool listing: {}".format(str(response)))
    return to_dict(response)


def get_nodepool(
    node_pool_id: str = None,
    parent: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get a specific nodepool of a cluster.

    The `parent` is following the form
    `projects/*/locations/*/clusters/*/nodePools/*`
    and will override any settings in the configuration block.

    ```json
    {
        "name": "retrieve-our-nodepool",
        "type": "probe",
        "provider": {
            "type": "python",
            "module": "chaosgcp.gke.nodepool.probes",
            "func": "get_nodepool",
            "secrets": ["gcp"],
            "arguments": {
                "parent": "projects/my-project-89/locations/us-east1/clusters/cluster-1/nodePools/default-pool"
            }
        }
    }
    ```

    If not provided this action uses the configuration settings. In that case,
    make sure to also pass the `node_pool_id` value.

    ```json
    {
        "name": "retrieve-our-nodepool",
        "type": "probe",
        "provider": {
            "type": "python",
            "module": "chaosgcp.gke.nodepool.probes",
            "func": "get_nodepool",
            "secrets": ["gcp"],
            "arguments": {
                "node_pool_id": "default-pool"
            }
        }
    }
    ```

    See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/get
    """  # noqa: E501
    parent = get_parent(parent, node_pool_id, configuration, secrets)
    client = get_client(configuration, secrets)
    request = container_v1.GetNodePoolRequest(name=parent)
    response = client.get_node_pool(request)
    logger.debug("NodePool fetched: {}".format(str(response)))
    return to_dict(response)
