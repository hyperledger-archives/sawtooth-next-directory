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
# pylint: disable=no-member

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.assertions import TestAssertions
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper

LOGGER = logging.getLogger(__name__)


class TestHelper(TestAssertions):
    """A minimal test helper required by this test helper"""

    def __init__(self, *args, **kwargs):
        TestAssertions.__init__(self, *args, **kwargs)
        self.user = CreateUserTestHelper()


# pylint: disable=invalid-name
helper = TestHelper()


class CreateTaskTestHelper(TestAssertions):
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
        message = rbac.task.make(task_id=task_id, name=name)
        self.assertIsInstance(message, protobuf.task_transaction_pb2.CreateTask)
        self.assertEqual(message.task_id, task_id)
        self.assertEqual(message.name, name)
        return message

    def create(self):
        """Create a test task"""
        user, keypair = helper.user.create()
        message = self.message()
        message.admins.extend([user.user_id])
        message.owners.extend([user.user_id])

        task, status = rbac.task.create(
            signer_keypair=keypair, message=message, object_id=message.task_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(task, message, rbac.task.message_fields_not_in_state)
        self.assertTrue(
            rbac.task.owner.exists(object_id=task.task_id, target_id=user.user_id)
        )
        self.assertTrue(
            rbac.task.admin.exists(object_id=task.task_id, target_id=user.user_id)
        )
        return task, user, keypair
