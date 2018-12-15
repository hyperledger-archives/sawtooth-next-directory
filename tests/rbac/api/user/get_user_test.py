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
""" Get User Test
"""

import requests
import pytest

from rbac.common.logs import getLogger

from tests.rbac import helper
from tests.rbac.api.assertions import assert_api_success
from tests.rbac.api.assertions import assert_api_get_requires_auth
from tests.rbac.api.config import api_wait

LOGGER = getLogger(__name__)


@pytest.mark.skip("Getting an intermittent index out of bound error")
@pytest.mark.api
@pytest.mark.api_user
def test_api_user_get_self():
    """ Test a user getting their self
    """
    user = helper.api.user.current
    url = helper.api.user.get_url(user_id=user["user_id"])
    assert assert_api_get_requires_auth(url)
    api_wait()  # temporary, see config
    response = requests.get(url=url, headers={"Authorization": user["token"]})
    result = assert_api_success(response)
    assert result["data"]["email"] == user["email"]
    assert result["data"]["name"] == user["name"]


@pytest.mark.skip("Getting an intermittent index out of bound error")
@pytest.mark.api
@pytest.mark.api_user
def test_api_user_get_other():
    """ Test a user getting another user's data
    """
    other = helper.api.user.current
    user = helper.api.user.current2
    url = helper.api.user.get_url(user_id=other["user_id"])
    assert assert_api_get_requires_auth(url)
    api_wait()  # temporary, see config
    response = requests.get(url=url, headers={"Authorization": user["token"]})
    result = assert_api_success(response)
    assert result["data"]["email"] == other["email"]
    assert result["data"]["name"] == other["name"]
