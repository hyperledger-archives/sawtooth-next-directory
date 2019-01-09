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
""" User Login Test
"""
# pylint: disable=invalid-name,redefined-outer-name,unused-import

import requests
import pytest

from rbac.common.logs import get_logger

from tests.rbac import helper
from tests.rbac.api.assertions import assert_api_error
from tests.rbac.api.assertions import assert_api_success

LOGGER = get_logger(__name__)


@pytest.mark.api
@pytest.mark.api_user
@pytest.mark.api_user_login
def test_api_user_login():
    """ Test user login with good data
    """
    url = helper.api.user.create.auth_url
    user = helper.api.user.create.current
    data = {"id": user["username"], "password": user["password"]}
    response = requests.post(url=url, headers=None, json=data)
    result = assert_api_success(response)
    assert result["data"]
    assert result["data"]["message"] == "Authorization successful"
    assert isinstance(result["data"]["user_id"], str)
    assert isinstance(result["token"], str)


@pytest.mark.api
@pytest.mark.api_user
@pytest.mark.parametrize(
    "data, message, status_code",
    [
        (
            {"password": helper.api.user.password()},
            "Bad Request: id field is required",
            400,
        ),
        (
            {"id": helper.api.user.username()},
            "Bad Request: password field is required",
            400,
        ),
        (
            {"id": helper.api.user.username(), "password": helper.api.user.password()},
            "No user with username '{}' exists.".format(helper.api.user.last_username),
            404,
        ),
    ],
)
def test_api_user_login_bad_data(data, message, status_code):
    """ Test user login with bad data
    """
    url = helper.api.user.create.auth_url
    response = requests.post(url=url, headers=None, json=data)
    assert assert_api_error(response, message, status_code)


@pytest.mark.api
@pytest.mark.api_user
def test_api_user_login_bad_password():
    """ Test user login with the wrong password
    """
    url = helper.api.user.create.auth_url
    user = helper.api.user.current
    data = {"id": user["username"], "password": "oops" + user["password"]}
    response = requests.post(url=url, headers=None, json=data)
    assert assert_api_error(response, "Unauthorized: Incorrect password", 401)
