# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from google.cloud import run_v2

from chaosgcp import load_credentials

__all__ = ["get_service", "list_services", "list_service_revisions"]


def get_service(
    name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Retrieve a single cloud run service

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_get_service

    :param name: the path to the service 'projects/PROJECT_ID/locations/LOC/services/SVC
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

    client = run_v2.ServicesClient(credentials=credentials)
    request = run_v2.GetServiceRequest(name=name)
    response = client.get_service(request=request)
    return response.__class__.to_dict(response)


def list_services(
    parent: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List all Cloud Run services

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_list_services

    :param parent: the path to the service 'projects/PROJECT_ID/locations/LOC
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

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
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    List all Cloud Run service revisions for a specific service.

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.revisions.RevisionsClient#google_cloud_run_v2_services_revisions_RevisionsClient_list_revisions

    :param parent: the path to the service 'projects/PROJECT_ID/locations/LOC/service/SVC
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

    client = run_v2.RevisionsClient(credentials=credentials)
    request = run_v2.ListRevisionsRequest(parent=parent)
    return list(
        map(
            lambda p: p.__class__.to_dict(p),
            client.list_revisions(request=request),
        )
    )


def get_active_revisions_autoscaling_config(
    parent: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    list_service_revisions(parent, configuration, secrets)
