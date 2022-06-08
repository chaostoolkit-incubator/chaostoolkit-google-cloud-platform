# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets

from chaosgcp import get_context, get_service

__all__ = ["run_trigger"]


def run_trigger(
    name: str,
    source: Dict[Any, Any],
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Runs a BuildTrigger at a particular source revision.

    NB: The trigger must exist in the targeted project.

    See: https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.triggers/run

    :param name: name of the trigger
    :param source: location of the source in a Google Cloud Source Repository
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
        .run(projectId=ctx.project_id, triggerId=name, body=source)
    )
    response = request.execute()
    return response
