# -*- coding: utf-8 -*-

from chaoslib.types import Configuration, Secrets

from chaosgcp import get_context, get_service

__all__ = ["list_triggers", "list_trigger_names", "get_trigger"]


def list_triggers(
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Lists existing BuildTriggers.

    See: https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.triggers/list

    :param configuration:
    :param secrets:

    :return:
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "cloudbuild", version="v1", configuration=configuration, secrets=secrets
    )

    request = service.projects().triggers().list(projectId=ctx.project_id)
    response = request.execute()
    return response


def list_trigger_names(
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    List only the trigger names of a project

    :param configuration:
    :param secrets:

    :return:
    """
    triggers = list_triggers(configuration=configuration, secrets=secrets)
    return [t["name"] for t in triggers["triggers"]]


def get_trigger(
    name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Returns information about a BuildTrigger.

    See: https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.triggers/get

    :param name: name of the trigger
    :param configuration:
    :param secrets:
    :return:
    """  # noqa: E501
    ctx = get_context(configuration=configuration, secrets=secrets)
    service = get_service(
        "cloudbuild", version="v1", configuration=configuration, secrets=secrets
    )

    request = (
        service.projects()
        .triggers()
        .get(projectId=ctx.project_id, triggerId=name)
    )
    response = request.execute()
    return response
