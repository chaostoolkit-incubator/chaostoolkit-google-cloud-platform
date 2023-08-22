# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1

from chaosgcp import load_credentials, wait_on_extended_operation

__all__ = [
    "inject_traffic_delay",
    "inject_traffic_faults",
    "remove_fault_injection_traffic_policy",
]


def inject_traffic_delay(
    url_map: str,
    target_name: str,
    target_path: str,
    impacted_percentage: float = 50.0,
    delay_in_seconds: int = 1,
    delay_in_nanos: int = 0,
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

    See: https://cloud.google.com/load-balancing/docs/l7-internal/setting-up-traffic-management#configure_fault_injection
    """  # noqa: E501
    credentials = load_credentials(secrets)

    client = compute_v1.UrlMapsClient(credentials=credentials)

    project = credentials.project_id

    request = compute_v1.GetUrlMapRequest(
        project=project,
        url_map=url_map,
    )

    urlmap = client.get(request=request)

    for pm in urlmap.path_matchers:
        if pm.name == target_name:
            for pr in pm.path_rules:
                for p in pr.paths:
                    if p == target_path:
                        fip = pr.route_action.fault_injection_policy
                        fip.delay.percentage = float(impacted_percentage)
                        fip.delay.fixed_delay.seconds = int(delay_in_seconds)
                        fip.delay.fixed_delay.nanos = int(delay_in_nanos)
                        break

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
    target_path: str,
    impacted_percentage: float = 50.0,
    http_status: int = 400,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Add/set HTTP status codes for a percentage of requests going through a
    url map on a given path.

    Note also, that the LB may be slow to reflect the change. It can take
    up to a couple of minutes from our experience before it propagates
    accordingly.

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

    See: https://cloud.google.com/load-balancing/docs/l7-internal/setting-up-traffic-management#configure_fault_injection
    """  # noqa: E501
    credentials = load_credentials(secrets)

    client = compute_v1.UrlMapsClient(credentials=credentials)

    project = credentials.project_id

    request = compute_v1.GetUrlMapRequest(
        project=project,
        url_map=url_map,
    )

    urlmap = client.get(request=request)

    for pm in urlmap.path_matchers:
        if pm.name == target_name:
            for pr in pm.path_rules:
                for p in pr.paths:
                    if p == target_path:
                        fip = pr.route_action.fault_injection_policy
                        fip.abort.percentage = float(impacted_percentage)
                        fip.abort.http_status = http_status
                        break

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
    target_path: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Remove any fault injection policy from url map on a given path.

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

    See: https://cloud.google.com/load-balancing/docs/l7-internal/setting-up-traffic-management#configure_fault_injection
    """  # noqa: E501
    credentials = load_credentials(secrets)

    client = compute_v1.UrlMapsClient(credentials=credentials)

    project = credentials.project_id

    request = compute_v1.GetUrlMapRequest(
        project=project,
        url_map=url_map,
    )

    urlmap = client.get(request=request)

    for pm in urlmap.path_matchers:
        if pm.name == target_name:
            for pr in pm.path_rules:
                for p in pr.paths:
                    if p == target_path:
                        pr.route_action.fault_injection_policy = None
                        break

    request = compute_v1.UpdateUrlMapRequest(
        project=project,
        url_map=url_map,
        url_map_resource=urlmap,
    )

    operation = client.update(request=request)
    wait_on_extended_operation(operation=operation)

    return urlmap.__class__.to_dict(urlmap)
