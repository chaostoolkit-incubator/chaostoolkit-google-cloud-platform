import logging
import uuid
from urllib.parse import quote_plus
from typing import Dict

from chaoslib.types import Configuration, Experiment, Journal, Secrets
from google.cloud import logging as gcp_logging

from chaosgcp import get_context

__all__ = ["after_experiment_control"]
logger = logging.getLogger("chaostoolkit")


def after_experiment_control(
    context: Experiment,
    state: Journal,
    labels: Dict[str, str] = None,
    project_id: str = None,
    region: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """
    Sends the full journal to Cloud Logging as a single payload
    """
    context = get_context(configuration, project_id=project_id, region=region)

    if not labels:
        labels = {}

    if context.region:
        labels["location"] = context.region

    insert_id = str(uuid.uuid4())

    client = gcp_logging.Client(project=context.project_id)
    cloud_logger = client.logger(name=quote_plus("chaostoolkit.org/journal"))
    cloud_logger.log_struct(info=state, insert_id=insert_id, labels=labels)
    logger.info(f"Journal sent to Cloud Logging with insert id: {insert_id}")
