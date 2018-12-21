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
"""Reject Role Add Admin Test"""
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
    related_id = helper.user.id()
    object_id = helper.role.id()
    proposal_id = helper.proposal.id()
    reason = helper.proposal.reason()
    message = rbac.role.admin.reject.make(
        proposal_id=proposal_id,
        related_id=related_id,
        object_id=object_id,
        reason=reason,
    )
    assert isinstance(message, protobuf.proposal_transaction_pb2.UpdateProposal)
    assert message.proposal_id == proposal_id
    assert message.related_id == related_id
    assert message.object_id == object_id
    assert message.reason == reason


@pytest.mark.role
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    related_id = helper.user.id()
    object_id = helper.role.id()
    proposal_id = helper.proposal.id()
    proposal_address = rbac.role.admin.propose.address(object_id, related_id)
    reason = helper.proposal.reason()
    signer_keypair = helper.user.key()
    signer_admin_address = rbac.role.admin.address(object_id, signer_keypair.public_key)
    signer_user_address = rbac.user.address(signer_keypair.public_key)
    message = rbac.role.admin.reject.make(
        proposal_id=proposal_id,
        related_id=related_id,
        object_id=object_id,
        reason=reason,
    )

    inputs, outputs = rbac.role.admin.reject.make_addresses(
        message=message, signer_keypair=signer_keypair
    )

    assert signer_admin_address in inputs
    assert signer_user_address in inputs
    assert proposal_address in inputs

    assert proposal_address in outputs


@pytest.mark.role
@pytest.mark.reject_role_admin
def test_create():
    """Test executing the message on the blockchain"""
    proposal, _, _, role_admin_key, _, _ = helper.role.admin.propose.create()

    reason = helper.role.admin.propose.reason()
    message = rbac.role.admin.reject.make(
        proposal_id=proposal.proposal_id,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
        reason=reason,
    )

    status = rbac.role.admin.reject.new(signer_keypair=role_admin_key, message=message)

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    reject = rbac.role.admin.propose.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(reject, protobuf.proposal_state_pb2.Proposal)
    assert reject.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_ROLE_ADMIN
    assert reject.proposal_id == proposal.proposal_id
    assert reject.object_id == proposal.object_id
    assert reject.related_id == proposal.related_id
    assert reject.close_reason == reason
    assert reject.closer == role_admin_key.public_key
    assert reject.status == protobuf.proposal_state_pb2.Proposal.REJECTED
