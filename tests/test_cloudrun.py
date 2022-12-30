from unittest.mock import MagicMock, patch

import fixtures

from chaosgcp.cloudrun.actions import run_v2


@patch("chaosgcp.cloudrun.actions.run_v2.ServicesClient", autospec=True)
@patch("chaosgcp.cloudrun.actions.run_v2.UpdateServiceRequest", autospec=True)
@patch("chaosgcp.cloudrun.actions.run_v2.RevisionTemplate", autospec=True)
@patch("chaosgcp.cloudrun.actions.run_v2.Service", autospec=True)
def test_update_service(service, tpl, request, client):
    credentials = MagicMock()
    credentials.load_credentials.return_value = MagicMock()

    client.return_value = MagicMock()

    service_name = "a-dummy-service"
    parent = (
        f"projects/{fixtures.configuration['gcp_project_id']}"
        f"/locations/{fixtures.configuration['gcp_zone']}"
        f"/services/{service_name}"
    )

    tpl.return_value = run_v2.RevisionTemplate(
        max_instance_request_concurrency=fixtures.cloudrun.max_instances,
        service_account=fixtures.cloudrun.service_account,
        encryption_key=fixtures.cloudrun.encryption_key,
        containers=fixtures.cloudrun.containers,
        vpc_access=fixtures.cloudrun.vpc_access,
    )

    tpl.assert_called_with(
        max_instance_request_concurrency=fixtures.cloudrun.max_instances,
        service_account=fixtures.cloudrun.service_account,
        encryption_key=fixtures.cloudrun.encryption_key,
        containers=fixtures.cloudrun.containers,
        vpc_access=fixtures.cloudrun.vpc_access,
    )

    service.return_value = run_v2.Service(
        name=parent,
        labels=fixtures.cloudrun.labels,
        template=tpl,
        traffic=fixtures.cloudrun.traffics,
    )

    service.assert_called_with(
        name=parent,
        labels=fixtures.cloudrun.labels,
        template=tpl,
        traffic=fixtures.cloudrun.traffics,
    )

    request.return_value = run_v2.UpdateServiceRequest(
        name=parent,
        template=fixtures.cloudrun.template,
        traffic=fixtures.cloudrun.traffics,
    )

    request.assert_called_with(
        name=parent,
        template=fixtures.cloudrun.template,
        traffic=fixtures.cloudrun.traffics,
    )

    client.update_service(request)
