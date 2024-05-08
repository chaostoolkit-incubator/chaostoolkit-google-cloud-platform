# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from chaoslib.types import Configuration, Secrets
from google.cloud import apphub_v1


__all__ = ["apphub_list_app_services"]
logger = logging.getLogger("chaostoolkit")


def apphub_list_app_services(
    host_project_id: str,
    location: str,
    application_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    # Create the fully qualified name string
    name_app = f"projects/{host_project_id}/locations/{location}/applications/{application_id}"
    # Create a client
    client = apphub_v1.AppHubClient()

    # Initialize request argument(s)
    request = apphub_v1.ListServicesRequest(
        parent=name_app,
    )

    # Make the request
    page_result = client.list_services(request=request)

    # Handle the response
    for response in page_result:
        logger.info(response)
