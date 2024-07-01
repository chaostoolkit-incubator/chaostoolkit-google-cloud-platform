import logging
import re
from typing import List, Tuple
from urllib.parse import urlparse

from chaoslib.exceptions import ActivityFailed
from google.cloud.compute_v1.types import compute

logger = logging.getLogger("chaostoolkit")

__all__ = [
    "get_fault_injection_policy",
    "remove_fault_injection_policy",
    "get_route_action_from_url",
]


def get_fault_injection_policy(
    urlmap: compute.UrlMap, target_name: str, target_path: str
) -> compute.HttpFaultInjection:
    route_action = get_route_action(urlmap, target_name, target_path)
    return route_action.fault_injection_policy


def remove_fault_injection_policy(
    urlmap: compute.UrlMap, target_name: str, target_path: str
) -> None:
    route_action = get_route_action(urlmap, target_name, target_path)
    route_action.fault_injection_policy = None


def get_fault_injection_policy_from_url(
    urlmaps: List[compute.UrlMap],
    url: str,
) -> Tuple[compute.UrlMap, compute.HttpRouteAction]:
    return get_route_action_from_url(urlmaps, url)


###############################################################################
# Private function
###############################################################################
def get_route_action(
    urlmap: compute.UrlMap, target_name: str, target_path: str
) -> compute.HttpRouteAction:
    url_map = urlmap.name
    path_matcher_found = False
    route_action = None

    for pm in urlmap.path_matchers:
        if route_action:
            break

        if pm.name == target_name:
            path_matcher_found = True

            for pr in pm.path_rules:
                if route_action:
                    break

                for p in pr.paths:
                    if p == target_path:
                        route_action = pr.route_action
                        break

            if route_action:
                break

            for rr in pm.route_rules:
                if route_action:
                    break

                for mr in rr.match_rules:
                    if mr.regex_match:
                        pattern = re.compile(mr.regex_match)
                        if pattern.match(target_path):
                            route_action = rr.route_action
                            break

                    if mr.full_path_match:
                        if target_path == mr.full_path_match:
                            route_action = rr.route_action
                            break

                    if mr.prefix_match:
                        if target_path.startswith(mr.prefix_match):
                            route_action = rr.route_action
                            break

    if not path_matcher_found:
        logger.debug(
            f"Failed to find path matcher '{target_name}' in URL map '{url_map}'"
        )
        raise ActivityFailed("failed to match the appropriate path matcher")

    if route_action is None:
        logger.debug(
            f"Failed to find path '{target_path}' in path matcher '{target_name}'"
        )
        raise ActivityFailed("failed to match the appropriate route/path")

    logger.debug(f"Found path '{target_path}' in '{target_name}'")

    return route_action


def get_route_action_from_url(
    urlmaps: List[compute.UrlMap], url: str
) -> Tuple[compute.UrlMap, compute.HttpRouteAction]:
    p = urlparse(url)
    domain = p.netloc

    found_urlmap = None
    for urlmap in urlmaps:
        if found_urlmap:
            break

        for host_rule in urlmap.host_rules:
            if domain in host_rule.hosts:
                found_urlmap = urlmap
                break

    for pm in found_urlmap.path_matchers:
        for rr in pm.route_rules:
            for mr in rr.match_rules:
                if mr.prefix_match is not None:
                    pattern = re.compile(f"^{mr.prefix_match}")
                    print(pattern, p.path, pattern.match(p.path))
                    if pattern.match(p.path):
                        return (found_urlmap, rr.route_action)
                elif mr.full_path_match is not None:
                    pattern = re.compile(f"^{mr.full_path_match}$")
                    if pattern.match(p.path):
                        return (found_urlmap, rr.route_action)
                elif mr.regex_match is not None:
                    pattern = re.compile(f"^{mr.regex_match}$")
                    if pattern.match(p.path):
                        return (found_urlmap, rr.route_action)

    raise ActivityFailed("failed to find a suitable route")
