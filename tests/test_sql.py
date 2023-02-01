# -*- coding: utf-8 -*-
from unittest.mock import ANY, MagicMock, patch

import fixtures

from chaosgcp.sql.actions import export_data, import_data, trigger_failover
from chaosgcp.sql.probes import (
    describe_database,
    describe_instance,
    list_databases,
    list_instances,
)


@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_list_instances(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    instances_svc = MagicMock()
    service.instances.return_value = instances_svc
    _list_instances = MagicMock()
    instances_svc.list = _list_instances
    _list_instances_resp = {"items": fixtures.sql.instances}
    _list_instances.return_value.execute.return_value = _list_instances_resp
    _list_next_instances = MagicMock(return_value=None)
    instances_svc.list_next = _list_next_instances

    list_instances(
        secrets=fixtures.secrets, configuration=fixtures.configuration
    )

    _list_instances.assert_called_with(project=project_id)
    _list_next_instances.assert_called_with(
        previous_request=_list_instances(),
        previous_response=_list_instances_resp,
    )


@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_describe_instances(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]
    instance_id = fixtures.sql.instances[0]["name"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    instances_svc = MagicMock()
    service.instances.return_value = instances_svc
    instances_get = MagicMock()
    instances_svc.get = instances_get
    instances_get.return_value.execute.return_value = fixtures.sql.instances[0]

    describe_instance(
        instance_id,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    instances_get.assert_called_with(project=project_id, instance=instance_id)


@patch("chaosgcp.sql.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_trigger_failover(Credentials, service_builder, wait_on_operation):
    project_id = fixtures.configuration["gcp_project_id"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    instances_svc = MagicMock()
    service.instances.return_value = instances_svc
    instances_failover = MagicMock()
    instances_svc.failover = instances_failover
    instances_failover.return_value.execute.return_value = (
        fixtures.sql.failover_operation
    )
    instances_get = MagicMock()
    instances_svc.get = instances_get
    instances_get.return_value.execute.return_value = fixtures.sql.instances[0]

    ops_svc = MagicMock()
    service.operations.return_value = ops_svc

    trigger_failover(
        fixtures.sql.instances[0]["name"],
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
        wait_until_complete=True,
    )

    instances_get.assert_called_with(
        project=project_id, instance=fixtures.sql.instances[0]["name"]
    )
    instances_failover.assert_called_with(
        project=project_id,
        instance=fixtures.sql.instances[0]["name"],
        body=fixtures.sql.failover_body,
    )

    wait_on_operation.assert_called_with(
        ops_svc, project=project_id, operation="mysqlfailover", frequency=10
    )


@patch("chaosgcp.sql.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_export_data(Credentials, service_builder, wait_on_operation):
    project_id = fixtures.configuration["gcp_project_id"]
    instance_id = fixtures.sql.instances[0]["name"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    instances_svc = MagicMock()
    service.instances.return_value = instances_svc
    _export_data = MagicMock()
    instances_svc.export = _export_data
    _export_data.return_value.execute.return_value = (
        fixtures.sql.export_operation
    )

    ops_svc = MagicMock()
    service.operations.return_value = ops_svc

    export_data(
        instance_id,
        "gs://chaosiqdemos/dump.sql",
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    _export_data.assert_called_with(
        project=project_id, instance=instance_id, body=ANY
    )

    wait_on_operation.assert_called_with(
        ops_svc, project=project_id, operation="mysqlexport"
    )


@patch("chaosgcp.sql.actions.wait_on_operation", autospec=False)
@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_import_data(Credentials, service_builder, wait_on_operation):
    project_id = fixtures.configuration["gcp_project_id"]
    instance_id = fixtures.sql.instances[0]["name"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    instances_svc = MagicMock()
    service.instances.return_value = instances_svc
    _import_data = MagicMock()
    instances_svc.import_ = _import_data
    _import_data.return_value.execute.return_value = (
        fixtures.sql.import_operation
    )

    ops_svc = MagicMock()
    service.operations.return_value = ops_svc

    import_data(
        instance_id,
        "gs://chaosiqdemos/dump.sql",
        "demo",
        import_user="chaosiq",
        project_id=project_id,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    _import_data.assert_called_with(
        project=project_id, instance=instance_id, body=ANY
    )

    wait_on_operation.assert_called_with(
        ops_svc, project=project_id, operation="mysqlimport"
    )


@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_list_databases(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]
    instance_id = fixtures.sql.instances[0]["name"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    databases_svc = MagicMock()
    service.databases.return_value = databases_svc
    _list_databases = MagicMock()
    databases_svc.list = _list_databases
    _list_databases_resp = {"items": fixtures.sql.databases}
    _list_databases.return_value.execute.return_value = _list_databases_resp

    response = list_databases(
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
        instance_id=instance_id,
    )
    databases = response["databases"]
    assert len(databases) == 2
    assert [db["name"] for db in databases] == ["postgres", "chaos"]

    _list_databases.assert_called_with(project=project_id, instance=instance_id)


@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_describe_database(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]
    instance_id = fixtures.sql.instances[0]["name"]
    database_name = fixtures.sql.databases[1]["name"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    databases_svc = MagicMock()
    service.databases.return_value = databases_svc
    databases_get = MagicMock()
    databases_svc.get = databases_get
    databases_get.return_value.execute.return_value = fixtures.sql.databases[1]

    describe_database(
        instance_id,
        database_name,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )

    databases_get.assert_called_with(
        project=project_id, instance=instance_id, database=database_name
    )
