# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

import fixtures

from chaosgcp.storage.probes import object_exists


@patch("chaosgcp.storage.gc_storage.Client", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_storage_object_exists(Credentials, gcs_client):
    Credentials.from_service_account_file.return_value = MagicMock()

    bucket = MagicMock()
    gcs_client.get_bucket.return_value = bucket
    blob = MagicMock()
    bucket.get_blob.return_value = blob

    assert object_exists(
        "bucket-id",
        "my-object-id",
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )


@patch("chaosgcp.storage.gc_storage", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_storage_object_does_not_exist(Credentials, gc_storage):
    Credentials.from_service_account_file.return_value = MagicMock()

    gcs_client = MagicMock()
    gc_storage.Client.return_value = gcs_client
    bucket = MagicMock()
    gcs_client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = None

    assert not object_exists(
        "bucket-id",
        "my-object-id",
        secrets=fixtures.secrets,
        configuration=fixtures.configuration,
    )
