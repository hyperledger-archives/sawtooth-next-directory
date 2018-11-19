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
"""Propose Task Add Admin Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.task
class ProposeTaskAddAdminTest(TestAssertions):
    """Propose Task Add Admin Test"""

    @pytest.mark.library
    def test_make(self):
        """Test making the message"""
        user_id = helper.user.id()
        task_id = helper.task.id()
        reason = helper.proposal.reason()
        message = rbac.task.admin.propose.make(
            user_id=user_id, task_id=task_id, reason=reason, metadata=None
        )
        self.assertIsInstance(
            message, protobuf.task_transaction_pb2.ProposeAddTaskAdmin
        )
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.task_id, task_id)
        self.assertEqual(message.reason, reason)

    @pytest.mark.library
    def test_make_addresses(self):
        """Test making the message addresses"""
        user_id = helper.user.id()
        user_address = rbac.user.address(user_id)
        task_id = helper.task.id()
        task_address = rbac.task.address(task_id)
        reason = helper.proposal.reason()
        relationship_address = rbac.task.admin.address(task_id, user_id)
        proposal_address = rbac.task.admin.propose.address(task_id, user_id)
        signer_keypair = helper.user.key()
        message = rbac.task.admin.propose.make(
            user_id=user_id, task_id=task_id, reason=reason, metadata=None
        )

        inputs, outputs = rbac.task.admin.propose.make_addresses(
            message=message, signer_keypair=signer_keypair
        )

        self.assertIsInstance(inputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(task_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 4)

        self.assertIsInstance(outputs, list)
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.library
    def test_make_payload(self):
        """Test making the message payload"""
        user_id = helper.user.id()
        user_address = rbac.user.address(user_id)
        task_id = helper.task.id()
        task_address = rbac.task.address(task_id)
        reason = helper.proposal.reason()
        relationship_address = rbac.task.admin.address(task_id, user_id)
        proposal_address = rbac.task.admin.propose.address(task_id, user_id)
        signer_keypair = helper.user.key()
        message = rbac.task.admin.propose.make(
            user_id=user_id, task_id=task_id, reason=reason, metadata=None
        )

        payload = rbac.task.admin.propose.make_payload(
            message=message, signer_keypair=signer_keypair
        )
        self.assertIsInstance(payload, protobuf.rbac_payload_pb2.RBACPayload)

        inputs = list(payload.inputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(task_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 4)

        outputs = list(payload.outputs)
        self.assertIsInstance(outputs, list)
        self.assertEqual(outputs, [proposal_address])

    def test_create(self):
        """Test executing the message on the blockchain"""
        task, _, _ = helper.task.create()
        reason = helper.proposal.reason()
        user, signer_keypair = helper.user.create()

        message = rbac.task.admin.propose.make(
            user_id=user.user_id, task_id=task.task_id, reason=reason, metadata=None
        )
        proposal, status = rbac.task.admin.propose.create(
            signer_keypair=signer_keypair,
            message=message,
            object_id=task.task_id,
            target_id=user.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_TASK_ADMIN
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, task.task_id)
        self.assertEqual(proposal.target_id, user.user_id)
        self.assertEqual(proposal.opener, signer_keypair.public_key)
        self.assertEqual(proposal.open_reason, reason)
