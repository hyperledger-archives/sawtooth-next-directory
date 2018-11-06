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

import pytest
import logging
from uuid import uuid4

from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.task.task_manager import TaskManager
from tests.rbac.common.task.task_test_helper import TaskTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.task
class CreateTaskTest(TaskTestHelper):
    def __init__(self, *args, **kwargs):
        TaskTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.task, TaskManager)
        self.assertTrue(callable(self.task.address))
        self.assertTrue(callable(self.task.make))
        self.assertTrue(callable(self.task.make_addresses))
        self.assertTrue(callable(self.task.make_payload))
        self.assertTrue(callable(self.task.create))
        self.assertTrue(callable(self.task.send))
        self.assertTrue(callable(self.task.get))

    @pytest.mark.unit
    def test_helper_interface(self):
        """Verify the expected user test helper interface"""
        self.assertTrue(callable(self.get_testdata_name))
        self.assertTrue(callable(self.get_testdata_username))
        self.assertTrue(callable(self.get_testdata_user))
        self.assertTrue(callable(self.get_testdata_user_with_key))
        self.assertTrue(callable(self.get_testdata_reason))
        self.assertTrue(callable(self.get_testdata_user_created))
        self.assertTrue(callable(self.get_testdata_user_created_with_manager))
        self.assertTrue(callable(self.get_testdata_taskname))
        self.assertTrue(callable(self.get_testdata_task))
        self.assertTrue(callable(self.get_testunit_user_task))
        self.assertTrue(callable(self.get_testdata_user_task))

    @pytest.mark.unit
    @pytest.mark.address
    def test_address(self):
        """Test the address method and that it is in sync with the addresser"""
        self.assertTrue(callable(self.task.address))

        task = self.get_testdata_task()
        self.assertIsInstance(task, protobuf.task_transaction_pb2.CreateTask)
        self.assertIsInstance(task.task_id, str)
        address1 = self.task.address(object_id=task.task_id)
        address2 = addresser.task.address(task.task_id)
        self.assertEqual(address1, address2)

    @pytest.mark.unit
    def test_make(self):
        """Test getting a test data user with keys"""
        self.assertTrue(callable(self.task.make))
        name = self.get_testdata_taskname()
        task_id = uuid4().hex
        message = self.task.make(task_id=task_id, name=name)
        self.assertIsInstance(message, protobuf.task_transaction_pb2.CreateTask)
        self.assertIsInstance(message.task_id, str)
        self.assertIsInstance(message.name, str)
        self.assertEqual(message.task_id, task_id)
        self.assertEqual(message.name, name)

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test the make addresses method for a CreateTask message"""
        self.assertTrue(callable(self.task.make_addresses))
        self.assertTrue(callable(self.get_testdata_user_with_key))
        self.assertTrue(callable(self.get_testdata_task))

        message, user, _ = self.get_testunit_user_task()
        inputs, outputs = self.task.make_addresses(message=message)

        task_address = addresser.task.address(message.task_id)
        user_address = addresser.user.address(user.user_id)
        owner_address = addresser.task.owner.address(message.task_id, user.user_id)
        admin_address = addresser.task.admin.address(message.task_id, user.user_id)

        self.assertIsInstance(inputs, list)
        self.assertIn(task_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(owner_address, inputs)
        self.assertIn(admin_address, inputs)
        # self.assertEqual(len(inputs), 5)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making a payload for a CreateTask message"""
        self.assertTrue(callable(self.task.make_payload))
        self.assertTrue(callable(self.get_testdata_user_with_key))
        self.assertTrue(callable(self.get_testdata_task))

        message, user, _ = self.get_testunit_user_task()
        payload = self.task.make_payload(message=message)
        self.assertEqual(payload.message_type, RBACPayload.CREATE_TASK)

        task_address = addresser.task.address(message.task_id)
        user_address = addresser.user.address(user.user_id)
        owner_address = addresser.task.owner.address(message.task_id, user.user_id)
        admin_address = addresser.task.admin.address(message.task_id, user.user_id)

        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(task_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(owner_address, inputs)
        self.assertIn(admin_address, inputs)
        # self.assertEqual(len(inputs), 5)
        self.assertEqual(inputs, outputs)

    @pytest.mark.integration
    def test_create(self, task=None, user=None, keypair=None):
        """Test creating a task"""
        self.assertTrue(callable(self.task.create))
        self.assertTrue(callable(self.get_testdata_user_task))

        if user is None and task is None:
            task, user, keypair = self.get_testdata_user_task()
        if user is None:
            user, keypair = self.get_testdata_user_created()
        if task is None:
            task = self.get_testdata_task()
            task.admins = [user.user_id]
            task.owners = [user.user_id]
        self.assertIsInstance(task, protobuf.task_transaction_pb2.CreateTask)

        got, status = self.task.create(
            signer_keypair=keypair, message=task, object_id=task.task_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, task, self.task.message_fields_not_in_state)
        self.assertTrue(
            self.task.owner.exists(object_id=task.task_id, target_id=user.user_id)
        )
        self.assertTrue(
            self.task.admin.exists(object_id=task.task_id, target_id=user.user_id)
        )
        # self.assertFalse(
        #    self.task.member.exists(object_id=task.task_id, target_id=user.user_id)
        # )
        return got, user, keypair
