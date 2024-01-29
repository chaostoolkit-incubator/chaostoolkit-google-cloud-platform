# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, patch

import fixtures

from unittest.mock import MagicMock, patch

import fixtures

from chaosgcp.compute.actions import compute_v1
from chaosgcp.compute.actions import set_instance_tags

@patch("chaosgcp.compute.actions.compute_v1.types.Tags", autospec=True)
@patch("chaosgcp.compute.actions.compute_v1.SetTagsInstanceRequest", autospec=True)
@patch("chaosgcp.compute.actions.compute_v1.GetInstanceRequest", autospec=True)
@patch("chaosgcp.compute.actions.compute_v1.InstancesClient", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)

def test_set_instance_tags(Credentials,client,instance_req,settag_req,tags):
    project_id = fixtures.configuration["gcp_project_id"]
    zone_name = fixtures.configuration["gcp_zone"]
    instance_name = "test_instance"
    tags_list=["test"]

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()
    

    instance_req.return_value=compute_v1.GetInstanceRequest(instance=instance_name, project=project_id,zone=zone_name)
    instance_req.assert_called_with(instance=instance_name, project=project_id,zone=zone_name)
    client.get.return_value=fixtures
    settag_req.return_value=compute_v1.SetTagsInstanceRequest(instance=instance_name,
        project=project_id,
        zone=zone_name,
        tags_resource=tags(fingerprint=fixtures.compute.response_get["tags"]["fingerprint"],items=tags_list))
    settag_req.assert_called_with(instance=instance_name, project=project_id,zone=zone_name,tags_resource=tags(fingerprint=fixtures.compute.response_get["tags"]["fingerprint"],items=tags_list))
    
    client.set_tags.return_value = compute_v1.Operation(name="op1")
    client.set_tags(settag_req)
   