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
import random
from uuid import uuid4

from rbac.common import protobuf
from rbac.common.manager.rbac_manager import RBACManager
from tests.rbac.common.sawtooth.batch_assertions import BatchAssertions
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper

LOGGER = logging.getLogger(__name__)


class TestHelper(BatchAssertions):
    def __init__(self, *args, **kwargs):
        BatchAssertions.__init__(self, *args, **kwargs)
        self.user = CreateUserTestHelper()


class ProposeManagerTestHelper(BatchAssertions):
    def __init__(self, *args, **kwargs):
        BatchAssertions.__init__(self, *args, **kwargs)
        self.rbac = RBACManager()
        self.test = TestHelper()

    def id(self):
        return uuid4().hex

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def create(self):
        """Create a propose manager proposal for a user that has no manager"""
        self.assertTrue(callable(self.rbac.user.manager.propose.create))
        user, user_key = self.test.user.create()
        manager, manager_key = self.test.user.create()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        proposal, status = self.rbac.user.manager.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=user.user_id,
            target_id=manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, user.user_id)
        self.assertEqual(proposal.target_id, manager.user_id)
        self.assertEqual(proposal.opener, user.user_id)
        self.assertEqual(proposal.open_reason, reason)
        return proposal, user, user_key, manager, manager_key
