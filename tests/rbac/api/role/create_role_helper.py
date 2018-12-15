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
""" A test helper class that provides API users
"""

import random
import requests


from tests.rbac.api.base.base_helper import BaseApiHelper
from tests.rbac.api.user.user_helper import UserTestHelper
from tests.rbac.api.assertions import assert_api_success
from tests.rbac.api.config import api_wait


# pylint: disable=too-few-public-methods
class StubTestHelper(BaseApiHelper):
    """ A minimal test helper required by this test helper
    """

    def __init__(self):
        super().__init__()
        self.user = UserTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class CreateRoleTestHelper(BaseApiHelper):
    """ A test helper class that provides API users
    """

    def __init__(self):
        super().__init__()
        self._current = None

    @property
    def url(self):
        """ Create Role endpoint """
        return self.url_base + "/api/roles/"

    def name(self):
        """ Get a random name """
        return "Role" + str(random.randint(1000, 10000))

    def new(self, user):
        """ Create a test role, assigned to user current if no user is supplied """
        if not user:
            user = helper.user.current
        data = {
            "name": self.name(),
            "owners": [user["user_id"]],
            "administrators": [user["user_id"]],
        }
        response = requests.post(
            url=self.url, headers={"Authorization": user["token"]}, json=data
        )
        result = assert_api_success(response)
        assert result["data"]["name"] == data["name"]
        assert result["data"]["owners"] == data["owners"]
        return result["data"]

    @property
    def current(self):
        """ A created role with the currently authenticated owner
        """
        if not self._current:
            owner = helper.user.create.authenticated()
            role = self.new(user=owner)
            self._current = (role, owner)
            api_wait()  # temporary, see config
        return self._current
