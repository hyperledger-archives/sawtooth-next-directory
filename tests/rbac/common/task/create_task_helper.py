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
"""Create Task Test Helper"""
# pylint: disable=no-member,too-few-public-methods

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper

LOGGER = logging.getLogger(__name__)


class StubTestHelper:
    """A minimal test helper required by this test helper"""

    def __init__(self):
        self.user = CreateUserTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class CreateTaskTestHelper:
    """Create Task Test Helper"""

    def id(self):
        """Get a test task_id (not created)"""
        return rbac.addresser.task.unique_id()

    def name(self):
        """Get a random name"""
        return "Task" + str(random.randint(1000, 10000))

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def message(self):
        """Get a test data CreateTask message"""
        task_id = self.id()
        name = self.name()
        user_id = helper.user.id()
        message = rbac.task.make(
            task_id=task_id, name=name, owners=[user_id], admins=[user_id]
        )
        assert isinstance(message, protobuf.task_transaction_pb2.CreateTask)
        assert message.task_id == task_id
        assert message.name == name
        return message

    def create(self):
        """Create a test task"""
        task_id = self.id()
        name = self.name()
        user, keypair = helper.user.create()
        message = rbac.task.make(
            task_id=task_id, name=name, owners=[user.user_id], admins=[user.user_id]
        )

        status = rbac.task.new(signer_keypair=keypair, message=message)

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        task = rbac.task.get(object_id=message.task_id)

        assert task.task_id == message.task_id
        assert task.name == message.name
        assert rbac.task.owner.exists(object_id=task.task_id, related_id=user.user_id)
        assert rbac.task.admin.exists(object_id=task.task_id, related_id=user.user_id)
        return task, user, keypair
