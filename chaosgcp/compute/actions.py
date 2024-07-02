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

import logging
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1
from google.cloud.compute_v1.types import Tags

from chaosgcp import load_credentials, wait_on_extended_operation

__all__ = ["set_instance_tags"]
logger = logging.getLogger("chaostoolkit")


def set_instance_tags(
    project_id: str,
    zone: str,
    instance_name: str,
    tags_list: list,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """Set a Network Tags to a GCE VM instance

    :param project_id : the project ID in which the DNS record is present
    :param ip_address: the IP address for the A record that needs to be changed
    :param zone: the name of the zone where the GCE VM is provisioned
    :param tags_list : list of network tags to be set to the GCE VM instance
    :return nothing
    """
    credentials = load_credentials(secrets)

    # Create a client
    client = compute_v1.InstancesClient(credentials=credentials)

    request = compute_v1.GetInstanceRequest(
        instance=instance_name,
        project=project_id,
        zone=zone,
    )

    # Make the request
    response = client.get(request=request)

    fgp = response.tags.fingerprint

    # Initialize request argument(s)
    request = compute_v1.SetTagsInstanceRequest(
        instance=instance_name,
        project=project_id,
        zone=zone,
        tags_resource=Tags(fingerprint=fgp, items=tags_list),
    )

    # Make the request
    operation = client.set_tags(request=request)

    # Handle the response
    # do not return anything as extended operations do not carry a payload
    wait_on_extended_operation(operation)


def suspend_vm_instance(
    project_id: str, zone: str, instance_name: str, secrets: Secrets = None
):
    """
    Suspend a GCE VM instance

    :param project_id : the project ID in which the GCE VM is present
    :param zone: the name of the zone where the GCE VM is present
    :param instance_name : the name of the GCE VM to be suspended
    """

    credentials = load_credentials(secrets)

    # Create a client
    client = compute_v1.InstancesClient(credentials=credentials)

    # Make the request to delete
    operation = client.suspend(
        project=project_id, zone=zone, instance=instance_name
    )

    wait_on_extended_operation(operation)

    if operation.error_code:
        logger.error(
            f"Error during instance suspension: [Code: {operation.error_code}]: {operation.error_message}"
        )
    else:
        logger.info("Instance suspended successfully")


def resume_vm_instance(
    project_id: str, zone: str, instance_name: str, secrets: Secrets = None
) -> Dict[str, Any]:
    """
    Resume a suspended GCE VM instance

    :param project_id : the project ID in which the GCE VM is present
    :param zone: the name of the zone where the GCE VM is present
    :param instance_name : the name of the GCE VM to be resumed
    """

    credentials = load_credentials(secrets)

    client = compute_v1.InstancesClient(credentials=credentials)

    operation = client.resume(
        project=project_id, zone=zone, instance=instance_name
    )

    wait_on_extended_operation(operation)

    if operation.error_code:
        logger.error(
            f"Error during instance resumption: [Code: {operation.error_code}]: {operation.error_message}"
        )
    else:
        logger.info("Instance resumed successfully")
