# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from google.cloud import run_v2

from chaosgcp import load_credentials

__all__ = ["get_service", "list_services", "list_service_revisions"]


def get_service(
    parent: str = None,
    project_id: str = None,
    region: str = None,
    name: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Retrieve a single cloud run service

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_get_service

    :param parent: the path to the service 'projects/PROJECT_ID/locations/LOC/services/SVC
    :param project_id: the project identifier where to delete the service when `parent` is not set
    :param region: the region where to delete the service when `parent` is not set
    :param name: the name of the service when `parent` is not set
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

    if not parent and not project_id and not region and not name:
        raise ActivityFailed(
            "set the parent or (project_id, region, name) arguments"
        )

    if not parent:
        parent = f"project/{project_id}/locations/{region}/services/{name}"

    client = run_v2.ServicesClient(credentials=credentials)
    request = run_v2.GetServiceRequest(name=parent)
    response = client.get_service(request=request)
    return response.__class__.to_dict(response)


def list_services(
    parent: str = None,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List all Cloud Run services

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_list_services

    :param parent: the path to the location in the project 'projects/PROJECT_ID/locations/LOC. Otherwise set the `project_id` and `region` fields
    :param project_id: the project identifier where to create the service when `parent` is not set
    :param region: the region where to create the service when `parent` is not set
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

    if not parent and not project_id and not region:
        raise ActivityFailed("set the parent or (project_id, region) arguments")

    if not parent:
        parent = f"project/{project_id}/locations/{region}"

    client = run_v2.ServicesClient(credentials=credentials)
    request = run_v2.ListServicesRequest(parent=parent)
    return list(
        map(
            lambda p: p.__class__.to_dict(p),
            client.list_services(request=request),
        )
    )


def list_service_revisions(
    parent: str,
    project_id: str = None,
    region: str = None,
    name: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List all Cloud Run service revisions for a specific service.

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.revisions.RevisionsClient#google_cloud_run_v2_services_revisions_RevisionsClient_list_revisions

    :param parent: the path to the service 'projects/PROJECT_ID/locations/LOC/services/SVC
    :param project_id: the project identifier where to delete the service when `parent` is not set
    :param region: the region where to delete the service when `parent` is not set
    :param name: the name of the service when `parent` is not set
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

    if not parent and not project_id and not region and not name:
        raise ActivityFailed(
            "set the parent or (project_id, region, name) arguments"
        )

    if not parent:
        parent = f"project/{project_id}/locations/{region}/services/{name}"

    client = run_v2.RevisionsClient(credentials=credentials)
    request = run_v2.ListRevisionsRequest(parent=parent)
    return list(
        map(
            lambda p: p.__class__.to_dict(p),
            client.list_revisions(request=request),
        )
    )
