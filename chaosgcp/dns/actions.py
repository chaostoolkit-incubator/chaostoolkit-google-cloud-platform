# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from chaosgcp import client

from chaosgcp import load_credentials

__all__ = ["update_service"]


def update_service(
    secrets: Secrets = None,
    project: str = None,
    ip_address: str= None,
    name: str= None,
    zone_name: str= None,
    kind: str= "dns#resourceRecordSet",
    ttl: int=5,
    record_type: str="A",
    existing_type: str="A"):

    credentials = load_credentials(secrets)

    service = client('dns', 'v1', credentials=credentials) 

    dns_record_body = {
        'kind': kind,   
        'name': name,   
        'rrdatas': [ip_address],      
        'ttl': ttl,  
        'type': record_type
    }

    request = service.resourceRecordSets().patch(
        project=project,
        managedZone=zone_name,
        name=name,
        type=existing_type,
        body=dns_record_body
        )

    response = request.execute()

    return response
