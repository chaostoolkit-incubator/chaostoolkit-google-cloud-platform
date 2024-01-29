# Copyright 2023 Google LLC.
from typing import Any, Dict

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1
from google.cloud.compute_v1.types import Tags
from logzero import logger

from chaosgcp import get_context, load_credentials, wait_on_extended_operation

__all__ =["set_instance_tags"]

def set_instance_tags(project_id:str, zone:str,instance_name: str,tags_list: list, configuration: Configuration = None,
                              secrets: Secrets = None) -> Dict[str, Any]:
    
    credentials = load_credentials(secrets)
    ctx = get_context(configuration, secrets)
    # Create a client
    client = compute_v1.InstancesClient()
    
    request = compute_v1.GetInstanceRequest(
        instance=instance_name,
        project=project_id,
        zone=zone,
    )

    # Make the request
    response = client.get(request=request)

    fgp=response.tags.fingerprint

    # Initialize request argument(s)
    request = compute_v1.SetTagsInstanceRequest(
        instance=instance_name,
        project=project_id,
        zone=zone,
        tags_resource=Tags(fingerprint=fgp,items=tags_list)
                
    )

    # Make the request
    operation = client.set_tags(request=request)

    # Handle the response
    wait_on_extended_operation(operation)
