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
"""Reject Manager Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class RejectManagerTest(TestAssertions):
    """Reject Manager Test"""

    @pytest.mark.library
    def test_make(self):
        """Test making the message"""
        user_id = helper.user.id()
        manager_id = helper.user.id()
        reason = helper.user.manager.propose.reason()
        proposal_id = helper.user.manager.propose.id()
        message = rbac.user.manager.reject.make(
            proposal_id=proposal_id,
            user_id=user_id,
            manager_id=manager_id,
            reason=reason,
        )
        self.assertIsInstance(
            message, protobuf.user_transaction_pb2.RejectUpdateUserManager
        )
        self.assertEqual(message.proposal_id, proposal_id)
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.manager_id, manager_id)
        self.assertEqual(message.reason, reason)

    @pytest.mark.library
    def test_make_addresses(self):
        """Test making a propose manager message"""
        user_id = helper.user.id()
        manager_id = helper.user.id()
        reason = helper.user.manager.propose.reason()
        proposal_id = helper.user.manager.propose.id()
        proposal_address = rbac.user.manager.reject.address(
            object_id=user_id, target_id=manager_id
        )
        message = rbac.user.manager.reject.make(
            proposal_id=proposal_id,
            user_id=user_id,
            manager_id=manager_id,
            reason=reason,
        )

        inputs, outputs = rbac.user.manager.reject.make_addresses(message=message)

        self.assertEqual(inputs, [proposal_address])
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.library
    def test_make_payload(self):
        """Test making a propose manager message"""
        user_id = helper.user.id()
        manager_id = helper.user.id()
        reason = helper.user.manager.propose.reason()
        proposal_id = helper.user.manager.propose.id()
        proposal_address = rbac.user.manager.reject.address(
            object_id=user_id, target_id=manager_id
        )
        message = rbac.user.manager.reject.make(
            proposal_id=proposal_id,
            user_id=user_id,
            manager_id=manager_id,
            reason=reason,
        )

        payload = rbac.user.manager.reject.make_payload(message=message)

        self.assertIsInstance(payload, protobuf.rbac_payload_pb2.RBACPayload)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertEqual(inputs, [proposal_address])
        self.assertEqual(outputs, [proposal_address])
        return payload

    @pytest.mark.integration
    def test_create(self):
        """Test rejecting a manager proposal"""
        proposal, _, _, _, manager_key = helper.user.manager.propose.create()

        reason = helper.user.manager.propose.reason()
        message = rbac.user.manager.reject.make(
            proposal_id=proposal.proposal_id,
            user_id=proposal.object_id,
            manager_id=proposal.target_id,
            reason=reason,
        )
        reject, status = rbac.user.manager.reject.create(
            signer_keypair=manager_key,
            message=message,
            object_id=proposal.object_id,
            target_id=proposal.target_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(reject, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            reject.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(reject.proposal_id, proposal.proposal_id)
        self.assertEqual(reject.object_id, proposal.object_id)
        self.assertEqual(reject.target_id, proposal.target_id)
        self.assertEqual(reject.close_reason, reason)
        self.assertEqual(reject.status, protobuf.proposal_state_pb2.Proposal.REJECTED)
