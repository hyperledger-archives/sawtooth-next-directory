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
"""Propose Manager Helper"""
# pylint: disable=no-member,too-few-public-methods

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper

LOGGER = logging.getLogger(__name__)


class StubTestHelper:
    """A minimal test helper required by this test helper"""

    def __init__(self):
        self.user = CreateUserTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class ProposeManagerTestHelper:
    """Propose Manager Helper"""

    def id(self):
        """Get a unique identifier"""
        return rbac.addresser.proposal.unique_id()

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def create(self):
        """Create a propose manager proposal for a user that has no manager"""
        user, user_key = helper.user.create()
        manager, manager_key = helper.user.create()
        proposal_id = self.id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )

        status = rbac.user.manager.propose.new(
            signer_user_id=user.user_id, signer_keypair=user_key, message=message
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        proposal = rbac.user.manager.propose.get(
            object_id=user.user_id, related_id=manager.user_id
        )

        assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
        assert (
            proposal.proposal_type
            == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
        )
        assert proposal.proposal_id == proposal_id
        assert proposal.object_id == user.user_id
        assert proposal.related_id == manager.user_id
        assert proposal.opener == user.user_id
        assert proposal.open_reason == reason
        return proposal, user, user_key, manager, manager_key
