from typing import Any, Dict, List, Optional, Union

from chaoslib.types import Configuration, Secrets
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.query import Query
from google.cloud.monitoring_v3.types.metric import TimeSeries

from chaosgcp import load_credentials, parse_interval

__all__ = [
    "get_metrics",
    "get_slo_health",
    "get_slo_burn_rate",
    "get_slo_budget",
]


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


def get_slo_health(
    name: str,
    end_time: str = "now",
    window: str = "5 minutes",
    alignment_period: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
    cross_series_reducer: int = "REDUCE_COUNT",
    group_by_fields: Optional[Union[str, List[str]]] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Get SLO Health of a service.

    The `name` argument is a full path to an SLO such as
    `"projects/<project_id>/services/<service_name>/serviceLevelObjectives/<slo_id>"`

    See also: https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/timeseries-selectors
    See also: https://cloud.google.com/python/docs/reference/monitoring/latest/google.cloud.monitoring_v3.types.Aggregation
    """  # noqa: E501
    psa = monitoring_v3.Aggregation.Aligner[per_series_aligner]
    csr = monitoring_v3.Aggregation.Reducer[cross_series_reducer]

    credentials = load_credentials(secrets)
    project = credentials.project_id
    start, end = parse_interval(end_time, window)

    client = monitoring_v3.ServiceMonitoringServiceClient(
        credentials=credentials
    )

    request = monitoring_v3.GetServiceLevelObjectiveRequest(
        name=name,
    )
    response = client.get_service_level_objective(request=request)

    group_by_fields = group_by_fields or None

    if isinstance(group_by_fields, str):
        group_by_fields = group_by_fields.split(",")

    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project}",
        filter=f'select_slo_health("{response.name}")',
        interval=monitoring_v3.TimeInterval(
            start_time=start,
            end_time=end,
        ),
        aggregation=monitoring_v3.Aggregation(
            alignment_period={"seconds": alignment_period},
            per_series_aligner=psa,
            cross_series_reducer=csr,
            group_by_fields=group_by_fields,
        ),
    )

    results = client.list_time_series(request=request)

    return list(map(lambda p: p.__class__.to_dict(p), results))


def get_slo_burn_rate(
    name: str,
    end_time: str = "now",
    window: str = "5 minutes",
    loopback_period: str = "300s",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Get SLO burn rate of a service.

    The `name` argument is a full path to an SLO such as
    `"projects/<project_id>/services/<service_name>/serviceLevelObjectives/<slo_id>"`

    See also: https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/timeseries-selectors
    """  # noqa: E501
    credentials = load_credentials(secrets)
    project = credentials.project_id
    start, end = parse_interval(end_time, window)

    client = monitoring_v3.ServiceMonitoringServiceClient(
        credentials=credentials
    )

    request = monitoring_v3.GetServiceLevelObjectiveRequest(
        name=name,
    )
    response = client.get_service_level_objective(request=request)

    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project}",
        filter=f'select_slo_burn_rate("{response.name}", "{loopback_period}")',
        interval=monitoring_v3.TimeInterval(
            start_time=start,
            end_time=end,
        ),
    )

    results = client.list_time_series(request=request)

    return list(map(lambda p: p.__class__.to_dict(p), results))


def get_slo_budget(
    name: str,
    end_time: str = "now",
    window: str = "5 minutes",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Get SLO burn rate of a service.

    The `name` argument is a full path to an SLO such as
    `"projects/<project_id>/services/<service_name>/serviceLevelObjectives/<slo_id>"`

    See also: https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/timeseries-selectors
    """  # noqa: E501
    credentials = load_credentials(secrets)
    project = credentials.project_id
    start, end = parse_interval(end_time, window)

    client = monitoring_v3.ServiceMonitoringServiceClient(
        credentials=credentials
    )

    request = monitoring_v3.GetServiceLevelObjectiveRequest(
        name=name,
    )
    response = client.get_service_level_objective(request=request)

    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project}",
        filter=f'select_slo_budget("{response.name}")',
        interval=monitoring_v3.TimeInterval(
            start_time=start,
            end_time=end,
        ),
    )

    results = client.list_time_series(request=request)

    return list(map(lambda p: p.__class__.to_dict(p), results))
