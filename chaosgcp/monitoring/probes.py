import json
import re
import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1
from google.cloud import monitoring_v3
from google.cloud.compute_v1.types import compute
from google.cloud.monitoring_v3.query import Query
from google.cloud.monitoring_v3.types.metric import TimeSeries

from chaosgcp import get_context, load_credentials, parse_interval

__all__ = [
    "get_metrics",
    "get_slo_health",
    "get_slo_burn_rate",
    "get_slo_budget",
    "valid_slo_ratio_during_window",
    "run_mql_query",
    "get_slo_from_url",
    "get_slo_health_from_url",
]
logger = logging.getLogger("chaostoolkit")


def get_metrics(
    metric_type: str,
    metric_labels_filters: Optional[Union[str, Dict[str, str]]] = None,
    resource_labels_filters: Optional[Union[str, Dict[str, str]]] = None,
    end_time: str = "now",
    window: str = "5 minutes",
    aligner: int = 0,
    aligner_minutes: int = 1,
    reducer: int = 0,
    reducer_group_by: Optional[List[str]] = None,
    project_id: str = None,
    region: str = None,
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
        if isinstance(metric_labels_filters, str):
            mlf = metric_labels_filters
            metric_labels_filters = {}
            for f in mlf.split(","):
                k, v = f.split("=", 1)
                metric_labels_filters[k] = v
        q = q.select_metrics(**metric_labels_filters)

    if resource_labels_filters:
        if isinstance(resource_labels_filters, str):
            rlf = resource_labels_filters
            resource_labels_filters = {}
            for f in rlf.split(","):
                k, v = f.split("=", 1)
                resource_labels_filters[k] = v
        q = q.select_resources(**resource_labels_filters)

    series = []
    for timeseries in q:
        d = TimeSeries.to_dict(timeseries)
        series.append(d)

    return series


def run_mql_query(
    project: str,
    mql: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Execute a MQL query and return its results.

    Use the project name or id.
    """
    credentials = load_credentials(secrets)
    client = monitoring_v3.QueryServiceClient(credentials=credentials)

    request = monitoring_v3.QueryTimeSeriesRequest(
        name=f"projects/{project}",
        query=mql,
    )

    results = client.query_time_series(request=request)

    return list(map(lambda p: p.__class__.to_dict(p), results))


def get_slo_health(
    name: str,
    end_time: str = "now",
    window: str = "5 minutes",
    alignment_period: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
    cross_series_reducer: int = "REDUCE_COUNT",
    group_by_fields: Optional[Union[str, List[str]]] = None,
    project_id: str = None,
    region: str = None,
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
    context = get_context(configuration, project_id=project_id, region=region)
    project = context.project_id
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
    project_id: str = None,
    region: str = None,
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
    context = get_context(configuration, project_id=project_id, region=region)
    project = context.project_id
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
    project_id: str = None,
    region: str = None,
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
    context = get_context(configuration, project_id=project_id, region=region)
    project = context.project_id
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
    min_level: Union[float, int, bool, str] = 0.90,
    end_time: str = "now",
    window: str = "5 minutes",
    alignment_period: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
    cross_series_reducer: int = "REDUCE_COUNT",
    group_by_fields: Optional[Union[str, List[str]]] = None,
    project_id: str = None,
    region: str = None,
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

    This probe does not support point of type `distribution_value`.

    See also: https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/timeseries-selectors
    See also: https://cloud.google.com/python/docs/reference/monitoring/latest/google.cloud.monitoring_v3.types.Aggregation
    See also: https://cloud.google.com/python/docs/reference/monitoring/latest/google.cloud.monitoring_v3.types.TypedValue
    """  # noqa: E501
    response = get_slo_health(
        name,
        end_time,
        window,
        alignment_period,
        per_series_aligner,
        cross_series_reducer,
        group_by_fields,
        project_id,
        region,
        configuration,
        secrets,
    )

    logger.debug(f"Return SLO health: {response}")

    if not response:
        logger.debug("SLO has no data for that period of time")
        return False

    points = response[0]["points"]

    good = 0
    total = 0
    for pt in points:
        total += 1
        if "double_value" in pt["value"]:
            if pt["value"]["double_value"] >= min_level:
                good += 1
        elif "int64_value" in pt["value"]:
            # because this is an int64, this is returned a string
            # Python3 should automatically handle this on 64 machines
            # Rust would be more explicit here
            if int(pt["value"]["int64_value"]) >= min_level:
                good += 1
        elif "bool_value" in pt["value"]:
            if pt["value"]["bool_value"] == min_level:
                good += 1
        elif "string_value" in pt["value"]:
            if pt["value"]["string_value"] == min_level:
                good += 1

    return ((good * 100.0) / total) >= expected_ratio


def query_time_series(
    mql_query: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Query time series using a MQL query.

    See also: https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/query
    """
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)
    project = context.project_id

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


def get_slo_from_url(
    url: str,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Get all SLOs associated directly with a URL from the load balancer
    perspective.
    """  # noqa: E501
    credentials = load_credentials(secrets)
    context = get_context(configuration, project_id=project_id, region=region)
    project = context.project_id
    backend_services = get_backend_services_from_url(credentials, context, url)

    client = monitoring_v3.ServiceMonitoringServiceClient(
        credentials=credentials
    )

    request = monitoring_v3.ListServicesRequest(parent=f"projects/{project}")
    services = client.list_services(request=request)

    results = []

    for service in services:
        if service.gke_service:
            request = monitoring_v3.ListServiceLevelObjectivesRequest(
                parent=service.name, view="EXPLICIT"
            )
            slos = client.list_service_level_objectives(request=request)
            for slo in slos:
                slo_dict = slo.__class__.to_dict(slo)

                # rather than exploring all potential sli combination
                # we just want to know if the backend service is used by the slo
                slo_str = json.dumps(slo_dict)
                for bs in backend_services:
                    if bs in slo_str:
                        results.append(slo_dict)

    return results


def get_slo_health_from_url(
    url: str,
    end_time: str = "now",
    window: str = "5 minutes",
    alignment_period: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
    cross_series_reducer: int = "REDUCE_COUNT",
    group_by_fields: Optional[Union[str, List[str]]] = None,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Get all SLO healths associated directly with a URL from the load balancer
    perspective.

    Use this probe to efficientely retrieve the curerent health of SLOs
    associated with a particular URL endpoint.
    """  # noqa: E501
    healths = []
    slos = get_slo_from_url(url, project_id, region, configuration, secrets)
    for slo in slos:
        healths.append(
            get_slo_health(
                slo["name"],
                end_time,
                window,
                alignment_period,
                per_series_aligner,
                cross_series_reducer,
                group_by_fields,
                project_id,
                region,
                configuration,
                secrets,
            )
        )
    return healths


###############################################################################
# Private functions
###############################################################################
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


def get_backend_services_from_url(credentials, context, url: str) -> List[str]:
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
    url_map, route_action = get_route_action_from_url(urlmaps, url)

    backend_services = []
    for bs in route_action.weighted_backend_services:
        _, name = bs.backend_service.rsplit("/", 1)
        backend_services.append(name)

    return backend_services
