import re
import time
from typing import Any, Dict

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from google.cloud import container_v1
from logzero import logger

from chaosgcp import load_credentials
from chaosgcp.types import GCPContext


def get_client(
    configuration: Configuration = None, secrets: Secrets = None
) -> container_v1.ClusterManagerClient:
    credentials = load_credentials(secrets)
    return container_v1.ClusterManagerClient(credentials=credentials)


def wait_on_operation(
    client: container_v1.ClusterManagerClient,
    op: container_v1.Operation,
    ctx: GCPContext,
    timeout: int = 0,
    poll_frequency: int = 1,
) -> container_v1.Operation:
    """
    Wait until the given operation is completed and return the result.

    You can set a timeout for the operation to complete. If `0`, no timeout
    is applied.
    """
    parent = ctx.get_operation_parent(op.name)
    started = time.time()

    while True:
        response = client.get_operation(name=parent)
        if response.status == container_v1.Operation.Status.DONE:
            return response

        if timeout > 0 and (started + timeout) > time.time():
            raise ActivityFailed(
                "operation failed in the given allowed timeout"
            )

        logger.debug(f"Waiting on operation: {parent} => {response.status}")
        time.sleep(poll_frequency)


def convert_nodepool_format(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    The newer version of the GCP API requires snake_case. We try our best
    to convert camelCase on the fly and warn users they ought to update
    accordingly.

    ```json
    "body": {
        "nodePool": {
            "config": {
                "oauthScopes": [
                    "gke-version-default",
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/trace.append"
                ]
            },
            "initialNodeCount": 1,
            "name": "default-pool"
        }
    }
    ```

    becomes:

    ```json
    "body": {
        "config": {
            "oauth_scopes": [
                "gke-version-default",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/logging.write",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/service.management.readonly",
                "https://www.googleapis.com/auth/servicecontrol",
                "https://www.googleapis.com/auth/trace.append"
            ]
        },
        "initial_node_count": 1,
        "name": "default-pool"
    }
    ```
    """
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    converted_once = False

    def convert(d: Dict[str, Any]) -> Dict[str, Any]:
        nonlocal converted_once
        r = {}
        for k, v in d.items():
            new_key = pattern.sub("_", k).lower()
            if converted_once is False and k != new_key:
                converted_once = True
            if isinstance(v, dict):
                r[new_key] = convert(v)
            else:
                r[new_key] = v
        return r

    # not used any longer
    if "nodePool" in body:
        body = body["nodePool"]

    result = convert(body)

    if converted_once:
        logger.debug(
            "The nodepool payload should now use snake_case for all its keys."
            "Please update your experiment's payload accordingly:"
        )
        logger.debug(f"Got: {body}")
        logger.debug(f"Converted to: {result}")

    return result
