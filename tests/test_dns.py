from unittest.mock import MagicMock, patch

import fixtures

from chaosgcp.dns.actions import update_service


@patch("chaosgcp.build", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_update_service(Credentials, dns_client):
    project_id = fixtures.configuration["gcp_project_id"]
    zone_name = "plsqlzone"
    name = "8144911341bc.38ftc5jekg33w.us-central1.sql.goog."
    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    dns_client.return_value = service

    recordsets_svc = MagicMock()
    recordsets_patch = MagicMock()

    recordsets_patch.execute.return_value = fixtures.dns.response
    recordsets_svc.patch.return_value = recordsets_patch
    service.resourceRecordSets.return_value = recordsets_svc

    response = update_service(
        name=name,
        zone_name=zone_name,
        ip_address="10.2.0.6",
        secrets=fixtures.secrets,
        project=project_id,
    )

    assert response["type"] == "A"