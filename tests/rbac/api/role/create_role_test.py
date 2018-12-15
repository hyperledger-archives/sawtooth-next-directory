# Copyright 2018 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
""" Test role creation """

import requests
import pytest

from rbac.common.logs import getLogger

from tests.rbac import helper
from tests.rbac.api.assertions import assert_api_error
from tests.rbac.api.assertions import assert_api_success
from tests.rbac.api.assertions import assert_api_post_requires_auth

LOGGER = getLogger(__name__)


@pytest.mark.api
@pytest.mark.api_role
@pytest.mark.api_create_role
def test_api_create_role():
    """ Test creating a role
    """
    url = helper.api.role.create.url
    user = helper.api.user.current
    data = {
        "name": helper.api.role.name(),
        "owners": [user["user_id"]],
        "administrators": [user["user_id"]],
    }
    assert assert_api_post_requires_auth(url=url, json=data)
    response = requests.post(
        url=url, headers={"Authorization": user["token"]}, json=data
    )
    result = assert_api_success(response)
    assert result["data"]
    assert result["data"]["name"] == data["name"]
    assert result["data"]["owners"] == data["owners"]
    assert result["data"]["administrators"] == data["administrators"]


@pytest.mark.api
@pytest.mark.api_role
@pytest.mark.parametrize(
    "data, message, status_code",
    [
        (
            {
                "owners": [helper.api.user.id()],
                "administrators": [helper.api.user.id()],
            },
            "Bad Request: name field is required",
            400,
        ),
        (
            {"name": helper.api.role.name(), "administrators": [helper.api.user.id()]},
            "Bad Request: owners field is required",
            400,
        ),
        (
            {"name": helper.api.role.name(), "owners": [helper.api.user.id()]},
            "Bad Request: administrators field is required",
            400,
        ),
    ],
)
def test_api_user_create_bad(data, message, status_code):
    """ Test create role with bad data
    """
    user = helper.api.user.current
    url = helper.api.role.create.url
    response = requests.post(
        url=url, headers={"Authorization": user["token"]}, json=data
    )
    assert_api_error(response, message, status_code)
