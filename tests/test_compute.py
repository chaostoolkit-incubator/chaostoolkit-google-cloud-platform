from unittest.mock import MagicMock, patch

import fixtures

from chaosgcp.compute.actions import compute_v1

@patch("chaosgcp.compute.actions.compute_v1.types.Tags", autospec=True)
@patch("chaosgcp.compute.actions.compute_v1.SetTagsInstanceRequest", autospec=True)
@patch("chaosgcp.compute.actions.compute_v1.GetInstanceRequest", autospec=True)
@patch("chaosgcp.compute.actions.compute_v1.InstancesClient", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)

def test_set_instance_tags(credentials,client,instance_req,settag_req,tags):
    project_id = fixtures.configuration["gcp_project_id"]
    zone_name = "us-central1-a"
    instance_name = "test_instance"
    tags_list=["test"]

    client.return_value = MagicMock()
    credentials = MagicMock()
    credentials.load_credentials.return_value = MagicMock()

    instance_req.return_value=compute_v1.GetInstanceRequest(instance=instance_name, project=project_id,zone=zone_name)
    instance_req.assert_called_with(instance=instance_name, project=project_id,zone=zone_name)
    client.get.return_value=fixtures.compute.response_get

    settag_req.return_value=compute_v1.SetTagsInstanceRequest(instance=instance_name,
        project=project_id,
        zone=zone_name,
        tags_resource=tags(fingerprint=fixtures.compute.response_get["tags"]["fingerprint"],items=tags_list))
    settag_req.assert_called_with(instance=instance_name, project=project_id,zone=zone_name,tags_resource=tags(fingerprint=fixtures.compute.response_get["tags"]["fingerprint"],items=tags_list))
   