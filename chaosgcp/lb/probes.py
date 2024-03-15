# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1

from chaosgcp import get_context, load_credentials

__all__ = [
    "get_backend_service_health",
]


def get_backend_service_health(
    backend_service: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Fetch the latest health check result of the given backend service

    See also: https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.backend_services.BackendServicesClient#google_cloud_compute_v1_services_backend_services_BackendServicesClient_get_health
    """  # noqa: E501
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)

    region = context.region
    project = context.project_id

    client = compute_v1.BackendServicesClient(credentials=credentials)

    request = compute_v1.GetHealthBackendServiceRequest(
        backend_service=backend_service,
        project=project,
    )

    response = client.get_health(request=request)

    return response.__class__.to_dict(response)
