# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1

from chaosgcp import (
    get_context,
    load_credentials,
    wait_on_extended_operation,
)
from chaosgcp.lb import (
    get_fault_injection_policy,
    remove_fault_injection_policy,
    get_fault_injection_policy_from_url,
)

__all__ = [
    "inject_traffic_delay",
    "inject_traffic_faults",
    "remove_fault_injection_traffic_policy",
    "add_latency_to_endpoint",
    "remove_latency_from_endpoint",
    "set_status_code_on_endpoint",
    "reset_status_code_on_endpoint",
]
logger = logging.getLogger("chaostoolkit")


def inject_traffic_delay(
    url_map: str,
    target_name: str,
    target_path: str = "/*",
    impacted_percentage: float = 50.0,
    delay_in_seconds: int = 1,
    delay_in_nanos: int = 0,
    regional: bool = False,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Add/set delay for a percentage of requests going through a url map on
    a given path.

    This will not work with classic LB.

    Note also, that the LB may be slow to reflect the change. It can take
    up to a couple of minutes from our experience before it propagates
    accordingly.

    The `target_name` argument is the the name of a path matcher in the
    URL map. The `target_path` argument is the path within the path matcher.
    Be sure to put the exact one you are targeting.

    This action supports looking into path rules as well as route rules
    (with prefix match, full path match or regex match).

    For instance:

    ```json
    {
        "type: "action",
        "name": "add-delay-to-home-page",
        "provider": {
            "type": "python",
            "module": "chaosgcp.lb.actions",
            "func": "inject_traffic_delay",
            "arguments": {
                "url_map": "demo-urlmap",
                "target_name": "allpaths",
                "target_path": "/*",
                "impacted_percentage": 75.0,
                "delay_in_seconds": 3,
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

    fip = get_fault_injection_policy(urlmap, target_name, target_path)

    fip.delay.percentage = float(impacted_percentage)
    fip.delay.fixed_delay.seconds = int(delay_in_seconds)
    fip.delay.fixed_delay.nanos = int(delay_in_nanos)

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

    return urlmap.__class__.to_dict(urlmap)


def inject_traffic_faults(
    url_map: str,
    target_name: str,
    target_path: str = "/*",
    impacted_percentage: float = 50.0,
    http_status: int = 400,
    regional: bool = False,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Add/set HTTP status codes for a percentage of requests going through a
    url map on a given path.

    Note also, that the LB may be slow to reflect the change. It can take
    up to a couple of minutes from our experience before it propagates
    accordingly.

    The `target_name` argument is the the name of a path matcher in the
    URL map. The `target_path` argument is the path within the path matcher.
    Be sure to put the exact one you are targeting.

    For instance:

    ```json
    {
        "type: "action",
        "name": "return-503-from-home-page",
        "provider": {
            "type": "python",
            "module": "chaosgcp.lb.actions",
            "func": "inject_traffic_faults",
            "arguments": {
                "url_map": "demo-urlmap",
                "target_name": "allpaths",
                "target_path": "/*",
                "impacted_percentage": 75.0,
                "http_status": 503,
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

    fip = get_fault_injection_policy(urlmap, target_name, target_path)

    fip.abort.percentage = float(impacted_percentage)
    fip.abort.http_status = http_status

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

    return urlmap.__class__.to_dict(urlmap)


def remove_fault_injection_traffic_policy(
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
    Remove any fault injection policy from url map on a given path.

    The `target_name` argument is the the name of a path matcher in the
    URL map. The `target_path` argument is the path within the path matcher.
    Be sure to put the exact one you are targeting.

    For instance:

    ```json
    {
        "type: "action",
        "name": "remove-fault-injection-policy",
        "provider": {
            "type": "python",
            "module": "chaosgcp.lb.actions",
            "func": "remove_fault_injection_traffic_policy",
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

    remove_fault_injection_policy(urlmap, target_name, target_path)

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

    return urlmap.__class__.to_dict(urlmap)


def add_latency_to_endpoint(
    url: str,
    latency: float = 0.3,
    percentage: float = 90.0,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Add latency to a particular URL.

    This is a high level shortcut to the `inject_traffic_delay` which
    infers all the appropriate parameters from the URL itself. It does this
    by querying the GCP project for all LB information and matches the
    correct target from there.

    This might no work on all combinaison of Load Balancer and backend
    services that GCP support but should work well with LB + Cloud Run.

    The `latency` is expressed in seconds with a default set to 0.3 seconds.
    """
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)

    region = context.region
    project = context.project_id

    if region:
        if not region:
            raise ActivityFailed(
                "when `regional` is set, the `gcp_region` configuration key "
                "must also be set"
            )
        client = compute_v1.RegionUrlMapsClient(credentials=credentials)
        request = compute_v1.ListRegionUrlMapsRequest(
            project=project,
            region=region,
        )
    else:
        client = compute_v1.UrlMapsClient(credentials=credentials)
        request = compute_v1.ListUrlMapsRequest(
            project=project,
        )

    urlmaps = client.list(request=request)
    url_map, route_action = get_fault_injection_policy_from_url(urlmaps, url)

    urlmap_name = url_map.name
    fip = route_action.fault_injection_policy
    fip.delay.percentage = float(percentage)
    fip.delay.fixed_delay.seconds = 0
    fip.delay.fixed_delay.nanos = int(latency * 1e9)

    if region:
        request = compute_v1.UpdateRegionUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
            region=region,
        )
    else:
        request = compute_v1.UpdateUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
        )

    operation = client.update(request=request)
    wait_on_extended_operation(operation=operation)

    return url_map.__class__.to_dict(url_map)


def remove_latency_from_endpoint(
    url: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Remove latency from a particular URL.

    This is a high level shortcut to the
    `remove_fault_injection_traffic_policy` which infers all the appropriate
    parameters from the URL itself. It does this by querying the GCP project
    for all LB information and matches the correct target from there.
    """
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)

    region = context.region
    project = context.project_id

    if region:
        if not region:
            raise ActivityFailed(
                "when `regional` is set, the `gcp_region` configuration key "
                "must also be set"
            )
        client = compute_v1.RegionUrlMapsClient(credentials=credentials)
        request = compute_v1.ListRegionUrlMapsRequest(
            project=project,
            region=region,
        )
    else:
        client = compute_v1.UrlMapsClient(credentials=credentials)
        request = compute_v1.ListUrlMapsRequest(
            project=project,
        )

    urlmaps = client.list(request=request)

    url_map, route_action = get_fault_injection_policy_from_url(urlmaps, url)

    urlmap_name = url_map.name
    route_action.fault_injection_policy = None

    if region:
        request = compute_v1.UpdateRegionUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
            region=region,
        )
    else:
        request = compute_v1.UpdateUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
        )

    operation = client.update(request=request)
    wait_on_extended_operation(operation=operation)

    return url_map.__class__.to_dict(url_map)


def set_status_code_on_endpoint(
    url: str,
    status_code: int = 400,
    percentage: float = 90.0,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Set the status code on a particular URL.

    This is a high level shortcut to the `inject_traffic_faults` which
    infers all the appropriate parameters from the URL itself. It does this
    by querying the GCP project for all LB information and matches the
    correct target from there.

    This might no work on all combinaison of Load Balancer and backend
    services that GCP support but should work well with LB + Cloud Run.
    """
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)

    region = context.region
    project = context.project_id

    if region:
        if not region:
            raise ActivityFailed(
                "when `regional` is set, the `gcp_region` configuration key "
                "must also be set"
            )
        client = compute_v1.RegionUrlMapsClient(credentials=credentials)
        request = compute_v1.ListRegionUrlMapsRequest(
            project=project,
            region=region,
        )
    else:
        client = compute_v1.UrlMapsClient(credentials=credentials)
        request = compute_v1.ListUrlMapsRequest(
            project=project,
        )

    urlmaps = client.list(request=request)

    url_map, route_action = get_fault_injection_policy_from_url(urlmaps, url)

    urlmap_name = url_map.name
    fip = route_action.fault_injection_policy
    fip.abort.percentage = float(percentage)
    fip.abort.http_status = status_code

    if region:
        request = compute_v1.UpdateRegionUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
            region=region,
        )
    else:
        request = compute_v1.UpdateUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
        )

    operation = client.update(request=request)
    wait_on_extended_operation(operation=operation)

    return url_map.__class__.to_dict(url_map)


def reset_status_code_on_endpoint(
    url: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Remove the status code set on an endpoint

    This is a high level shortcut to the
    `remove_fault_injection_traffic_policy` which infers all the appropriate
    parameters from the URL itself. It does this by querying the GCP project
    for all LB information and matches the correct target from there.
    """
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)

    region = context.region
    project = context.project_id

    if region:
        if not region:
            raise ActivityFailed(
                "when `regional` is set, the `gcp_region` configuration key "
                "must also be set"
            )
        client = compute_v1.RegionUrlMapsClient(credentials=credentials)
        request = compute_v1.ListRegionUrlMapsRequest(
            project=project,
            region=region,
        )
    else:
        client = compute_v1.UrlMapsClient(credentials=credentials)
        request = compute_v1.ListUrlMapsRequest(
            project=project,
        )

    urlmaps = client.list(request=request)

    url_map, route_action = get_fault_injection_policy_from_url(urlmaps, url)

    urlmap_name = url_map.name
    route_action.fault_injection_policy = None

    if region:
        request = compute_v1.UpdateRegionUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
            region=region,
        )
    else:
        request = compute_v1.UpdateUrlMapRequest(
            project=project,
            url_map=urlmap_name,
            url_map_resource=url_map,
        )

    operation = client.update(request=request)
    wait_on_extended_operation(operation=operation)

    return url_map.__class__.to_dict(url_map)
