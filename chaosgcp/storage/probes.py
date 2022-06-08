# -*- coding: utf-8 -*-

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosgcp import storage

__all__ = ["object_exists"]


def object_exists(
    bucket_name: str,
    object_name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Indicates whether a file in Cloud Storage bucket exists.

    :param bucket_name: name of the bucket
    :param object_name: name of the object within the bucket as path
    :param configuration:
    :param secrets:
    """
    validate_bucket_object_args(bucket_name, object_name)

    client = storage.client(configuration=configuration, secrets=secrets)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(object_name)

    logger.debug(
        "Object {o} exists in bucket {b}? {blob}".format(
            b=bucket_name, o=object_name, blob=blob
        )
    )

    return blob is not None


###############################################################################
# Private functions
###############################################################################
def validate_bucket_object_args(bucket_name, object_name):
    """
    Ensure both arguments are valid ie not empty or raises error

    :param bucket_name: Name of the bucket
    :param object_name: Name of the object (as path format)
    """
    if not bucket_name:
        raise ActivityFailed("Cannot get object. " "Bucket name is mandatory.")
    if not object_name:
        raise ActivityFailed("Cannot get object. " "Object name is mandatory.")
