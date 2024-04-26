#Copyright 2024 Google LLC

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


from unittest.mock import MagicMock, patch
from chaosgcp.iam.controls import policy as imported_policy
import fixtures


@patch("chaosgcp.iam.controls.policy.initialize_service", autospec=True)
@patch("chaosgcp.iam.controls.policy.get_policy", autospec=True)
@patch("chaosgcp.iam.controls.policy.set_policy", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_manage_time_bound_temporary_iam_roles(
    initialize_service, get_policy, set_policy, Credentials
):
    initialize_service.return_value = MagicMock()
    set_policy.return_value = MagicMock()
    get_policy.return_value = MagicMock()
    # Test Remove roles
    imported_policy.manage_time_bound_temporary_iam_roles(
        "project_id",
        ["roles/editor"],
        ["user:owner@example.com"],
        {"title": "test", "description": "test", "expression": "test"},
        "remove",
        0,
    )
    # Test Add roles
    imported_policy.manage_time_bound_temporary_iam_roles(
        "project_id",
        ["roles/editor"],
        ["user:owner@example.com"],
        {"title": "test", "description": "test", "expression": "test"},
        "add",
        0,
    )


@patch("chaosgcp.iam.controls.policy.initialize_service", autospec=True)
@patch("chaosgcp.iam.controls.policy.get_policy", autospec=True)
@patch("chaosgcp.iam.controls.policy.set_policy", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_before_experiment_control(
    initialize_service, get_policy, set_policy, Credentials
):
    initialize_service.return_value = MagicMock()
    set_policy.return_value = MagicMock()
    get_policy.return_value = MagicMock()
    mycontext = {"title": "iampolicytest"}
    imported_policy.before_experiment_control(
        context=mycontext,
        project_id="myprojectid",
        roles=["roles/editor"],
        members=["user:owner@example.com"],
        configuration=fixtures.configuration,
        iam_propogation_sleep_time_in_minutes=0,
        expiry_time_in_minutes=0,
    )


@patch("chaosgcp.iam.controls.policy.initialize_service", autospec=True)
@patch("chaosgcp.iam.controls.policy.get_policy", autospec=True)
@patch("chaosgcp.iam.controls.policy.set_policy", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_after_experiment_control(
    initialize_service, get_policy, set_policy, Credentials
):
    initialize_service.return_value = MagicMock()
    set_policy.return_value = MagicMock()
    get_policy.return_value = MagicMock()
    mycontext = {"title": "iampolicytest"}
    mystate = {"status": "succeeded"}
    imported_policy.after_experiment_control(
        context=mycontext,
        state=mystate,
        project_id="myprojectid",
        roles=["roles/editor"],
        members=["user:owner@example.com"],
        configuration=fixtures.configuration,
        iam_propogation_sleep_time_in_minutes=0,
        expiry_time_in_minutes=0,
    )

