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
"""Confirm Role Add Member Test"""

# pylint: disable=no-member,too-many-locals

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
    proposal_id = helper.proposal.id()
    reason = helper.proposal.reason()
    message = rbac.role.member.confirm.make(
        proposal_id=proposal_id, user_id=user_id, role_id=role_id, reason=reason
    )
    assert isinstance(message, protobuf.role_transaction_pb2.ConfirmAddRoleMember)
    assert message.proposal_id == proposal_id
    assert message.user_id == user_id
    assert message.role_id == role_id
    assert message.reason == reason


@pytest.mark.role
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    user_id = helper.user.id()
    role_id = helper.role.id()
    proposal_id = helper.proposal.id()
    proposal_address = rbac.role.member.propose.address(role_id, user_id)
    reason = helper.proposal.reason()
    relationship_address = rbac.role.member.address(role_id, user_id)
    signer_keypair = helper.user.key()

    user_address = rbac.user.address(user_id)
    signer_admin_address = rbac.role.admin.address(role_id, signer_keypair.public_key)
    signer_owner_address = rbac.role.owner.address(role_id, signer_keypair.public_key)
    signer_user_address = rbac.user.address(signer_keypair.public_key)
    message = rbac.role.member.confirm.make(
        proposal_id=proposal_id, user_id=user_id, role_id=role_id, reason=reason
    )

    inputs, outputs = rbac.role.member.confirm.make_addresses(
        message=message, signer_keypair=signer_keypair
    )

    assert user_address in inputs
    assert signer_owner_address in inputs
    assert signer_admin_address in inputs
    assert signer_user_address in inputs
    assert proposal_address in inputs
    assert relationship_address in inputs

    assert proposal_address in outputs
    assert relationship_address in outputs


@pytest.mark.role
@pytest.mark.confirm_role_member
def test_create():
    """Test executing the message on the blockchain"""
    proposal, _, _, role_owner_key, _, _ = helper.role.member.propose.create()

    reason = helper.role.member.propose.reason()

    status = rbac.role.member.confirm.new(
        signer_keypair=role_owner_key,
        proposal_id=proposal.proposal_id,
        role_id=proposal.object_id,
        user_id=proposal.related_id,
        reason=reason,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    confirm = rbac.role.member.confirm.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(confirm, protobuf.proposal_state_pb2.Proposal)
    assert confirm.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_ROLE_MEMBER
    assert confirm.proposal_id == proposal.proposal_id
    assert confirm.object_id == proposal.object_id
    assert confirm.related_id == proposal.related_id
    assert confirm.close_reason == reason
    assert confirm.status == protobuf.proposal_state_pb2.Proposal.CONFIRMED
    assert rbac.role.member.exists(
        object_id=proposal.object_id, related_id=proposal.related_id
    )
