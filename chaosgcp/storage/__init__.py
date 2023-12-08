# -*- coding: utf-8 -*-

from chaoslib.types import Configuration, Secrets
from google.cloud import storage as gc_storage

from chaosgcp import get_context, load_credentials

__all__ = ["client"]


def client(
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Create a client for Google Cloud Storage
    """
    ctx = get_context(
        configuration=configuration, project_id=project_id, region=region
    )
    credentials = load_credentials(secrets=secrets)
    return gc_storage.Client(project=ctx.project_id, credentials=credentials)
