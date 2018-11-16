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
"""Test Propose Role Task Helper"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions


LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class ProposeRoleTaskHelperTest(TestAssertions):
    """Test Propose Role Task Helper"""

    @pytest.mark.library
    def test_id(self):
        """Test get a random proposal id"""
        id1 = helper.role.task.propose.id()
        id2 = helper.role.task.propose.id()
        self.assertIsInstance(id1, str)
        self.assertIsInstance(id2, str)
        self.assertEqual(len(id1), 24)
        self.assertEqual(len(id2), 24)
        self.assertNotEqual(id1, id2)

    @pytest.mark.library
    def test_reason(self):
        """Test get a random reason"""
        reason1 = helper.role.task.propose.reason()
        reason2 = helper.role.task.propose.reason()
        self.assertIsInstance(reason1, str)
        self.assertIsInstance(reason2, str)
        self.assertGreater(len(reason1), 4)
        self.assertGreater(len(reason2), 4)
        self.assertNotEqual(reason1, reason2)

    @pytest.mark.integration
    def test_create(self):
        """A role owner creates an add role task proposal
        to add a task to their role"""
        proposal, role, role_owner, role_owner_key, task, task_owner, task_owner_key = (
            helper.role.task.propose.create()
        )
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertIsInstance(role, protobuf.role_state_pb2.RoleAttributes)
        self.assertIsInstance(task, protobuf.task_state_pb2.TaskAttributes)
        self.assertIsInstance(role_owner, protobuf.user_state_pb2.User)
        self.assertIsInstance(task_owner, protobuf.user_state_pb2.User)
        self.assertIsInstance(role_owner_key, Key)
        self.assertIsInstance(task_owner_key, Key)
        self.assertEqual(proposal.object_id, role.role_id)
        self.assertEqual(proposal.target_id, task.task_id)
