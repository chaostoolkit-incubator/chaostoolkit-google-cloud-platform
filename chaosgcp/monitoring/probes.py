from typing import Any, Dict, List, Optional, Union

from chaoslib.types import Configuration, Secrets
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.query import Query
from google.cloud.monitoring_v3.types.metric import TimeSeries
from logzero import logger

from chaosgcp import load_credentials, parse_interval

__all__ = [
    "get_metrics",
    "get_slo_health",
    "get_slo_burn_rate",
    "get_slo_budget",
    "valid_slo_ratio_during_window",
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


def valid_slo_ratio_during_window(
    name: str,
    expected_ratio: float = 0.90,
    min_level: float = 0.90,
    end_time: str = "now",
    window: str = "5 minutes",
    alignment_period: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
    cross_series_reducer: int = "REDUCE_COUNT",
    group_by_fields: Optional[Union[str, List[str]]] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Compute SLO during various intervals of the window. Then for each returned
    interval, we compare the SLO with `min_level` (between 0 and 1.0).

    Finally use the `expected_ratio` value (between 0 and 1.0) as the treshold
    which tells us if our service was reaching `min_level` for at least
    that number of time.

    For instance, with `expected_ratio` set to `0.5` and `min_level` set to
    `0.8`, we say that we want that 50% of the intervals have a SLO
    above `0.8`.

    The `name` argument is a full path to an SLO such as
    `"projects/<project_id>/services/<service_name>/serviceLevelObjectives/<slo_id>"`

    See also: https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/timeseries-selectors
    See also: https://cloud.google.com/python/docs/reference/monitoring/latest/google.cloud.monitoring_v3.types.Aggregation
    """  # noqa: E501
    response = get_slo_health(
        name,
        end_time,
        window,
        alignment_period,
        per_series_aligner,
        cross_series_reducer,
        group_by_fields,
        configuration,
        secrets,
    )

    logger.debug(f"Return SLO health: {response}")

    points = response[0]["points"]

    good = 0
    total = 0
    for pt in points:
        total += 1
        if pt["value"]["double_value"] >= min_level:
            good += 1

    return ((good * 100.0) / total) >= expected_ratio


def query_time_series(
    mql_query: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Query time series using a MQL query.

    See also: https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/query
    """
    credentials = load_credentials(secrets)
    project = credentials.project_id

    client = monitoring_v3.QueryServiceClient(credentials=credentials)
    request = monitoring_v3.QueryTimeSeriesRequest(
        name=f"projects/{project}",
        query=mql_query,
    )

    return list(
        map(
            lambda p: p.__class__.to_dict(p),
            client.query_time_series(request=request),
        )
    )


q = """fetch https_lb_rule::loadbalancing.googleapis.com/https/request_count
| filter
    resource.url_map_name = "demo-urlmap"
    && resource.project_id = "staging10022023"
| { buckets:
      filter resource.backend_target_type = 'BACKEND_BUCKET'
      | map update[resource.backend_name: resource.backend_target_name]
      | align delta()
      | filter_ratio_by
          [resource.url_map_name, resource.project_id, resource.backend_name,
           resource.backend_target_name],
          metric.response_code_class = 200
  ; services:
      filter resource.backend_target_type = 'BACKEND_SERVICE'
      | align delta()
      | filter_ratio_by
          [resource.url_map_name, resource.project_id, resource.backend_name,
           resource.backend_target_name],
          metric.response_code_class = 200 }
| union
| within 60m
"""
r = query_time_series(q, {}, {})

print(r)
