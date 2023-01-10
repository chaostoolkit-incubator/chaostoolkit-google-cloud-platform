# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from google.cloud import run_v2

from chaosgcp import load_credentials

__all__ = ["create_service", "delete_service", "update_service"]


def create_service(
    parent: str,
    service_id: str,
    container: Dict[str, Any],
    description: str = None,
    max_instance_request_concurrency: int = 0,
    service_account: str = None,
    encryption_key: str = None,
    traffic: List[Dict[str, Any]] = None,
    labels: Dict[str, str] = None,
    annotations: Dict[str, str] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Deletes a Cloud Run service and all its revisions. Cannot be undone.

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_delete_service

    :param parent: the path to the location in the project 'projects/PROJECT_ID/locations/LOC
    :param service_id: unique identifier for the service
    :param container: definition of the container as per https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.types.Container
    :param description: optional text description of the service
    :param max_instance_request_concurrency: optional maximum number of requests that each serving instance can receive
    :param labels: optional labels to set on the service
    :param annotations: optional annotations to set on the service
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

    traffics = None
    if traffic:
        traffics = list(map(lambda t: run_v2.TrafficTarget(**t), traffic))

    max_instances = 0
    if max_instance_request_concurrency:
        max_instances = max_instance_request_concurrency

    client = run_v2.ServicesClient(credentials=credentials)
    tpl = run_v2.RevisionTemplate(
        max_instance_request_concurrency=max_instances,
        service_account=service_account,
        encryption_key=encryption_key,
        containers=[run_v2.Container(**container)],
    )
    svc = run_v2.Service(
        description=description,
        labels=labels,
        annotations=annotations,
        template=tpl,
        traffic=traffics,
    )
    request = run_v2.CreateServiceRequest(
        parent=parent, service_id=service_id, service=svc
    )

    operation = client.create_service(request=request)
    response = operation.result()
    return response.__class__.to_dict(response)


def delete_service(
    parent: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Deletes a Cloud Run service and all its revisions. Cannot be undone.

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_delete_service

    :param parent: the path to the service 'projects/PROJECT_ID/locations/LOC/services/SVC
    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    credentials = load_credentials(secrets)

    client = run_v2.ServicesClient(credentials=credentials)
    request = run_v2.DeleteServiceRequest(
        name=parent,
    )

    operation = client.delete_service(request=request)
    response = operation.result()
    return response.__class__.to_dict(response)


def update_service(
    parent: str,
    container: Dict[str, Any] = None,
    max_instance_request_concurrency: int = 100,
    service_account: str = None,
    encryption_key: str = None,
    traffic: List[Dict[str, Any]] = None,
    labels: Dict[str, str] = None,
    annotations: Dict[str, str] = None,
    vpc_access_config: Dict[str, str] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Updates a Cloud Run service.

    For example:

    ```json
    {
        "name": "route-traffic-two-latest-and-older-revision",
        "type": "action",
        "provider": {
            "type": "python",
            "module": chaosgcp.cloudrun.actions",
            "func": "update_service",
            "arguments": {
                "parent": "projects/${gcp_project_id}/locations/${gcp_location}/services/${service_name}",
                "container": {
                    "image": "eu.gcr.io/${gcp_project_id}/demo"
                },
                "traffic": [{
                    "type_": 1,
                    "percent": 50
                }, {
                    "type_": 2,
                    "revision": "whatever-w788x",
                    "percent": 50
                }],
            }
        }
    }
    ```

    See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_delete_service

    :param container: definition of the container as per https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.types.Container
    :param labels: optional labels to set on the service
    :param annotations: optional annotations to set on the service
    :param configuration:
    :param secrets:
    :param vpc_access_config: optional value for vpc_connect

    :return:
    """  # noqa: E501

    credentials = load_credentials(secrets)

    traffics = None
    if traffic:
        traffics = list(map(lambda t: run_v2.TrafficTarget(**t), traffic))

    containers = None
    if container:
        containers = [run_v2.Container(**container)]

    vpc_access = None
    if vpc_access_config:
        vpc_access = vpc_access_config

    client = run_v2.ServicesClient(credentials=credentials)

    tpl = run_v2.RevisionTemplate(
        max_instance_request_concurrency=max_instance_request_concurrency,
        service_account=service_account,
        encryption_key=encryption_key,
        containers=containers,
        vpc_access=vpc_access,
    )

    svc = run_v2.Service(
        name=parent,
        labels=labels,
        annotations=annotations,
        template=tpl,
        traffic=traffics,
    )
    request = run_v2.UpdateServiceRequest(service=svc)

    operation = client.update_service(request=request)
    response = operation.result()

    return response.__class__.to_dict(response)
