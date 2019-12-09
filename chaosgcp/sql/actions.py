# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosgcp import wait_on_operation, get_context, get_service
from chaosgcp.sql.probes import describe_instance

__all__ = ["trigger_failover"]


def trigger_failover(instance_id: str,
                     wait_until_complete: bool = True,
                     settings_version: int = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None) -> Dict[str, Any]:
    """
    Causes a high-availability Cloud SQL instance to failover.

    See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/failover

    :param instance_id: Cloud SQL instance ID.
    :param wait_until_complete: wait for the operation in progress to complete.
    :param settings_version: The current settings version of this instance.

    :return:
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service('sqladmin', version='v1beta4',
                          configuration=configuration, secrets=secrets)

    if not settings_version:
        # dynamically fetches the value from instance description
        instance = describe_instance(instance_id,
                                     configuration=configuration,
                                     secrets=secrets)
        settings_version = instance["settings"]["settingsVersion"]

    failover_request_body = {
        "failoverContext": {
            "kind": "sql#failoverContext",
            "settingsVersion": settings_version
        }
    }
    request = service.instances().failover(project=ctx.project_id,
                                           instance=instance_id,
                                           body=failover_request_body)
    response = request.execute()

    logger.debug('Database {db} failover: {resp}'.format(
        db=instance_id, resp=response
    ))

    if wait_until_complete:
        ops = service.operations()
        response = wait_on_operation(
            ops, project=ctx.project_id, operation=response["name"])

    return response
