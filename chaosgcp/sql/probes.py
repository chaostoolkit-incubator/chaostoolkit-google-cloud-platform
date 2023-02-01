# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets

from chaosgcp import get_context, get_service

__all__ = ["list_instances", "describe_instance"]


def list_instances(
    configuration: Configuration = None, secrets: Secrets = None
) -> Dict[str, Any]:
    """
    Lists Cloud SQL instances in a given project in the alphabetical order of
    the instance name.

    See: https://cloud.google.com/sql/docs/postgres/admin-api/v1/instances/list
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "sqladmin",
        version="v1",
        configuration=configuration,
        secrets=secrets,
    )

    instances = []

    request = service.instances().list(project=ctx.project_id)
    while request is not None:
        response = request.execute()
        instances.extend(response["items"])
        request = service.instances().list_next(
            previous_request=request, previous_response=response
        )

    return {"instances": instances}


def describe_instance(
    instance_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Displays configuration and metadata about a Cloud SQL instance.

    Information such as instance name, IP address, region, the CA certificate
    and configuration settings will be displayed.

    See: https://cloud.google.com/sql/docs/postgres/admin-api/v1/instances/get

    :param instance_id: Cloud SQL instance ID.
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "sqladmin",
        version="v1",
        configuration=configuration,
        secrets=secrets,
    )

    request = service.instances().get(
        project=ctx.project_id, instance=instance_id
    )
    response = request.execute()
    return response


def list_databases(
    instance_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Lists databases in the specified Cloud SQL instance

    See: https://cloud.google.com/sql/docs/postgres/admin-api/rest/v1/databases/list

    :param instance_id: Cloud SQL instance ID.
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "sqladmin",
        version="v1",
        configuration=configuration,
        secrets=secrets,
    )

    request = service.databases().list(
        project=ctx.project_id, instance=instance_id
    )
    response = request.execute()

    databases = response.get("items", [])
    return {"databases": databases}


def describe_database(
    instance_id: str,
    database_name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Displays configuration and metadata about a Cloud SQL database

    Information such as database name, charset, and collation
    will be displayed.

    See: https://cloud.google.com/sql/docs/postgres/admin-api/rest/v1/databases/get

    :param instance_id: Cloud SQL instance ID.
    :param database: Cloud SQL database name.
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "sqladmin",
        version="v1",
        configuration=configuration,
        secrets=secrets,
    )

    request = service.databases().get(
        project=ctx.project_id, instance=instance_id, database=database_name
    )
    response = request.execute()

    return response
