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
""" Create User Test
"""
# pylint: disable=invalid-name

import requests
import pytest

from rbac.common.logs import get_logger

from tests.rbac import helper
from tests.rbac.api.assertions import assert_api_success

LOGGER = get_logger(__name__)


@pytest.mark.api
@pytest.mark.api_user
@pytest.mark.api_create_user
@pytest.mark.parametrize(
    "data",
    [
        (
            {
                "name": helper.api.user.create.name(),
                "username": helper.api.user.create.username(),
                "email": helper.api.user.create.email(),
                "password": helper.api.user.create.password(),
            }
        )
    ],
)
def test_api_create_user(data):
    """ Test creating a user
    """
    url = helper.api.user.create.url
    response = requests.post(url=url, headers=None, json=data)
    result = assert_api_success(response)
    assert result["data"]
    assert result["data"]["message"] == "Authorization successful"
    assert isinstance(result["data"]["user"], dict)
    assert result["data"]["user"]["email"] == data["email"]
    assert result["data"]["user"]["username"] == data["username"]
    assert result["data"]["user"]["name"] == data["name"]
    assert "password" not in result["data"]["user"]
    if "manager" in data:
        assert result["data"]["user"]["manager"] == data["manager"]


@pytest.mark.api
@pytest.mark.api_user
@pytest.mark.api_create_user
@pytest.mark.parametrize(
    "data",
    [
        (
            {
                "name": helper.api.user.create.name(),
                "username": helper.api.user.create.username(),
                "email": helper.api.user.create.email(),
                "password": helper.api.user.create.password(),
            }
        )
    ],
)
def test_api_create_user_with_manager(data):
    """ Test creating a user
    """
    url = helper.api.user.create.url
    data["manager"] = helper.api.user.current["user_id"]
    response = requests.post(url=url, headers=None, json=data)
    result = assert_api_success(response)
    assert result["data"]
    assert result["data"]["message"] == "Authorization successful"
    assert isinstance(result["data"]["user"], dict)
    assert result["data"]["user"]["email"] == data["email"]
    assert result["data"]["user"]["username"] == data["username"]
    assert result["data"]["user"]["name"] == data["name"]
    assert "password" not in result["data"]["user"]
    assert result["data"]["user"]["manager"] == data["manager"]
