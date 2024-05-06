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
import datetime
import logging
import time
from datetime import timezone
from typing import List, Dict


from chaoslib.exceptions import InterruptExecution
from chaoslib.types import Configuration, Experiment, Journal, Secrets

from chaosgcp import client

__all__ = ["before_experiment_control", "after_experiment_control"]

logger = logging.getLogger("chaostoolkit")
# To get the current time, which will be used while granting and revoking conditional role
set_current_time = datetime.datetime.now(timezone.utc)


def before_experiment_control(
    context: Experiment,
    project_id: str,
    roles: List[str],
    members: List[str],
    iam_propogation_sleep_time_in_minutes: int = 2,
    expiry_time_in_minutes: int = 10,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """Set IAM roles for chaos experiments.

    This function temporarily adds specified IAM roles to designated members
    within a project for the duration of a chaos experiment. It calculates an
    expiration timestamp and applies a time-bound IAM condition to ensure
    automatic role removal after the experiment concludes.

    Args:
        context: The Experiment context
        project_id: The ID of the project where IAM roles will be managed.
        roles: A list of IAM role names to be added to members.
        members: A list of member identities (e.g., emails) to receive roles.
        configuration: (Optional) Configuration object for the experiment.
        secrets: (Optional) Secrets object containing sensitive information.
        iam_propogation_sleep_time_in_minutes: (Optional) Time (in minutes) to
            allow for IAM changes to propagate (default: 2).
        expiry_time_in_minutes: (Optional) Duration (in minutes) after which
            the IAM roles should expire (default: 10).

    Raises:
        InterruptExecution: If an error occurs while adding the IAM roles,
            preventing the experiment from proceeding.
    """
    # Generate expiration timestamp (current time + expiration_minutes)
    expire_time_minutes = (
        iam_propogation_sleep_time_in_minutes + expiry_time_in_minutes
    )
    expiration_timestamp = set_current_time + datetime.timedelta(
        minutes=expire_time_minutes
    )
    formatted_timestamp = expiration_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    roles_iam_condition = {
        "title": "chaostoolkit",
        "description": "Should expire soon",
        "expression": f'request.time < timestamp("{formatted_timestamp}")',
    }
    try:
        manage_time_bound_temporary_iam_roles(
            project_id,
            members,
            roles,
            roles_iam_condition,
            "add",
            iam_propogation_sleep_time_in_minutes,
            secrets=secrets,
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise InterruptExecution(
            "Failed to add IAM roles, Please check logs"
        ) from e


def after_experiment_control(
    context: Experiment,
    state: Journal,
    project_id: str,
    roles: List[str],
    members: List[str],
    iam_propogation_sleep_time_in_minutes: int = 2,
    expiry_time_in_minutes: int = 10,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    """Cleans up IAM roles after chaos experiments.

    This function removes temporary IAM roles that were granted to designated
    members within a project during a chaos experiment. It calculates an
    expiration timestamp (which should have already passed) and applies a
    time-bound IAM condition to facilitate the removal process.

    Args:
        context: The Experiment context
        state: The Journal object
        project_id: The ID of the project where IAM roles will be managed.
        roles: A list of IAM role names to be removed from members.
        members: A list of member identities (e.g., emails) to have roles
            removed.
        iam_propogation_sleep_time_in_minutes: (Optional) Time (in minutes) to
            allow for IAM changes to propagate (default: 2).
        expiry_time_in_minutes: (Optional) Duration (in minutes) after which
            the IAM roles should have expired (default: 10).
        configuration: (Optional) Configuration object for the experiment.
        secrets: (Optional) Secrets object containingsensitive information.

    Raises:
        InterruptExecution: If an error occurs while removing the IAM roles,
            potentially indicating an issue with the cleanup process.
    """
    # Generate expiration timestamp (current time + expiration_minutes)
    expire_time_minutes = (
        iam_propogation_sleep_time_in_minutes + expiry_time_in_minutes
    )
    expiration_timestamp = set_current_time + datetime.timedelta(
        minutes=expire_time_minutes
    )
    formatted_timestamp = expiration_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    roles_iam_condition = {
        "title": "chaostoolkit",
        "description": "Should expire soon",
        "expression": f'request.time < timestamp("{formatted_timestamp}")',
    }
    try:
        manage_time_bound_temporary_iam_roles(
            project_id,
            members,
            roles,
            roles_iam_condition,
            "remove",
            iam_propogation_sleep_time_in_minutes,
            secrets=secrets,
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise InterruptExecution(
            "Failed to remove IAM roles, Please check logs"
        ) from e


def manage_time_bound_temporary_iam_roles(
    project_id: str,
    members: List[str],
    roles: List[str],
    roles_iam_condition: Dict[str, str],
    manage_type: str,
    iam_propogation_sleep_time_in_minutes: int = 2,
    secrets: Secrets = None,
) -> None:
    """Manages temporary, time-bound IAM roles for the specified project and members.

    This function either grants or revokes the specified IAM roles to/from the
    provided members, with an expiration time determined by the given condition.

    Args:
        project_id: The ID of the project where the roles will be managed.
        members: A List of member email addresses or IDs to grant/revoke roles to.
        roles: A List of IAM role names to grant/revoke.
        roles_iam_condition: A Dictionary representing the IAM condition that
            enforces the expiration time. It should have the following keys:
            - "title": A descriptive title for the condition.
            - "description": A brief explanation of the condition's purpose.
            - "expression": The Common Expression Language (CEL) expression that
                defines the condition's logic.
        manage_type: The type of operation to perform: "add" to grant roles,
            "remove" to revoke roles.
        iam_propogation_sleep_time_in_minutes: The number of minutes to wait for
            role changes to propagate before proceeding further (default: 2).

    Raises:
        TypeError: If any of the arguments are not of the expected type.
        ValueError: If `manage_type` is not "add" or "remove".
        # (Add other potential exceptions based on your IAM implementation)

    Example:
        # Grant roles with a 15-minute expiration:
        expiration_timestamp = datetime.datetime.now() + datetime.timedelta(minutes=15)
        condition = {
            "title": "TemporaryAccess",
            "description": "Grants access for 15 minutes",
            "expression": f"request.time < timestamp(\"{expiration_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')}\")",
        }
        manage_time_bound_temporary_iam_roles(
            project_id="my-project",
            members=["user1@example.com"],
            roles=["roles/editor"],
            roles_iam_condition=condition,
            manage_type="add",
        )
    """

    # Initializes service.
    crm_service = initialize_service(secrets=secrets)

    if manage_type == "add":
        logger.info("Adding Conditional Roles..")
        logger.info(roles_iam_condition)
        modify_policy_add_roles(
            crm_service,
            project_id,
            roles,
            members,
            roles_iam_condition,
            iam_propogation_sleep_time_in_minutes,
        )

    elif manage_type == "remove":
        logger.info(roles_iam_condition)
        logger.info("Removing Conditional Roles..")
        modify_policy_remove_roles(
            crm_service, project_id, roles, members, roles_iam_condition
        )

    else:
        logger.warning("Invalid manage type: must be 'add' or 'remove'.")
        raise ValueError("Invalid manage type: must be 'add' or 'remove'")


def initialize_service(
    secrets: Secrets = None,
) -> Dict:
    """Initializes a Cloud Resource Manager service."""

    # credentials, _ = google.auth.default(
    #    scopes=["https://www.googleapis.com/auth/cloud-platform"]
    # )
    # crm_service = googleapiclient.discovery.build(
    #    "cloudresourcemanager", "v1", credentials=credentials
    # )
    crm_service = client("cloudresourcemanager", "v1", secrets=secrets)
    return crm_service


def get_policy(crm_service, project_id: str, version: int = 3) -> Dict:
    """Gets IAM policy for a project."""
    logger.info("Getting IAM policy for a project.")
    policy = (
        crm_service.projects()
        .getIamPolicy(
            resource=project_id,
            body={"options": {"requestedPolicyVersion": version}},
        )
        .execute()
    )
    return policy


def set_policy(crm_service, project_id: str, policy: str) -> Dict:
    """Sets IAM policy for a project."""
    logger.info("Setting IAM policy for a project.")
    policy = (
        crm_service.projects()
        .setIamPolicy(resource=project_id, body={"policy": policy})
        .execute()
    )
    return policy


def modify_policy_add_roles(
    crm_service,
    project_id: str,
    roles: List[str],
    member: List[str],
    iam_condition: Dict[str, str],
    iam_propogation_sleep_time_in_minutes: int,
) -> None:
    """Adds a member to multiple roles with an IAM condition (for new roles)."""
    policy = get_policy(crm_service, project_id)
    logger.info(
        "Adding new time based conditional IAM Policy Bindings for this experiment"
    )
    for role in roles:
        binding = {
            "role": role,
            "members": [member],
            "condition": iam_condition,
        }
        policy["bindings"].append(binding)
    policy["version"] = 3
    if roles and member:
        set_policy(crm_service, project_id, policy)
        logger.info(
            f"Waiting for IAM policy propgation for {iam_propogation_sleep_time_in_minutes} minutes"
        )
        time.sleep(iam_propogation_sleep_time_in_minutes * 60)
        logger.info(
            (f"waited for {iam_propogation_sleep_time_in_minutes} minutes")
        )
    else:
        logger.info("No roles or members to Add")


def modify_policy_remove_roles(
    crm_service,
    project_id: str,
    roles: List[str],
    member: List[str],
    iam_condition: Dict[str, str],
) -> None:
    policy = get_policy(crm_service, project_id)
    logger.info(
        "Removing only those IAM Policy Bindings which were assigned during the experiment (if any)"
    )
    for role in roles:
        binding = next(
            (
                b
                for b in policy["bindings"]
                if b["role"] == role
                and b["members"].sort() == member.sort()
                and b.get("condition") == iam_condition
            ),
            None,
        )
        if binding is not None:
            policy["bindings"].remove(binding)
    set_policy(crm_service, project_id, policy)
