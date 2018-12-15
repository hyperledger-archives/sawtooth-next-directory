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
""" User Test Helper
"""
from tests.rbac.api.base.base_helper import BaseApiHelper
from tests.rbac.api.user.create_user_helper import CreateUserTestHelper
from tests.rbac.testdata.user import UserTestData


class UserTestHelper(UserTestData, BaseApiHelper):
    """ User Test Helper
    """

    def __init__(self):
        super().__init__()
        self.create = CreateUserTestHelper()

    def get_url(self, user_id):
        """ User get endpoint """
        return self.url_base + "/api/users/{}".format(user_id)

    @property
    def list_url(self):
        """ Users get all endpoint """
        return self.url_base + "/api/users/"

    @property
    def current(self):
        """ A currently authenticated user """
        return self.create.current

    @property
    def current2(self):
        """ Another currently authenticated user
            unrelated to current. Tests should not
            establish a relationship.
        """
        return self.create.current2
