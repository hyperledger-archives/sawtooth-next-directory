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

import logging
import pytest

from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from rbac.common.user.manager import Manager
from rbac.common.user.reject_manager import RejectUpdateUserManager
from tests.rbac.common.manager.test_base import TestBase

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class RejectManagerTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.rbac.user, UserManager)
        self.assertIsInstance(self.rbac.user.manager, Manager)
        self.assertIsInstance(self.rbac.user.manager.reject, RejectUpdateUserManager)
        self.assertTrue(callable(self.rbac.user.manager.reject.address))
        self.assertTrue(callable(self.rbac.user.manager.reject.make))
        self.assertTrue(callable(self.rbac.user.manager.reject.make_addresses))
        self.assertTrue(callable(self.rbac.user.manager.reject.make_payload))
        self.assertTrue(callable(self.rbac.user.manager.reject.create))
        self.assertTrue(callable(self.rbac.user.manager.reject.send))
        self.assertTrue(callable(self.rbac.user.manager.reject.get))

    @pytest.mark.unit
    def test_make(self):
        """Test making the message"""
        self.assertTrue(callable(self.rbac.user.manager.reject.make))
        user_id = self.test.user.id()
        manager_id = self.test.user.id()
        reason = self.test.user.manager.propose.reason()
        proposal_id = self.test.user.manager.propose.id()
        message = self.rbac.user.manager.reject.make(
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

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.rbac.user.manager.reject.make_addresses))
        user_id = self.test.user.id()
        manager_id = self.test.user.id()
        reason = self.test.user.manager.propose.reason()
        proposal_id = self.test.user.manager.propose.id()
        proposal_address = self.rbac.user.manager.reject.address(
            object_id=user_id, target_id=manager_id
        )
        message = self.rbac.user.manager.reject.make(
            proposal_id=proposal_id,
            user_id=user_id,
            manager_id=manager_id,
            reason=reason,
        )

        inputs, outputs = self.rbac.user.manager.reject.make_addresses(message=message)

        self.assertEqual(inputs, [proposal_address])
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.rbac.user.manager.reject.make_payload))
        user_id = self.test.user.id()
        manager_id = self.test.user.id()
        reason = self.test.user.manager.propose.reason()
        proposal_id = self.test.user.manager.propose.id()
        proposal_address = self.rbac.user.manager.reject.address(
            object_id=user_id, target_id=manager_id
        )
        message = self.rbac.user.manager.reject.make(
            proposal_id=proposal_id,
            user_id=user_id,
            manager_id=manager_id,
            reason=reason,
        )

        payload = self.rbac.user.manager.reject.make_payload(message=message)

        self.assertIsInstance(payload, RBACPayload)
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
        self.assertTrue(callable(self.rbac.user.manager.reject.create))
        proposal, user, user_key, manager, manager_key = (
            self.test.user.manager.propose.create()
        )

        reason = self.test.user.manager.propose.reason()
        message = self.rbac.user.manager.reject.make(
            proposal_id=proposal.proposal_id,
            user_id=proposal.object_id,
            manager_id=proposal.target_id,
            reason=reason,
        )
        reject, status = self.rbac.user.manager.reject.create(
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
