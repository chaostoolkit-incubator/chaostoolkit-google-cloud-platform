"""Tests for dns functions in the dns/actions.py."""
# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0
from unittest import mock
from chaosgcp.dns.actions import update_dns_a_record
import fixtures


@mock.patch("build", autospec=True)
@mock.patch("credentials", autospec=True)
def test_update_dns_a_record(credentials, dns_client):
  """description of the test_update_dns_a_record.
  
  Args:
    credentials: description of credentials
    dns_client: description of dns
  """
  project_id = fixtures.configuration["gcp_project_id"]
  zone_name = "plsqlzone"
  name = "8144911341bc.38ftc5jekg33w.us-central1.sql.goog."
  credentials.from_service_account_file.return_value = mock.MagicMock()

  service = mock.MagicMock()
  dns_client.return_value = service

  recordsets_svc = mock.MagicMock()
  recordsets_patch = mock.MagicMock()

  recordsets_patch.execute.return_value = fixtures.dns.response
  recordsets_svc.patch.return_value = recordsets_patch
  service.resourceRecordSets.return_value = recordsets_svc

  response = update_dns_a_record(
      name=name,
      zone_name=zone_name,
      ip_address="10.2.0.6",
      secrets=fixtures.secrets,
      project=project_id,
  )

  assert response["type"] == "A"