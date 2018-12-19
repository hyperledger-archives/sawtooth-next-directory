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
"""Propose Role Add Task Test"""
# pylint: disable=no-member,too-many-locals

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from rbac.common.crypto import hash_util
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
@pytest.mark.library
def test_make():
    """Test making the message"""
    task_id = helper.task.id()
    role_id = helper.role.id()
    proposal_id = hash_util.generate_12_byte_random_hex()
    reason = helper.proposal.reason()
    message = rbac.role.task.propose.make(
        proposal_id=proposal_id,
        task_id=task_id,
        role_id=role_id,
        reason=reason,
        metadata=None,
    )
    assert isinstance(message, protobuf.role_transaction_pb2.ProposeAddRoleTask)
    assert message.proposal_id == proposal_id
    assert message.task_id == task_id
    assert message.role_id == role_id
    assert message.reason == reason


@pytest.mark.role
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    task_id = helper.task.id()
    task_address = rbac.task.address(task_id)
    role_id = helper.role.id()
    role_address = rbac.role.address(role_id)
    proposal_id = hash_util.generate_12_byte_random_hex()
    reason = helper.proposal.reason()
    relationship_address = rbac.role.task.address(role_id, task_id)
    proposal_address = rbac.role.task.propose.address(role_id, task_id)
    role_owner_keypair = helper.user.key()
    role_owner_address = rbac.role.owner.address(role_id, role_owner_keypair.public_key)
    role_owner_user_address = rbac.user.address(role_owner_keypair.public_key)
    message = rbac.role.task.propose.make(
        proposal_id=proposal_id,
        task_id=task_id,
        role_id=role_id,
        reason=reason,
        metadata=None,
    )

    inputs, outputs = rbac.role.task.propose.make_addresses(
        message=message, signer_keypair=role_owner_keypair
    )

    assert relationship_address in inputs
    assert task_address in inputs
    assert role_address in inputs
    assert proposal_address in inputs
    assert role_owner_address in inputs
    assert role_owner_user_address in inputs

    assert proposal_address in outputs


@pytest.mark.role
@pytest.mark.propose_role_task
def test_create():
    """Test executing the message on the blockchain"""
    role, _, role_owner_key = helper.role.create()
    proposal_id = hash_util.generate_12_byte_random_hex()
    reason = helper.proposal.reason()
    task, _, _ = helper.task.create()

    message = rbac.role.task.propose.make(
        proposal_id=proposal_id,
        task_id=task.task_id,
        role_id=role.role_id,
        reason=reason,
        metadata=None,
    )
    proposal, status = rbac.role.task.propose.create(
        signer_keypair=role_owner_key,
        message=message,
        object_id=role.role_id,
        related_id=task.task_id,
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"
    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert proposal.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_ROLE_TASK
    assert proposal.proposal_id == proposal_id
    assert proposal.object_id == role.role_id
    assert proposal.related_id == task.task_id
    assert proposal.opener == role_owner_key.public_key
    assert proposal.open_reason == reason
