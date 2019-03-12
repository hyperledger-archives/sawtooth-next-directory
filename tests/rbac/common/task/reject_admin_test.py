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
"""Reject Task Add Admin Test"""
# pylint: disable=no-member
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.task
@pytest.mark.library
def test_make():
    """Test making the message"""
    related_id = helper.user.id()
    object_id = helper.task.id()
    proposal_id = helper.proposal.id()
    reason = helper.proposal.reason()
    message = rbac.task.admin.reject.make(
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


@pytest.mark.task
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    related_id = helper.user.id()
    object_id = helper.task.id()
    proposal_id = helper.proposal.id()
    proposal_address = rbac.task.admin.propose.address(object_id, related_id)
    reason = helper.proposal.reason()
    signer_user_id = helper.user.id()
    signer_admin_address = rbac.task.admin.address(object_id, signer_user_id)

    message = rbac.task.admin.reject.make(
        proposal_id=proposal_id,
        related_id=related_id,
        object_id=object_id,
        reason=reason,
    )

    inputs, outputs = rbac.task.admin.reject.make_addresses(
        message=message, signer_user_id=signer_user_id
    )

    assert proposal_address in inputs
    assert signer_admin_address in inputs

    assert proposal_address in outputs


@pytest.mark.task
@pytest.mark.reject_task_admin
def test_create():
    """Test executing the message on the blockchain"""
    proposal, _, task_admin, task_admin_key, _, _ = helper.task.admin.propose.create()

    reason = helper.task.admin.propose.reason()
    message = rbac.task.admin.reject.make(
        proposal_id=proposal.proposal_id,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
        reason=reason,
    )

    status = rbac.task.admin.reject.new(
        signer_keypair=task_admin_key,
        signer_user_id=task_admin.user_id,
        message=message,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    reject = rbac.task.admin.propose.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(reject, protobuf.proposal_state_pb2.Proposal)
    assert reject.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_TASK_ADMIN
    assert reject.proposal_id == proposal.proposal_id
    assert reject.object_id == proposal.object_id
    assert reject.related_id == proposal.related_id
    assert reject.close_reason == reason
    assert reject.closer == task_admin.user_id
    assert reject.status == protobuf.proposal_state_pb2.Proposal.REJECTED
