# Copyright 2023 Google LLC.
# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets

from chaosgcp import client

__all__ = ["update_dns_A_record"]


def update_dns_A_record(
    project: str ,
    ip_address: str ,
    name: str ,
    zone_name: str,
    kind: str = "dns#resourceRecordSet",
    ttl: int = 5,
    record_type: str = "A",
    existing_type: str = "A",
    secrets: Secrets = None,
) -> Dict[str, Any]:
    
    """ 
    Updates the DNS A record entry, It cannot be undone
    :param project : the project ID in which the DNS record is present
    :param ip_address: the IP address for the A record that needs to be changed
    :param name: the name of the dns record entry 
    :param zone_name: the name of the dns zone name which needs to be changed
    :param kind : the type of dns record set
    :param ttl: time to live for dns record change 
    :param record_type: the record type for the name

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
        project=project,
        managedZone=zone_name,
        name=name,
        type=existing_type,
        body=dns_record_body,
    )

    response = request.execute()

    return response