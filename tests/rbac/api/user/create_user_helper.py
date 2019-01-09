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
""" Create User Test Helper
"""

import requests

from tests.rbac.api.base.base_helper import BaseApiHelper
from tests.rbac.api.assertions import assert_api_success
from tests.rbac.testdata.user import UserTestData
from tests.rbac.api.config import api_wait


class CreateUserTestHelper(BaseApiHelper, UserTestData):
    """ Create User Test Helper
    """

    def __init__(self):
        super().__init__()
        self._current = None
        self._current2 = None

    @property
    def url(self):
        """ Create User endpoint
        """
        return self.url_base + "/api/users/"

    @property
    def auth_url(self):
        """ User login endpoint
        """
        return self.url_base + "/api/authorization/"

    @property
    def current(self):
        """ A currently authenticated user
        """
        if not self._current:
            self._current = self.authenticated()
        return self._current

    @property
    def current2(self):
        """ Another currently authenticated user
            unrelated to current. Tests should not
            establish a relationship.
        """
        if not self._current2:
            self._current2 = self.authenticated()
        return self._current2

    def new(self, manager_id=None):
        """ Provides a created test user
        """
        data = {
            "name": self.name(),
            "username": self.username(),
            "email": self.email(),
            "password": self.password(),
            "manager": manager_id,
        }
        response = requests.post(url=self.url, headers=None, json=data)
        result = assert_api_success(response)
        assert result["data"]["message"] == "Authorization successful"
        return data

    def authenticated(self, user=None):
        """ Provides newly created test user with authentication token
        """
        if not user:
            user = self.new()
            api_wait()  # temporary, see config
        data = {"id": user["username"], "password": user["password"]}
        response = requests.post(url=self.auth_url, headers=None, json=data)
        result = assert_api_success(response)
        assert result["data"]["message"] == "Authorization successful"
        user["user_id"] = result["data"]["user_id"]
        user["token"] = result["token"]
        return user
