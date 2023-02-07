from typing import Any, Dict, List, Optional
from urllib.parse import quote

from chaoslib.types import Configuration, Secrets
from google.cloud import logging

from chaosgcp import get_context, parse_interval

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%Z"


def get_logs_between_timestamps(
    log_name: Optional[str] = None,
    filter: Optional[str] = None,
    end_time: str = "now",
    window: str = "1h",
    order_by: str = "asc",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Read logs during an interval and return a list of entries.
    """
    context = get_context(configuration, secrets)
    client = logging.Client(project=context.project_id)

    start_time, end_time = parse_interval(end_time, window)

    f = ""

    if log_name:
        f = f'logName="projects/{context.project_id}/logs/{quote(log_name, safe="")}"'  # noqa: E501

    if filter and f:
        f = f"{f} AND {filter}"
    elif filter and not f:
        f = filter

    f = f'{f} AND timestamp>="{start_time.isoformat(timespec="seconds")}"'
    f = f'{f} AND timestamp<="{end_time.isoformat(timespec="seconds")}"'

    ordering = order_by = logging.ASCENDING
    if order_by == "desc":
        ordering = logging.DESCENDING

    entries = []
    for entry in client.list_entries(filter_=f, order_by=ordering):
        entries.append(entry.to_api_repr())

    return entries
