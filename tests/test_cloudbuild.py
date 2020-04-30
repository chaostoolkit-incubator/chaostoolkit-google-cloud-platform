# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch, ANY

from chaosgcp.sql.actions import trigger_failover, export_data, import_data
from chaosgcp.sql.probes import list_instances, describe_instance, \
    list_databases, describe_database
from chaosgcp.cloudbuild.actions import run_trigger
from chaosgcp.cloudbuild.probes import list_triggers, list_trigger_names, \
    get_trigger

import fixtures



@patch('chaosgcp.build', autospec=True)
@patch('chaosgcp.Credentials', autospec=True)
def test_list_triggers(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    projects_svc = MagicMock()
    triggers_svc = MagicMock()
    triggers_list = MagicMock()

    triggers_list.return_value.execute.return_value = fixtures.cloudbuild.triggers
    triggers_svc.list = triggers_list
    projects_svc.triggers.return_value = triggers_svc
    service.projects.return_value = projects_svc

    response = list_triggers(
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    triggers_list.assert_called_with(projectId=project_id)

    assert "triggers" in response
    assert len(response["triggers"]) == 1


#
# def test_list_trigger_names():
#     names
#     assert names == ["a-dummy-trigger"]


@patch('chaosgcp.build', autospec=True)
@patch('chaosgcp.Credentials', autospec=True)
def test_list_trigger_names(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    projects_svc = MagicMock()
    triggers_svc = MagicMock()
    triggers_list = MagicMock()

    triggers_list.return_value.execute.return_value = fixtures.cloudbuild.triggers
    triggers_svc.list = triggers_list
    projects_svc.triggers.return_value = triggers_svc
    service.projects.return_value = projects_svc

    response = list_trigger_names(
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    triggers_list.assert_called_with(projectId=project_id)

    assert response == ["a-dummy-trigger"]


@patch('chaosgcp.build', autospec=True)
@patch('chaosgcp.Credentials', autospec=True)
def test_get_trigger(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]
    trigger_name = "a-dummy-trigger"

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    projects_svc = MagicMock()
    triggers_svc = MagicMock()
    triggers_get = MagicMock()

    triggers_get.return_value.execute.return_value = fixtures.cloudbuild.trigger
    triggers_svc.get = triggers_get
    projects_svc.triggers.return_value = triggers_svc
    service.projects.return_value = projects_svc

    response = get_trigger(
        name=trigger_name,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    triggers_get.assert_called_with(projectId=project_id, triggerId=trigger_name)
    assert response["name"] == trigger_name




@patch('chaosgcp.build', autospec=True)
@patch('chaosgcp.Credentials', autospec=True)
def test_run_trigger(Credentials, service_builder):
    project_id = fixtures.configuration["gcp_project_id"]
    trigger_name = "a-dummy-trigger"
    source = {"branchName": "master"}

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    projects_svc = MagicMock()
    triggers_svc = MagicMock()
    triggers_run = MagicMock()

    triggers_run.return_value.execute.return_value = fixtures.cloudbuild.triggered_build
    triggers_svc.run = triggers_run
    projects_svc.triggers.return_value = triggers_svc
    service.projects.return_value = projects_svc

    response = run_trigger(
        name=trigger_name,
        source=source,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    triggers_run.assert_called_with(projectId=project_id, triggerId=trigger_name, body=source)
    assert response["metadata"]["build"]["status"] == "QUEUED"
