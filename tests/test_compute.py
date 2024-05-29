# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import MagicMock, patch
from chaosgcp.compute.actions import compute_v1
import fixtures


@patch("chaosgcp.compute.actions.compute_v1.types.Tags", autospec=True)
@patch(
    "chaosgcp.compute.actions.compute_v1.SetTagsInstanceRequest", autospec=True
)
@patch("chaosgcp.compute.actions.compute_v1.GetInstanceRequest", autospec=True)
@patch("chaosgcp.compute.actions.compute_v1.InstancesClient", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_set_instance_tags(Credentials, client, instance_req, settag_req, tags):
    project_id = fixtures.configuration["gcp_project_id"]
    zone_name = fixtures.configuration["gcp_zone"]
    instance_name = "test_instance"
    tags_list = ["test"]

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()

    instance_req.return_value = compute_v1.GetInstanceRequest(
        instance=instance_name, project=project_id, zone=zone_name
    )
    instance_req.assert_called_with(
        instance=instance_name, project=project_id, zone=zone_name
    )
    client.get.return_value = fixtures
    settag_req.return_value = compute_v1.SetTagsInstanceRequest(
        instance=instance_name,
        project=project_id,
        zone=zone_name,
        tags_resource=tags(
            fingerprint=fixtures.compute.response_get["tags"]["fingerprint"],
            items=tags_list,
        ),
    )
    settag_req.assert_called_with(
        instance=instance_name,
        project=project_id,
        zone=zone_name,
        tags_resource=tags(
            fingerprint=fixtures.compute.response_get["tags"]["fingerprint"],
            items=tags_list,
        ),
    )

    client.set_tags.return_value = compute_v1.Operation(name="op1")
    client.set_tags(settag_req)


@patch("chaosgcp.compute.actions.compute_v1.InstancesClient", autospec=True)
@patch(
    "chaosgcp.compute.actions.compute_v1.SuspendInstanceRequest", autospec=True
)
@patch("chaosgcp.Credentials", autospec=True)
def test_suspend_vm_instance(Credentials, client, suspendvm_req):
    project_id = fixtures.configuration["gcp_project_id"]
    zone_name = fixtures.configuration["gcp_zone"]
    instance_name = "test_instance"

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()

    suspendvm_req.return_value = compute_v1.SuspendInstanceRequest(
        instance=instance_name, project=project_id, zone=zone_name
    )


@patch("chaosgcp.compute.actions.compute_v1.InstancesClient", autospec=True)
@patch(
    "chaosgcp.compute.actions.compute_v1.SuspendInstanceRequest", autospec=True
)
@patch("chaosgcp.Credentials", autospec=True)
def test_resume_vm_instance(Credentials, client, resumevm_req):
    project_id = fixtures.configuration["gcp_project_id"]
    zone_name = fixtures.configuration["gcp_zone"]
    instance_name = "test_instance"

    client.return_value = MagicMock()
    Credentials.from_service_account_file.return_value = MagicMock()

    resumevm_req.return_value = compute_v1.ResumeInstanceRequest(
        instance=instance_name, project=project_id, zone=zone_name
    )
