# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from googleapiclient import discovery

from chaosgcp import load_credentials

__all__ = ["update_service"]


def update_service(
    secrets: Secrets = None,
    project: str = None,
    managed_zone: str = None,
    ip_address: str="10.0.0.6",
    name: str="b2e453371f40.34gubvy95ghwe.us-central1.sql.goog.",
    zone_name: str="pscsqlzone"):

    credentials = load_credentials(secrets)

    service = discovery.build('dns', 'v1', credentials=credentials)

    # Project ID for this request.
    project = project  # TODO(developer): Update placeholder value.

    # The name of the zone for this request.
    managed_zone = zone_name  # TODO(developer): Update placeholder value.

    dns_record_body = {
        # TODO(developer): Update kind placeholder value.
        'kind': 'dns#resourceRecordSet',
        # TODO(developer): Update name placeholder value.
        'name': name,
        # TODO(developer): Update rrdatas placeholder values.
        'rrdatas': [ip_address],
        # TODO(developer): Update ttl placeholder value.
        'ttl': 5,
        # TODO(developer): Update type placeholder value.
        'type': 'A'
    }

    request = service.resourceRecordSets().patch(
        project=project,
        managedZone=managed_zone,
        # TODO(developer): Update name placeholder value.
        name=name,
        # TODO(developer): Update type placeholder value.
        type='A',
        body=dns_record_body
        )

    response = request.execute()

    return response.__class__.to_dict(response)
