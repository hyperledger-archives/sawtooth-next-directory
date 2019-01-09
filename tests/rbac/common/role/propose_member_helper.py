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
"""Propose Member Helper"""
# pylint: disable=no-member,too-few-public-methods

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper
from tests.rbac.common.role.create_role_helper import CreateRoleTestHelper

LOGGER = logging.getLogger(__name__)


class StubTestHelper:
    """A minimal test helper required by this test helper"""

    def __init__(self):
        self.user = CreateUserTestHelper()
        self.role = CreateRoleTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class ProposeRoleMemberTestHelper:
    """Propose Member Helper"""

    def id(self):
        """Get a unique identifier"""
        return rbac.addresser.proposal.unique_id()

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def create(self):
        """A user creates an add role member proposal
        to add themselves as an member to a role"""
        role, role_owner, role_owner_key = helper.role.create()
        user, user_key = helper.user.create()
        proposal_id = self.id()
        reason = self.reason()
        message = rbac.role.member.propose.make(
            proposal_id=proposal_id,
            role_id=role.role_id,
            user_id=user.user_id,
            reason=reason,
            metadata=None,
        )

        status = rbac.role.member.propose.new(
            signer_keypair=user_key, signer_user_id=user.user_id, message=message
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        proposal = rbac.role.member.propose.get(
            object_id=role.role_id, related_id=user.user_id
        )

        assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
        assert (
            proposal.proposal_type
        ), protobuf.proposal_state_pb2.Proposal.ADD_ROLE_MEMBER
        assert proposal.proposal_id == proposal_id
        assert proposal.object_id == role.role_id
        assert proposal.related_id == user.user_id
        assert proposal.opener == user.user_id
        assert proposal.open_reason == reason
        return proposal, role, role_owner, role_owner_key, user, user_key
