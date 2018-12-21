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
"""Propose Role Add Member Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
@pytest.mark.library
def test_make():
    """Test making the message"""
    user_id = helper.user.id()
    role_id = helper.role.id()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.proposal.reason()
    message = rbac.role.member.propose.make(
        proposal_id=proposal_id,
        user_id=user_id,
        role_id=role_id,
        reason=reason,
        metadata=None,
    )
    assert isinstance(message, protobuf.role_transaction_pb2.ProposeAddRoleMember)
    assert message.proposal_id == proposal_id
    assert message.user_id == user_id
    assert message.role_id == role_id
    assert message.reason == reason


@pytest.mark.role
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    user_id = helper.user.id()
    user_address = rbac.user.address(user_id)
    role_id = helper.role.id()
    role_address = rbac.role.address(role_id)
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.proposal.reason()
    relationship_address = rbac.role.member.address(role_id, user_id)
    proposal_address = rbac.role.member.propose.address(role_id, user_id)
    signer_keypair = helper.user.key()
    message = rbac.role.member.propose.make(
        proposal_id=proposal_id,
        user_id=user_id,
        role_id=role_id,
        reason=reason,
        metadata=None,
    )

    inputs, outputs = rbac.role.member.propose.make_addresses(
        message=message, signer_keypair=signer_keypair
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
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.proposal.reason()
    user, signer_keypair = helper.user.create()

    message = rbac.role.member.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        role_id=role.role_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.role.member.propose.new(
        signer_keypair=signer_keypair, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    proposal = rbac.role.member.propose.get(
        object_id=role.role_id, related_id=user.user_id
    )

    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        proposal.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_ROLE_MEMBER
    )
    assert proposal.proposal_id == proposal_id
    assert proposal.object_id == role.role_id
    assert proposal.related_id == user.user_id
    assert proposal.opener == signer_keypair.public_key
    assert proposal.open_reason == reason
