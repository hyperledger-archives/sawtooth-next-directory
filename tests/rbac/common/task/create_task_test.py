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
"""Create Task Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.task
class CreateTaskTest(TestAssertions):
    """Create Task Test"""

    @pytest.mark.library
    @pytest.mark.address
    def test_address(self):
        """Test the address method and that it is in sync with the addresser"""
        task_id = helper.task.id()
        address1 = rbac.task.address(object_id=task_id)
        address2 = rbac.addresser.task.address(task_id)
        self.assertEqual(address1, address2)

    @pytest.mark.library
    def test_make(self):
        """Test making a message"""
        name = helper.task.name()
        task_id = helper.task.id()
        user_id = helper.user.id()
        message = rbac.task.make(
            task_id=task_id, name=name, owners=[user_id], admins=[user_id]
        )
        self.assertIsInstance(message, protobuf.task_transaction_pb2.CreateTask)
        self.assertIsInstance(message.task_id, str)
        self.assertIsInstance(message.name, str)
        self.assertEqual(message.task_id, task_id)
        self.assertEqual(message.name, name)
        self.assertEqual(message.owners, [user_id])
        self.assertEqual(message.admins, [user_id])

    @pytest.mark.library
    def test_make_addresses(self):
        """Test the make addresses method for the message"""
        name = helper.task.name()
        task_id = helper.task.id()
        task_address = rbac.task.address(task_id)
        user_id = helper.user.id()
        user_address = rbac.user.address(user_id)
        owner_address = rbac.task.owner.address(task_id, user_id)
        admin_address = rbac.task.admin.address(task_id, user_id)
        message = rbac.task.make(
            task_id=task_id, name=name, owners=[user_id], admins=[user_id]
        )

        inputs, outputs = rbac.task.make_addresses(message=message)

        self.assertIsInstance(inputs, list)
        self.assertIn(task_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(owner_address, inputs)
        self.assertIn(admin_address, inputs)
        self.assertEqual(
            len(inputs), 5
        )  # user_address will appear twice, as owner and admin
        self.assertEqual(inputs, outputs)

    @pytest.mark.library
    def test_make_payload(self):
        """Test making a payload for a CreateTask message"""
        name = helper.task.name()
        task_id = helper.task.id()
        user_id = helper.user.id()
        task_address = rbac.task.address(task_id)
        user_address = rbac.user.address(user_id)
        owner_address = rbac.task.owner.address(task_id, user_id)
        admin_address = rbac.task.admin.address(task_id, user_id)
        message = rbac.task.make(
            task_id=task_id, name=name, owners=[user_id], admins=[user_id]
        )

        payload = rbac.task.make_payload(message=message)

        self.assertEqual(
            payload.message_type, protobuf.rbac_payload_pb2.RBACPayload.CREATE_TASK
        )
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(task_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(owner_address, inputs)
        self.assertIn(admin_address, inputs)
        self.assertEqual(
            len(inputs), 5
        )  # user_address will appear twice, as owner and admin
        self.assertEqual(inputs, outputs)

    @pytest.mark.integration
    def test_create(self):
        """Test creating a task"""
        user, keypair = helper.user.create()
        name = helper.task.name()
        task_id = helper.task.id()
        message = rbac.task.make(
            task_id=task_id, name=name, owners=[user.user_id], admins=[user.user_id]
        )

        task, status = rbac.task.create(
            signer_keypair=keypair, message=message, object_id=task_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(task, message, rbac.task.message_fields_not_in_state)
        self.assertTrue(
            rbac.task.owner.exists(object_id=task.task_id, target_id=user.user_id)
        )
        self.assertTrue(
            rbac.task.admin.exists(object_id=task.task_id, target_id=user.user_id)
        )
