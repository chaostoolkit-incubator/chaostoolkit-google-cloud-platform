import logging
import re

from chaoslib.exceptions import ActivityFailed
from google.cloud.compute_v1.types import compute

logger = logging.getLogger("chaostoolkit")

__all__ = ["get_fault_injection_policy", "remove_fault_injection_policy"]


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
