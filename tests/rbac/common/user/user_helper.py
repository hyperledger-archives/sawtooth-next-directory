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

import logging

from tests.rbac.common.user.create_user_helper import CreateUserTestHelper
from tests.rbac.common.user.propose_manager_helper import ProposeManagerTestHelper

LOGGER = logging.getLogger(__name__)


class UserManangerTestHelper:
    def __init__(self):
        self.propose = ProposeManagerTestHelper()


class UserTestHelper:
    def __init__(self):
        self.create_user = CreateUserTestHelper()
        self.manager = UserManangerTestHelper()

    def id(self):
        return self.create_user.id()

    def name(self):
        return self.create_user.name()

    def username(self):
        return self.create_user.username()

    def reason(self):
        return self.create_user.reason()

    def message(self):
        return self.create_user.message()

    def message_with_manager(self):
        return self.create_user.message_with_manager()

    def create(self):
        return self.create_user.create()

    def create_with_manager(self):
        return self.create_user.create_with_manager()

    def create_with_grand_manager(self):
        return self.create_user.create_with_grand_manager()
