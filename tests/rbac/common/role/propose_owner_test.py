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
"""Propose Role Add Owner Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class ProposeRoleAddOwnerTest(TestAssertions):
    """Propose Role Add Owner Test"""

    @pytest.mark.library
    def test_make(self):
        """Test making the message"""
        user_id = helper.user.id()
        role_id = helper.role.id()
        reason = helper.proposal.reason()
        message = rbac.role.owner.propose.make(
            user_id=user_id, role_id=role_id, reason=reason, metadata=None
        )
        self.assertIsInstance(
            message, protobuf.role_transaction_pb2.ProposeAddRoleOwner
        )
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.role_id, role_id)
        self.assertEqual(message.reason, reason)

    @pytest.mark.library
    def test_make_addresses(self):
        """Test making the message addresses"""
        user_id = helper.user.id()
        user_address = rbac.user.address(user_id)
        role_id = helper.role.id()
        role_address = rbac.role.address(role_id)
        reason = helper.proposal.reason()
        relationship_address = rbac.role.owner.address(role_id, user_id)
        proposal_address = rbac.role.owner.propose.address(role_id, user_id)
        signer_keypair = helper.user.key()
        message = rbac.role.owner.propose.make(
            user_id=user_id, role_id=role_id, reason=reason, metadata=None
        )

        inputs, outputs = rbac.role.owner.propose.make_addresses(
            message=message, signer_keypair=signer_keypair
        )

        self.assertIsInstance(inputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 4)

        self.assertIsInstance(outputs, list)
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.library
    def test_make_payload(self):
        """Test making the message payload"""
        user_id = helper.user.id()
        user_address = rbac.user.address(user_id)
        role_id = helper.role.id()
        role_address = rbac.role.address(role_id)
        reason = helper.proposal.reason()
        relationship_address = rbac.role.owner.address(role_id, user_id)
        proposal_address = rbac.role.owner.propose.address(role_id, user_id)
        signer_keypair = helper.user.key()
        message = rbac.role.owner.propose.make(
            user_id=user_id, role_id=role_id, reason=reason, metadata=None
        )

        payload = rbac.role.owner.propose.make_payload(
            message=message, signer_keypair=signer_keypair
        )
        self.assertIsInstance(payload, protobuf.rbac_payload_pb2.RBACPayload)

        inputs = list(payload.inputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 4)

        outputs = list(payload.outputs)
        self.assertIsInstance(outputs, list)
        self.assertEqual(outputs, [proposal_address])

    def test_create(self):
        """Test executing the message on the blockchain"""
        role, _, _ = helper.role.create()
        reason = helper.proposal.reason()
        user, signer_keypair = helper.user.create()

        message = rbac.role.owner.propose.make(
            user_id=user.user_id, role_id=role.role_id, reason=reason, metadata=None
        )
        proposal, status = rbac.role.owner.propose.create(
            signer_keypair=signer_keypair,
            message=message,
            object_id=role.role_id,
            target_id=user.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_OWNER
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, role.role_id)
        self.assertEqual(proposal.target_id, user.user_id)
        self.assertEqual(proposal.opener, signer_keypair.public_key)
        self.assertEqual(proposal.open_reason, reason)
