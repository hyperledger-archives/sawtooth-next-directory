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
""" Remove Role Member Test
"""
# pylint: disable=no-member
import pytest

from rbac.common import addresser
from rbac.common.role import Role
from rbac.common import protobuf
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.remove_role_member
@pytest.mark.role
@pytest.mark.library
def test_make():
    """ Test making the message
    """
    next_id = helper.user.id()
    role_id = helper.role.id()
    reason = helper.proposal.reason()
    proposal_id = addresser.proposal.unique_id()
    message = Role().member.remove.make(
        proposal_id=proposal_id, object_id=role_id, related_id=next_id, reason=reason
    )
    assert isinstance(message, protobuf.proposal_transaction_pb2.RemovalProposal)
    assert message.proposal_id == proposal_id
    assert message.object_id == role_id
    assert message.related_id == next_id
    assert message.reason == reason


@pytest.mark.remove_role_member
@pytest.mark.role
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    next_id = helper.user.id()
    role_id = helper.role.id()
    proposal_id = addresser.proposal.unique_id()
    reason = helper.proposal.reason()
    signer_user_id = helper.user.id()
    relationship_address = Role().member.address(role_id, next_id)
    proposal_address = Role().member.remove.address(role_id, next_id)
    role_owner_address = Role().owner.address(role_id, signer_user_id)

    message = Role().member.remove.make(
        proposal_id=proposal_id, object_id=role_id, related_id=next_id, reason=reason
    )

    inputs, outputs = Role().member.remove.make_addresses(
        message=message, signer_user_id=signer_user_id
    )

    assert relationship_address in inputs
    assert proposal_address in inputs
    assert role_owner_address in inputs

    assert proposal_address in outputs
    assert relationship_address in outputs


@pytest.mark.remove_role_member
@pytest.mark.role
def test_new():
    """Test executing the message on the blockchain"""
    proposal, _, role_owner, role_owner_key, _, _ = helper.role.member.propose.create()

    reason = helper.role.member.propose.reason()

    status = Role().member.confirm.new(
        signer_keypair=role_owner_key,
        signer_user_id=role_owner.next_id,
        proposal_id=proposal.proposal_id,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
        reason=reason,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    assert Role().member.exists(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    proposal_id = helper.proposal.id()
    reason = helper.proposal.reason()

    Role().member.confirm.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    status2 = Role().member.remove.new(
        signer_keypair=role_owner_key,
        signer_user_id=role_owner.next_id,
        proposal_id=proposal_id,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
        reason=reason,
    )

    assert len(status2) == 1
    assert status2[0]["status"] == "COMMITTED"

    removal = Role().member.remove.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(removal, protobuf.proposal_state_pb2.Proposal)
    assert (
        removal.proposal_type == protobuf.proposal_state_pb2.Proposal.REMOVE_ROLE_MEMBER
    )
    assert removal.proposal_id == proposal_id
    assert removal.object_id == proposal.object_id
    assert removal.related_id == proposal.related_id
    assert removal.open_reason == reason
    assert removal.close_reason == ""
    assert removal.opener == role_owner.next_id
    assert removal.closer == role_owner.next_id
    assert removal.status == protobuf.proposal_state_pb2.Proposal.REMOVED

    assert Role().member.not_exists(
        object_id=proposal.object_id, related_id=proposal.related_id
    )
