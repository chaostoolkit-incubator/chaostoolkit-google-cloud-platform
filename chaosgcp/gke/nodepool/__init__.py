import time

from chaoslib.types import Configuration, Secrets
from chaosreliably import ActivityFailed
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
