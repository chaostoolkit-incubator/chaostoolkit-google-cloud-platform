# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1

from chaosgcp import get_context, load_credentials, wait_on_extended_operation
from chaosgcp.lb import get_path_matcher


__all__ = ["get_backend_service_health", "get_fault_injection_traffic_policy"]
logger = logging.getLogger("chaostoolkit")


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


def get_fault_injection_traffic_policy(
    url_map: str,
    target_name: str,
    target_path: str = "/*",
    regional: bool = False,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get the fault injection policy from url map at a given path.

    The `target_name` argument is the the name of a path matcher in the
    URL map. The `target_path` argument is the path within the path matcher.
    Be sure to put the exact one you are targeting.

    For instance:

    ```json
    {
        "type: "probe",
        "name": "get-fault-injection-policy",
        "provider": {
            "type": "python",
            "module": "chaosgcp.lb.probes",
            "func": "get_fault_injection_traffic_policy",
            "arguments": {
                "url_map": "demo-urlmap",
                "target_name": "allpaths",
                "target_path": "/*",
            }
        }
    }
    ```

    Set `regional` to talk to a regional LB.

    See: https://cloud.google.com/load-balancing/docs/l7-internal/setting-up-traffic-management#configure_fault_injection
    """  # noqa: E501
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)

    region = context.region
    project = context.project_id

    if regional:
        if not region:
            raise ActivityFailed(
                "when `regional` is set, the `gcp_region` configuration key "
                "must also be set"
            )
        client = compute_v1.RegionUrlMapsClient(credentials=credentials)
        request = compute_v1.GetRegionUrlMapRequest(
            project=project,
            url_map=url_map,
            region=region,
        )
    else:
        client = compute_v1.UrlMapsClient(credentials=credentials)
        request = compute_v1.GetUrlMapRequest(
            project=project,
            url_map=url_map,
        )

    urlmap = client.get(request=request)

    found_pr = get_path_matcher(urlmap, target_name, target_path)

    fault = found_pr.route_action.fault_injection_policy

    if regional:
        request = compute_v1.UpdateRegionUrlMapRequest(
            project=project,
            url_map=url_map,
            url_map_resource=urlmap,
            region=region,
        )
    else:
        request = compute_v1.UpdateUrlMapRequest(
            project=project,
            url_map=url_map,
            url_map_resource=urlmap,
        )

    operation = client.update(request=request)
    wait_on_extended_operation(operation=operation)

    return fault.__class__.to_dict(fault)
