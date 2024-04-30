# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1
from google.cloud.compute_v1.types import Tags

from chaosgcp import load_credentials, wait_on_extended_operation, to_dict

__all__ = ["set_instance_tags"]
logger = logging.getLogger("chaostoolkit")


def set_instance_tags(
    project_id: str,
    zone: str,
    instance_name: str,
    tags_list: list,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """Set a Network Tags to a GCE VM instance

    :param project_id : the project ID in which the DNS record is present
    :param ip_address: the IP address for the A record that needs to be changed
    :param zone: the name of the zone where the GCE VM is provisioned
    :param tags_list : list of network tags to be set to the GCE VM instance
    :return JSON Response which is in form of dictionary
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
    wait_on_extended_operation(operation)

    response = operation.result()

    return to_dict(response)
