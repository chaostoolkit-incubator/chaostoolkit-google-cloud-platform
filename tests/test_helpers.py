# -*- coding: utf-8 -*-
from unittest.mock import MagicMock

import fixtures

from chaosgcp import wait_on_operation


def test_wait_on_operation_kwargs():
    """
    Test this helper function can be called with various arguments
    depending on the `operation service` signature from GCE's API
    """
    ops_svc = MagicMock()
    ops_svc.get().execute.return_value = {"status": "DONE"}

    # case 1
    response = wait_on_operation(
        ops_svc,
        projectId=fixtures.configuration["gcp_project_id"],
        zone=fixtures.configuration["gcp_zone"],
        operationId="operation-xyz",
    )

    ops_svc.get.assert_called_with(
        projectId=fixtures.configuration["gcp_project_id"],
        zone=fixtures.configuration["gcp_zone"],
        operationId="operation-xyz",
    )
    assert response["status"] == "DONE"

    # case 2
    response = wait_on_operation(
        ops_svc,
        project=fixtures.configuration["gcp_project_id"],
        operation="operation-xyz",
    )

    ops_svc.get.assert_called_with(
        project=fixtures.configuration["gcp_project_id"],
        operation="operation-xyz",
    )
    assert response["status"] == "DONE"
