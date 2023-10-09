# -*- coding: utf-8 -*-
import os.path
import time
from datetime import datetime
from typing import Any, Dict, List, Tuple

import dateparser
import httplib2
from chaoslib.discovery.discover import (
    discover_actions,
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.exceptions import ActivityFailed, FailedActivity
from chaoslib.types import (
    Configuration,
    DiscoveredActivities,
    Discovery,
    Secrets,
)
from google.api_core.extended_operation import ExtendedOperation
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource, build
from logzero import logger

from chaosgcp.types import GCPContext

__all__ = [
    "__version__",
    "client",
    "discover",
    "get_context",
    "get_parent",
    "get_service",
    "wait_on_operation",
    "wait_on_extended_operation",
    "load_credentials",
    "to_dict",
    "context_from_parent_path",
    "parse_interval",
]
__version__ = "0.12.3"


def get_service(
    service_name: str,
    version: str = "v1",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Resource:
    """
    Create a client for the given service/version couple.
    """
    return client(service_name, version=version, secrets=secrets)


def get_context(
    configuration: Configuration, secrets: Secrets = None
) -> GCPContext:
    """
    Collate all the GCP context information.
    """
    return GCPContext(
        project_id=configuration.get("gcp_project_id"),
        cluster_name=configuration.get("gcp_gke_cluster_name"),
        region=configuration.get("gcp_region"),
        zone=configuration.get("gcp_zone"),
        parent=configuration.get("gcp_parent"),
    )


def context_from_parent_path(parent: str) -> GCPContext:
    logger.debug(f"Loading GCP context from '{parent}'")
    _, project_id, _, location, *rest = parent.split("/")
    region = location
    zone = None

    elements = location.rsplit("-", 1)

    if len(elements) == 2:
        zone = location
        region = elements[0]

    cluster_name = None
    index_of_clusters = rest.index("clusters")
    if index_of_clusters > 0:
        cluster_name = rest[index_of_clusters + 1]

    return GCPContext(
        project_id=project_id,
        region=region,
        zone=zone,
        cluster_name=cluster_name,
        parent=parent,
    )


def wait_on_operation(
    operation_service: Any, frequency: int = 1, **kwargs: Dict
) -> Dict[str, Any]:
    """
    Wait until the given operation is completed and return the result.
    """
    while True:
        logger.debug(
            "Waiting for operation '{}'".format(
                kwargs.get("operationId", kwargs.get("operation"))
            )
        )

        result = operation_service.get(**kwargs).execute()

        if result["status"] == "DONE":
            return result

        time.sleep(frequency)


def wait_on_extended_operation(
    operation: ExtendedOperation, frequency: int = 1, timeout: int = 60
) -> None:
    start = time.time()

    while True:
        logger.debug(
            "Waiting for extended operation '{}'".format(operation.name)
        )

        if operation.done():
            logger.debug(f"Extended operation '{operation.name}' is done")
            return None

        time.sleep(frequency)

        if (start + timeout) < time.time():
            logger.debug(f"Cancelling extended operation '{operation.name}'")
            operation.cancel()
            return None


def load_credentials(secrets: Secrets = None):
    """
    Load GCP credentials from the experiment secrets

    To authenticate, you need to create a service account manually and either
    pass the filename or the content of the file into the `secrets` object.

    So, in the experiment, use one of the followings:

    ```json
    {
        "gcp": {
            "service_account_file": "/path/to/file.json"
        }
    }
    ```

    ```json
    {
        "gcp": {
            "service_account_info": {
                "type": "service_account",
                "project_id": "...",
                "private_key_id": "...",
                "private_key": "...",
                "client_email": "...",
                "client_id": "...",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...."
            }
        }
    }
    ```

    You would likely want to read value from the environment or Vault if you
    use the second approach, and avoid storing sensitive data into the
    experiment itself.

    Make sure your service account has enough permissions for the activities
    you wish to conduct (though do not give it too wide permissions either).

    See: https://developers.google.com/api-client-library/python/auth/service-accounts
    Also: http://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html
    """  # noqa: E501
    secrets = secrets or {}
    service_account_file = secrets.get("service_account_file")
    service_account_info = secrets.get("service_account_info")

    if not service_account_file:
        google_app_creds = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS",
            os.getenv("GCP_APPLICATION_CREDENTIALS"),
        )
        if google_app_creds:
            service_account_file = google_app_creds

    credentials = None
    if service_account_file:
        service_account_file = os.path.expanduser(service_account_file)
        if not os.path.exists(service_account_file):
            raise FailedActivity(
                "GCP account settings not found at {}".format(
                    service_account_file
                )
            )

        logger.debug(
            "Using GCP credentials from file: {}".format(service_account_file)
        )
        credentials = Credentials.from_service_account_file(
            service_account_file
        )
    elif service_account_info and isinstance(service_account_info, dict):
        logger.debug("Using GCP credentials embedded into secrets")
        credentials = Credentials.from_service_account_info(
            service_account_info
        )
    else:
        raise FailedActivity(
            "missing GCP credentials settings in secrets of this activity"
        )

    if credentials is not None and credentials.expired:
        logger.debug("GCP credentials need to be refreshed as they expired")
        credentials.refresh(httplib2.Http())

    if not credentials:
        raise FailedActivity(
            "missing a service account to authenticate with the "
            "Google Cloud Platform"
        )

    return credentials


def client(
    service_name: str, version: str = "v1", secrets: Secrets = None
) -> Resource:
    """
    Create a client for the given service.
    """
    credentials = load_credentials(secrets=secrets)
    return build(service_name, version=version, credentials=credentials)


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Google Cloud Platform capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-google-cloud")

    discovery = initialize_discovery_result(
        "chaostoolkit-google-cloud", __version__, "gcp"
    )
    discovery["activities"].extend(load_exported_activities())
    return discovery


def get_parent(
    parent: str = None,
    node_pool_id: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> str:
    if parent:
        return parent

    ctx = get_context(configuration=configuration, secrets=secrets)
    parent = ctx.get_cluster_parent()

    if not parent:
        raise ActivityFailed(
            "Missing GCP configuration keys to the path of the resource"
        )

    if node_pool_id:
        parent = f"{parent}/nodePools/{node_pool_id}"

    return parent


def to_dict(response: Any) -> dict:
    return response.__class__.to_dict(response)


def parse_interval(
    end_time: str = "now", window: str = "1h"
) -> Tuple[datetime, datetime]:
    end_time = dateparser.parse(
        end_time, settings={"TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True}
    )
    if not end_time:
        raise ActivityFailed("unparsable end time value")

    start_time = dateparser.parse(
        window,
        settings={
            "TIMEZONE": "UTC",
            "RELATIVE_BASE": end_time,
            "RETURN_AS_TIMEZONE_AWARE": True,
        },
    )
    if not start_time:
        raise ActivityFailed("unparsable window value")

    return (start_time, end_time)


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaosgcp.gke.nodepool.actions"))
    activities.extend(discover_probes("chaosgcp.gke.nodepool.probes"))
    activities.extend(discover_actions("chaosgcp.sql.actions"))
    activities.extend(discover_probes("chaosgcp.sql.probes"))
    activities.extend(discover_probes("chaosgcp.storage.probes"))
    activities.extend(discover_actions("chaosgcp.cloudbuild.actions"))
    activities.extend(discover_probes("chaosgcp.cloudbuild.probes"))
    activities.extend(discover_actions("chaosgcp.cloudrun.actions"))
    activities.extend(discover_probes("chaosgcp.cloudrun.probes"))
    activities.extend(discover_probes("chaosgcp.monitoring.probes"))
    activities.extend(discover_probes("chaosgcp.cloudlogging.probes"))
    activities.extend(discover_probes("chaosgcp.artifact.probes"))
    activities.extend(discover_actions("chaosgcp.lb.actions"))
    return activities
