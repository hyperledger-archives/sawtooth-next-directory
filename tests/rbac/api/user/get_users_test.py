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
""" Get Users Test
"""

import requests
import pytest

from rbac.common.logs import getLogger

from tests.rbac import helper
from tests.rbac.api.assertions import assert_api_success
from tests.rbac.api.assertions import assert_api_get_requires_auth

LOGGER = getLogger(__name__)


@pytest.mark.skip("Getting an intermittent index out of bound error")
@pytest.mark.api
@pytest.mark.api_user
def test_api_users_get_all():
    """ Test getting all users with default page settings. Test that:
    1. URL requires authorization
    2. Returns a list of data
    3. Returns at least one record
    """
    user = helper.api.user.current
    url = helper.api.user.list_url
    assert assert_api_get_requires_auth(url)
    response = requests.get(url=url, headers={"Authorization": user["token"]})
    result = assert_api_success(response)
    assert isinstance(result["data"], list)
    assert result["paging"]["total"] > 0
