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
"""Propose Role Add Task Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class ProposeRoleAddTaskTest(TestAssertions):
    """Propose Role Add Task Test"""

    @pytest.mark.library
    def test_make(self):
        """Test making the message"""
        task_id = helper.task.id()
        role_id = helper.role.id()
        reason = helper.proposal.reason()
        message = rbac.role.task.propose.make(
            task_id=task_id, role_id=role_id, reason=reason, metadata=None
        )
        self.assertIsInstance(message, protobuf.role_transaction_pb2.ProposeAddRoleTask)
        self.assertEqual(message.task_id, task_id)
        self.assertEqual(message.role_id, role_id)
        self.assertEqual(message.reason, reason)

    @pytest.mark.library
    def test_make_addresses(self):
        """Test making the message addresses"""
        task_id = helper.task.id()
        task_address = rbac.task.address(task_id)
        role_id = helper.role.id()
        role_address = rbac.role.address(role_id)
        reason = helper.proposal.reason()
        relationship_address = rbac.role.task.address(role_id, task_id)
        proposal_address = rbac.role.task.propose.address(role_id, task_id)
        role_owner_keypair = helper.user.key()
        role_owner_address = rbac.role.owner.address(
            role_id, role_owner_keypair.public_key
        )
        message = rbac.role.task.propose.make(
            task_id=task_id, role_id=role_id, reason=reason, metadata=None
        )

        inputs, outputs = rbac.role.task.propose.make_addresses(
            message=message, signer_keypair=role_owner_keypair
        )

        self.assertIsInstance(inputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(task_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(role_owner_address, inputs)
        self.assertEqual(len(inputs), 5)

        self.assertIsInstance(outputs, list)
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.library
    def test_make_payload(self):
        """Test making the message payload"""
        task_id = helper.task.id()
        task_address = rbac.task.address(task_id)
        role_id = helper.role.id()
        role_address = rbac.role.address(role_id)
        reason = helper.proposal.reason()
        relationship_address = rbac.role.task.address(role_id, task_id)
        proposal_address = rbac.role.task.propose.address(role_id, task_id)
        role_owner_keypair = helper.user.key()
        role_owner_address = rbac.role.owner.address(
            role_id, role_owner_keypair.public_key
        )
        message = rbac.role.task.propose.make(
            task_id=task_id, role_id=role_id, reason=reason, metadata=None
        )

        payload = rbac.role.task.propose.make_payload(
            message=message, signer_keypair=role_owner_keypair
        )
        self.assertIsInstance(payload, protobuf.rbac_payload_pb2.RBACPayload)

        inputs = list(payload.inputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(task_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(role_owner_address, inputs)
        self.assertEqual(len(inputs), 5)

        outputs = list(payload.outputs)
        self.assertIsInstance(outputs, list)
        self.assertEqual(outputs, [proposal_address])

    def test_create(self):
        """Test executing the message on the blockchain"""
        role, _, role_owner_key = helper.role.create()
        reason = helper.proposal.reason()
        task, _, _ = helper.task.create()

        message = rbac.role.task.propose.make(
            task_id=task.task_id, role_id=role.role_id, reason=reason, metadata=None
        )
        proposal, status = rbac.role.task.propose.create(
            signer_keypair=role_owner_key,
            message=message,
            object_id=role.role_id,
            target_id=task.task_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_TASK
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, role.role_id)
        self.assertEqual(proposal.target_id, task.task_id)
        self.assertEqual(proposal.opener, role_owner_key.public_key)
        self.assertEqual(proposal.open_reason, reason)
