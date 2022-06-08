# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosgcp import get_context, get_service, wait_on_operation
from chaosgcp.sql.probes import describe_instance

__all__ = ["trigger_failover", "export_data", "import_data"]


def trigger_failover(
    instance_id: str,
    wait_until_complete: bool = True,
    settings_version: int = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Causes a high-availability Cloud SQL instance to failover.

    See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/failover

    :param instance_id: Cloud SQL instance ID.
    :param wait_until_complete: wait for the operation in progress to complete.
    :param settings_version: The current settings version of this instance.

    :return:
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "sqladmin",
        version="v1beta4",
        configuration=configuration,
        secrets=secrets,
    )

    if not settings_version:
        # dynamically fetches the value from instance description
        instance = describe_instance(
            instance_id, configuration=configuration, secrets=secrets
        )
        settings_version = instance["settings"]["settingsVersion"]

    failover_request_body = {
        "failoverContext": {
            "kind": "sql#failoverContext",
            "settingsVersion": settings_version,
        }
    }
    request = service.instances().failover(
        project=ctx.project_id, instance=instance_id, body=failover_request_body
    )
    response = request.execute()

    logger.debug(
        "Database {db} failover: {resp}".format(db=instance_id, resp=response)
    )

    if wait_until_complete:
        ops = service.operations()
        response = wait_on_operation(
            ops, project=ctx.project_id, operation=response["name"]
        )

    return response


def export_data(
    instance_id: str,
    storage_uri: str,
    project_id: str = None,
    file_type: str = "sql",
    databases: List[str] = None,
    tables: List[str] = None,
    export_schema_only: bool = False,
    wait_until_complete: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Exports data from a Cloud SQL instance to a Cloud Storage bucket
    as a SQL dump or CSV file.

    See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/export

    If `project_id` is given, it will take precedence over the global
    project ID defined at the configuration level.
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)

    if file_type not in ["sql", "csv"]:
        raise ActivityFailed(
            "Cannot export database. "
            "File type '{ft}' is invalid.".format(ft=file_type)
        )
    if not project_id and not ctx.project_id:
        raise ActivityFailed(
            "Cannot import data into database. "
            "The project ID must be defined in configuration or as argument."
        )

    if databases is None:
        databases = []
    if tables is None:
        tables = []

    export_request_body = {
        "exportContext": {
            "kind": "sql#exportContext",
            "fileType": file_type,
            "uri": storage_uri,
            "databases": databases,
        }
    }

    if file_type == "sql":
        export_request_body["sqlExportOptions"] = {
            "tables": tables,
            "schemaOnly": export_schema_only,
            "mysqlExportOptions": {"masterData": 0},
        }
    elif file_type == "csv":
        export_request_body["csvExportOptions"] = {"selectQuery": databases[0]}

    service = get_service(
        "sqladmin",
        version="v1beta4",
        configuration=configuration,
        secrets=secrets,
    )
    request = service.instances().export(
        project=project_id or ctx.project_id,
        instance=instance_id,
        body=export_request_body,
    )
    response = request.execute()

    logger.debug(
        "Export data from database {db}[{proj}]: {resp}".format(
            proj=project_id or ctx.project_id, db=instance_id, resp=response
        )
    )

    if wait_until_complete:
        ops = service.operations()
        response = wait_on_operation(
            ops, project=ctx.project_id, operation=response["name"]
        )

    return response


def import_data(
    instance_id: str,
    storage_uri: str,
    database: str,
    project_id: str = None,
    file_type: str = "sql",
    import_user: str = None,
    table: str = None,
    columns: List[str] = None,
    wait_until_complete: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Imports data into a Cloud SQL instance from a SQL dump or CSV file
    in Cloud Storage.

    See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/import

    If `project_id` is given, it will take precedence over the global
    project ID defined at the configuration level.
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)

    if file_type not in ["sql", "csv"]:
        raise ActivityFailed(
            "Cannot import data into database. "
            "File type '{ft}' is invalid.".format(ft=file_type)
        )
    if not database:
        raise ActivityFailed(
            "Cannot import data into database. " "Database name is required."
        )
    if not storage_uri:
        raise ActivityFailed(
            "Cannot import data into database. "
            "Path of the import file in Cloud Storage is required."
        )
    if file_type == "csv" and not table:
        raise ActivityFailed(
            "Cannot import data into database. "
            "The table to which CSV data is imported is required"
        )
    if not project_id and not ctx.project_id:
        raise ActivityFailed(
            "Cannot import data into database. "
            "The project ID must be defined in configuration or as argument."
        )

    if columns is None:
        columns = []

    import_request_body = {
        "importContext": {
            "kind": "sql#importContext",
            "fileType": file_type,
            "uri": storage_uri,
            "database": database,
            "importUser": import_user,
        }
    }

    if file_type == "csv":
        import_request_body["csvImportOptions"] = {
            "table": table,
            "columns": columns,
        }

    service = get_service(
        "sqladmin",
        version="v1beta4",
        configuration=configuration,
        secrets=secrets,
    )
    request = service.instances().import_(
        project=project_id or ctx.project_id,
        instance=instance_id,
        body=import_request_body,
    )
    response = request.execute()

    logger.debug(
        "Import data into database {db}[{proj}]: {resp}".format(
            proj=project_id or ctx.project_id, db=instance_id, resp=response
        )
    )

    if wait_until_complete:
        ops = service.operations()
        response = wait_on_operation(
            ops, project=ctx.project_id, operation=response["name"]
        )

    return response
