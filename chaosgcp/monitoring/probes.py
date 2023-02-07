from typing import Any, Dict, List, Optional

from chaoslib.types import Configuration, Secrets
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.query import Query
from google.cloud.monitoring_v3.types.metric import TimeSeries

from chaosgcp import load_credentials, parse_interval

__all__ = ["get_metrics"]


def get_metrics(
    metric_type: str,
    metric_labels_filters: Optional[Dict[str, str]] = None,
    resource_labels_filters: Optional[Dict[str, str]] = None,
    end_time: str = "now",
    window: str = "5 minutes",
    aligner: int = 0,
    aligner_minutes: int = 1,
    reducer: int = 0,
    reducer_group_by: Optional[List[str]] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Query for Cloud Monitoring metrics and returns a list of time series
    objects for the metric and period.

    Refer to the documentation
    https://cloud.google.com/python/docs/reference/monitoring/latest/query
    to learn about the various flags.
    """
    credentials = load_credentials(secrets)
    client = monitoring_v3.MetricServiceClient(credentials=credentials)

    start, end = parse_interval(end_time, window)
    interval = (end - start).total_seconds()
    if interval <= 60.0:
        interval = 1
    else:
        interval = int(interval / 60.0)

    q = Query(
        client=client,
        project=credentials.project_id,
        metric_type=metric_type,
        end_time=end,
        minutes=interval,
    )

    q = q.align(aligner, aligner_minutes)
    if reducer_group_by:
        q = q.reduce(reducer, *reducer_group_by)

    if metric_labels_filters:
        q = q.select_metrics(**metric_labels_filters)

    if resource_labels_filters:
        q = q.select_resources(**resource_labels_filters)

    series = []
    for timeseries in q:
        d = TimeSeries.to_dict(timeseries)
        series.append(d)

    return series
