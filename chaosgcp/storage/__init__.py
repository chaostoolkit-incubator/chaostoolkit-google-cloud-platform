# -*- coding: utf-8 -*-

from chaoslib.types import Configuration, Secrets
from google.cloud import storage as gc_storage

from chaosgcp import get_context, load_credentials

__all__ = ["client"]


def client(configuration: Configuration = None, secrets: Secrets = None):
    """
    Create a client for Google Cloud Storage
    """
    ctx = get_context(configuration=configuration, secrets=secrets)
    credentials = load_credentials(secrets=secrets)
    return gc_storage.Client(project=ctx.project_id, credentials=credentials)
