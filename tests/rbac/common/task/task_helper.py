# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Task Test Helper Class"""
# pylint: disable=no-member,too-few-public-methods,invalid-name
from rbac.common.logs import get_default_logger
from tests.rbac.common.task.create_task_helper import CreateTaskTestHelper
from tests.rbac.common.task.propose_admin_helper import ProposeTaskAdminTestHelper
from tests.rbac.common.task.propose_owner_helper import ProposeTaskOwnerTestHelper

LOGGER = get_default_logger(__name__)


class TaskAdminTestHelper:
    """Task Test Helper Admin Class"""

    def __init__(self):
        """Task Test Helper Admin Class"""
        self.propose = ProposeTaskAdminTestHelper()


class TaskOwnerTestHelper:
    """Task Test Helper Owner Class"""

    def __init__(self):
        """Task Test Helper Owner Class"""
        self.propose = ProposeTaskOwnerTestHelper()


class TaskTestHelper:
    """Task Test Helper Class"""

    def __init__(self):
        """Task Test Helper Class"""
        self.create_task = CreateTaskTestHelper()
        self.admin = TaskAdminTestHelper()
        self.owner = TaskOwnerTestHelper()

    def id(self):
        """Return a unique identifier"""
        return self.create_task.id()

    def name(self):
        """Return a random name"""
        return self.create_task.name()

    def reason(self):
        """Return a random reason"""
        return self.create_task.reason()

    def message(self):
        """Make a task create message"""
        return self.create_task.message()

    def create(self):
        """Create a test task"""
        return self.create_task.create()
