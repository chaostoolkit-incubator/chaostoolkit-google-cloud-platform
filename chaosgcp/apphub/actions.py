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
from typing import Dict, Any, List, Generator, Optional

from google.cloud import compute_v1, apphub_v1
from google.cloud import resourcemanager_v3

from chaoslib.types import Configuration, Secrets
from chaosgcp.lb.actions import (
    inject_traffic_faults,
    remove_fault_injection_traffic_policy,
)
from chaosgcp import get_context, load_credentials
from chaoslib.exceptions import ActivityFailed


__all__ = [
    "inject_fault_if_url_map_exists_app_hub",
    "remove_fault_if_url_map_exists_app_hub",
]
logger = logging.getLogger("chaostoolkit")


def apphub_app_list_services(
    host_project_id: str,
    project_id: str,
    location: str,
    application_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[str]:
    """Retrieves a list of service URIs associated with an AppHub application.

    This function queries the AppHub API to list all services deployed within
    a specific application and extracts their associated URIs.

    Args:
        host_project_id (str): The ID of the Host Apphub project.
        project_id (str): The ID of the Google Cloud project to inject fault into.
        location (str): The geographic location (e.g., "us-central1") of the application.
        application_id (str): The unique identifier for the AppHub application.

    Returns:
        list: A list of strings, where each string is the URI of a service associated
              with the specified application. The URIs are formatted to contain the
                      project ID instead of the project number only for project_id."""
    try:
        name_app = f"projects/{host_project_id}/locations/{location}/applications/{application_id}"
        credentials = load_credentials(secrets)
        client = apphub_v1.AppHubClient()
        request = apphub_v1.ListServicesRequest(parent=name_app)
        service_uris = []
        updated_uri = None
        logger.info("Getting attached Services of given Application in Apphub")
        for response in client.list_services(request=request):
            uri = response.service_reference.uri.replace(
                resourcemanager_v3.ProjectsClient(credentials=credentials)
                .get_project(name="projects/{}".format(project_id))
                .name,
                "projects/{}".format(project_id),
            )
            updated_uri = (
                uri[uri.find("/projects/") :] if "/projects/" in uri else uri
            )
            service_uris.append(updated_uri)
        logger.debug(f"Listing Services {updated_uri}")
        return service_uris
    except Exception as e:
        raise ActivityFailed(
            f"Error Listing Services of Apphub Application: {e}"
        )


def get_url_map_essentials(
    project_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Optional[Generator[Dict[str, str], Any, None]]:
    """Retrieves essential information for URL maps in a Google Cloud project.

    This function queries the Google Compute Engine API to fetch key details
    about URL maps (including regional and global) within the specified project.
    It yields a dictionary for each URL map, containing the following:

    * region: The region (or "global") where the URL map is located.
    * service: The default backend service associated with the URL map
    * self_link: The selfLink URL uniquely identifying the URL map resource.
    Args:
        project_id (str): The ID of the Google Cloud project to query.

    Yields:
        Generator[Dict[str, str]]: A dictionary containing the region, service, and self_link of each
            URL map found in the project.

    Raises:
        Error: If there's an error communicating
            with the Google Cloud API (e.g., authentication issues, invalid project ID).
    """
    try:
        # client = compute_v1.UrlMapsClient()
        # request = compute_v1.AggregatedListUrlMapsRequest(project=project_id)
        credentials = load_credentials(secrets)
        context = get_context(configuration, project_id=project_id)
        client = compute_v1.UrlMapsClient(credentials=credentials)
        request = compute_v1.AggregatedListUrlMapsRequest(
            project=context.project_id
        )

        for response in client.aggregated_list(request=request):
            scope, url_maps_scoped_list = response
            region = scope.split("/")[-1] if "/" in scope else "global"

            if url_maps_scoped_list.url_maps:
                for url_map in url_maps_scoped_list.url_maps:
                    yield {
                        "region": region,
                        "service": url_map.default_service[
                            url_map.default_service.find("/projects/") :
                        ]
                        if "/projects/" in url_map.default_service
                        else url_map.default_service,
                        "self_link": url_map.self_link,
                    }
    except Exception as e:
        raise ActivityFailed(f"Error getting urlMaps {e}")


def url_map_exists(
    url_map_value: str,
    host_project_id: str,
    project_id: str,
    region: str,
    application_name: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """Checks if a specific URL map value exists within AppHub-related URL maps.

    This function first retrieves the selfLink URLs of all URL maps associated with services
    in the specified AppHub application. It then searches these URL maps to determine if the
    given `url_map_value` is present after the "urlMaps/" segment.

    Args:
        url_map_value (str): The specific value (e.g., "my-url-map") to search for after "urlMaps/" in the URL.
        host_project_id (str): The ID of the Host Apphub project.
        project_id (str): The ID of the Google Cloud project where service exists.
        region (str): The region where the AppHub application is deployed.
        application_name (str): The name of the AppHub application.

    Returns:
        bool: True if the `url_map_value` is found within the URL maps associated with
              the specified AppHub application.
    """
    try:
        availableUrlMaps = []
        service_uris = apphub_app_list_services(
            host_project_id,
            project_id,
            region,
            application_name,
            configuration,
            secrets,
        )
        url_map_essentials = get_url_map_essentials(
            project_id, configuration, secrets
        )

        for details in url_map_essentials:
            if details["service"] in service_uris:
                availableUrlMaps.append(details["self_link"])
                logger.debug(details["self_link"])

        for umap in availableUrlMaps:
            index = umap.find("/urlMaps/")
            if (
                index != -1
                and umap[index + len("/urlMaps/") :] == url_map_value
            ):
                logger.debug(
                    "given url_map is found within the URL maps associated with the specified AppHub application"
                )
                return True  # Found, so return True immediately

    except Exception as e:
        raise ActivityFailed(f"Error retrieving URL map information: {e}")


def inject_fault_if_url_map_exists_app_hub(
    application_name: str,
    host_project_id: str,
    url_map: str,
    project_id: str,
    region: str,
    target_name: str,
    target_path: str = "/*",
    impacted_percentage: float = 50.0,
    http_status: int = 400,
    regional: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """Processes a URL map if it exists within the specified AppHub application.

    Args:
        application_name (str): The name of the AppHub application.
        url_map (str): The URL map value to check for.
        project_id (str): The Google Cloud project ID.
        region (str): The region of the AppHub application.
        target_name (str): the the name of a path matcher in the URL map.
        target_path (str): default "/*",
        impacted_percentage: float default 50.0,
        http_status (int) default 400,
        regional: (bool) default True,
        configuration: (Configuration) default None,
        secrets: (Secrets) default None,
    """

    if url_map_exists(
        url_map,
        host_project_id,
        project_id,
        region,
        application_name,
        configuration,
        secrets,
    ):
        # URL map exists, proceed with your processing logic here
        logger.info(
            f"Given URL map '{url_map}' found in given Apphub Application. Proceeding with Fault Injection Action "
        )
        inject_traffic_faults(
            url_map,
            target_name,
            target_path,
            impacted_percentage,
            http_status,
            regional,
            project_id,
            region,
            configuration,
            secrets,
        )
    else:
        raise ActivityFailed(
            f"Given URL map '{url_map}' not found in given Apphub Application, Cannot Inject Fault "
        )


def remove_fault_if_url_map_exists_app_hub(
    application_name: str,
    host_project_id: str,
    url_map: str,
    project_id: str,
    region: str,
    target_name: str,
    target_path: str = "/*",
    regional: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """Processes a URL map if it exists within the specified AppHub application.

    Args:
        application_name (str): The name of the AppHub application.
        host_project_id (str): The ID of the Host Apphub project.
        url_map (str): The URL map value to check for.
        project_id (str): The Google Cloud project ID.
        region (str): The region of the AppHub application.
        target_name (str): the the name of a path matcher in the URL map.
        target_path (str): default "/*",
        regional: (bool) default True,
        configuration: (Configuration) default None,
        secrets: (Secrets) default None,
    """

    if url_map_exists(
        url_map,
        host_project_id,
        project_id,
        region,
        application_name,
        configuration,
        secrets,
    ):
        # URL map exists, proceed with your processing logic here
        logger.info(
            f"URL map '{url_map}' - Rollback of Fault Injection Action "
        )
        remove_fault_injection_traffic_policy(
            url_map,
            target_name,
            target_path,
            regional,
            project_id,
            region,
            configuration,
            secrets,
        )
    else:
        raise ActivityFailed(
            f"Given URL map '{url_map}' not found, RollBack not required "
        )
