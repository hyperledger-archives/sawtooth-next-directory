# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Propose Role Add Member Test"""
# pylint: disable=no-member
import pytest

from rbac.common import addresser
from rbac.common.user import User
from rbac.common.role import Role
from rbac.common import protobuf
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper


LOGGER = get_default_logger(__name__)


@pytest.mark.role
@pytest.mark.library
def test_make():
    """Test making the message"""
    next_id = helper.user.id()
    role_id = helper.role.id()
    proposal_id = addresser.proposal.unique_id()
    reason = helper.proposal.reason()
    message = Role().member.propose.make(
        proposal_id=proposal_id,
        next_id=next_id,
        role_id=role_id,
        reason=reason,
        metadata=None,
    )
    assert isinstance(message, protobuf.role_transaction_pb2.ProposeAddRoleMember)
    assert message.proposal_id == proposal_id
    assert message.next_id == next_id
    assert message.role_id == role_id
    assert message.reason == reason


@pytest.mark.role
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    next_id = helper.user.id()
    user_address = User().address(next_id)
    role_id = helper.role.id()
    role_address = Role().address(role_id)
    proposal_id = addresser.proposal.unique_id()
    reason = helper.proposal.reason()
    relationship_address = Role().member.address(role_id, next_id)
    proposal_address = Role().member.propose.address(role_id, next_id)
    signer_user_id = helper.user.id()
    message = Role().member.propose.make(
        proposal_id=proposal_id,
        next_id=next_id,
        role_id=role_id,
        reason=reason,
        metadata=None,
    )

    inputs, outputs = Role().member.propose.make_addresses(
        message=message, signer_user_id=signer_user_id
    )

    assert relationship_address in inputs
    assert user_address in inputs
    assert role_address in inputs
    assert proposal_address in inputs

    assert proposal_address in outputs


@pytest.mark.role
@pytest.mark.propose_role_member
def test_create():
    """Test executing the message on the blockchain"""
    role, _, _ = helper.role.create()
    proposal_id = addresser.proposal.unique_id()
    reason = helper.proposal.reason()
    user, signer_keypair = helper.user.create()

    message = Role().member.propose.make(
        proposal_id=proposal_id,
        next_id=user.next_id,
        role_id=role.role_id,
        reason=reason,
        metadata=None,
        signer_user_id=user.next_id,
    )

    status = Role().member.propose.new(
        signer_keypair=signer_keypair, signer_user_id=user.next_id, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    proposal = Role().member.propose.get(
        object_id=role.role_id, related_id=user.next_id
    )

    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        proposal.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_ROLE_MEMBER
    )
    assert proposal.proposal_id == proposal_id
    assert proposal.object_id == role.role_id
    assert proposal.related_id == user.next_id
    assert proposal.opener == user.next_id
    assert proposal.open_reason == reason
