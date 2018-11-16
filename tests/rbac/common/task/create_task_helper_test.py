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
"""Test Create Task Test Helper"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.task
class CreateTaskTestHelperTest(TestAssertions):
    """Test Create Task Test Helper"""

    @pytest.mark.library
    def test_id(self):
        """Test get a random task_id"""
        task_id1 = helper.task.id()
        task_id2 = helper.task.id()
        self.assertIsInstance(task_id1, str)
        self.assertIsInstance(task_id2, str)
        self.assertNotEqual(task_id1, task_id2)

    @pytest.mark.library
    def test_name(self):
        """Test get a random name"""
        name1 = helper.task.name()
        name2 = helper.task.name()
        self.assertIsInstance(name1, str)
        self.assertIsInstance(name2, str)
        self.assertGreater(len(name1), 4)
        self.assertGreater(len(name2), 4)
        self.assertNotEqual(name1, name2)

    @pytest.mark.library
    def test_reason(self):
        """Test get a random reason"""
        reason1 = helper.task.reason()
        reason2 = helper.task.reason()
        self.assertIsInstance(reason1, str)
        self.assertIsInstance(reason2, str)
        self.assertGreater(len(reason1), 4)
        self.assertGreater(len(reason2), 4)
        self.assertNotEqual(reason1, reason2)

    @pytest.mark.library
    def test_message(self):
        """Test getting a test create task message"""
        message = helper.task.message()
        self.assertIsInstance(message, protobuf.task_transaction_pb2.CreateTask)
        self.assertIsInstance(message.task_id, str)
        self.assertIsInstance(message.name, str)

    @pytest.mark.integration
    def test_create(self):
        """Test getting a created test task"""
        task, user, keypair = helper.task.create()
        self.assertIsInstance(task, protobuf.task_state_pb2.TaskAttributes)
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(task.task_id, str)
        self.assertIsInstance(task.name, str)
        self.assertIsInstance(keypair, Key)
