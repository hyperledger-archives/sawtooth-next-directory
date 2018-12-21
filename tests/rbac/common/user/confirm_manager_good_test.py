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
"""Confirm Manager Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.library
def test_make():
    """Test making the message"""
    object_id = helper.user.id()
    related_id = helper.user.id()
    reason = helper.user.manager.propose.reason()
    proposal_id = helper.user.manager.propose.id()
    message = rbac.user.manager.confirm.make(
        proposal_id=proposal_id,
        object_id=object_id,
        related_id=related_id,
        reason=reason,
    )
    assert isinstance(message, protobuf.proposal_transaction_pb2.UpdateProposal)
    assert message.proposal_id == proposal_id
    assert message.object_id == object_id
    assert message.related_id == related_id
    assert message.reason == reason


@pytest.mark.user
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    object_id = helper.user.id()
    user_address = rbac.user.address(object_id=object_id)
    signer_keypair = helper.user.key()

    related_id = helper.user.id()
    reason = helper.user.manager.propose.reason()
    proposal_id = helper.proposal.id()
    proposal_address = rbac.user.manager.confirm.address(
        object_id=object_id, related_id=related_id
    )
    signer_user_address = rbac.user.address(signer_keypair.public_key)
    message = rbac.user.manager.confirm.make(
        proposal_id=proposal_id,
        object_id=object_id,
        related_id=related_id,
        reason=reason,
    )

    inputs, outputs = rbac.user.manager.confirm.make_addresses(
        message=message, signer_keypair=signer_keypair
    )

    assert user_address in inputs
    assert proposal_address in inputs
    assert signer_user_address in inputs

    assert user_address in outputs
    assert proposal_address in outputs


@pytest.mark.user
@pytest.mark.confirm_user_manager
def test_create():
    """Test confirming a manager proposal"""
    proposal, _, _, _, manager_key = helper.user.manager.propose.create()
    reason = helper.user.manager.propose.reason()

    status = rbac.user.manager.confirm.new(
        signer_keypair=manager_key,
        proposal_id=proposal.proposal_id,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
        reason=reason,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    confirm = rbac.user.manager.confirm.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(confirm, protobuf.proposal_state_pb2.Proposal)
    assert (
        confirm.proposal_type
        == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert confirm.proposal_id == proposal.proposal_id
    assert confirm.object_id == proposal.object_id
    assert confirm.related_id == proposal.related_id
    assert confirm.close_reason == reason
    assert confirm.status == protobuf.proposal_state_pb2.Proposal.CONFIRMED

    user = rbac.user.get(object_id=proposal.object_id)
    assert isinstance(user, protobuf.user_state_pb2.User)
    assert user.manager_id == proposal.related_id
