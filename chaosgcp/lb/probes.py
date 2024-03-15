# -*- coding: utf-8 -*-
from typing import Any, Dict, List

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
) -> List[Dict[str, Any]]:
    """
    Fetch the latest health check result of the given backend service.

    See also: https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.backend_services.BackendServicesClient#google_cloud_compute_v1_services_backend_services_BackendServicesClient_get_health
    """  # noqa: E501
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)

    region = context.region
    project = context.project_id

    health_per_group = []

    client = compute_v1.BackendServicesClient(credentials=credentials)

    request = compute_v1.GetBackendServiceRequest(
        backend_service=backend_service,
        project=project,
    )
    svc = client.get(request=request)

    if region:
        client = compute_v1.RegionBackendServicesClient(credentials=credentials)

        for backend in svc.backends:
            neg = backend.group

            request = compute_v1.GetHealthRegionBackendServiceRequest(
                backend_service=backend_service,
                project=project,
                region=region,
                resource_group_reference_resource=compute_v1.ResourceGroupReference(
                    group=neg
                ),
            )
            response = client.get_health(request=request)
            health_per_group.append(response.__class__.to_dict(response))
    else:
        client = compute_v1.BackendServicesClient(credentials=credentials)

        for backend in svc.backends:
            neg = backend.group

            request = compute_v1.GetHealthBackendServiceRequest(
                backend_service=backend_service,
                project=project,
                resource_group_reference_resource=compute_v1.ResourceGroupReference(
                    group=neg
                ),
            )
            response = client.get_health(request=request)
            health_per_group.append(response.__class__.to_dict(response))

    return health_per_group
