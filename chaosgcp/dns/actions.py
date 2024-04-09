"""DNS A record update.

This file has the function to update the DNS A record for testing the DNS changes may effect the working flow

Typical usage example in an experiment json file:

  "module": "chaosgcp.dns.actions",
  "func": "update_service",
"""

# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaosgcp import client

from chaoslib.types import Configuration, Secrets

__all__ = ["update_dns_record"]


def update_dns_record(
    project_id: str,
    ip_address: str,
    name: str,
    zone_name: str,
    kind: str = "dns#resourceRecordSet",
    ttl: int = 5,
    record_type: str = "A",
    existing_type: str = "A",
    secrets: Secrets = None,
    configuration: Configuration = None,
) -> Dict[str, Any]:
  """Updates the DNS A record entry, It cannot be undone.

  Args:
      project_id : the project ID in which the DNS record is present
      ip_address: the IP address for the A record that needs to be changed
      name: the name of the dns record entry 
      zone_name: the name of the dns zone name which needs to be changed
      kind : the type of dns record set
      ttl: time to live for dns record change 
      record_type: the record type for the name
      existing_type: the existing type of record 
      secrets: authorization token
  Returns:
      JSON Response which is in form of dictionary
  """
  service = client("dns", "v1", secrets=secrets)

  dns_record_body = {
      "kind": kind,
      "name": name,
      "rrdatas": [ip_address],
      "ttl": ttl,
      "type": record_type,
  }

  request = service.resourceRecordSets().patch(
      project=project_id,
      managedZone=zone_name,
      name=name,
      type=existing_type,
      body=dns_record_body,
  )
  
  try:
    response = request.execute()
  except Exception as e:
    print("Exception occurred: "+ str(e))
    return {}

  return response.__class__.to_dict(response)
