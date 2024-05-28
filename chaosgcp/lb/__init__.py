import logging
import re

from chaoslib.exceptions import ActivityFailed
from google.cloud.compute_v1.types import compute

logger = logging.getLogger("chaostoolkit")

__all__ = ["get_path_matcher"]


def get_path_matcher(
    urlmap: compute.UrlMap, target_name: str, target_path: str
) -> compute.PathMatcher:
    url_map = urlmap.name
    path_matcher_found = False
    found_pr = None

    for pm in urlmap.path_matchers:
        if found_pr:
            break

        if pm.name == target_name:
            path_matcher_found = True

            for pr in pm.path_rules:
                if found_pr:
                    break

                for p in pr.paths:
                    if p == target_path:
                        found_pr = pr
                        break

            if found_pr:
                break

            for rr in pm.route_rules:
                if found_pr:
                    break

                for mr in rr.match_rules:
                    if mr.regex_match:
                        pattern = re.compile(mr.regex_match)
                        if pattern.match(target_path):
                            found_pr = pr
                            break

                    if mr.full_path_match:
                        if target_path == mr.full_path_match:
                            found_pr = pr
                            break

                    if mr.prefix_match:
                        if target_path.startswith(mr.prefix_match):
                            found_pr = pr
                            break

    if not path_matcher_found:
        logger.debug(
            f"Failed to find path matcher '{target_name}' in URL map '{url_map}'"
        )
        raise ActivityFailed("failed to match the appropriate path matcher")

    if not found_pr:
        logger.debug(
            f"Failed to find path '{target_path}' in path matcher '{target_name}'"
        )
        raise ActivityFailed("failed to match the appropriate route/path")

    logger.debug(f"Found path '({target_path}' in '{target_name}'")

    return found_pr
