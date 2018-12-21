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
"""Create Task Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.task
@pytest.mark.library
@pytest.mark.address
def test_address():
    """Test the address method and that it is in sync with the addresser"""
    task_id = helper.task.id()
    address1 = rbac.task.address(object_id=task_id)
    address2 = rbac.addresser.task.address(task_id)
    assert address1 == address2


@pytest.mark.task
@pytest.mark.library
def test_make():
    """Test making a message"""
    name = helper.task.name()
    task_id = helper.task.id()
    user_id = helper.user.id()
    message = rbac.task.make(
        task_id=task_id, name=name, owners=[user_id], admins=[user_id]
    )
    assert isinstance(message, protobuf.task_transaction_pb2.CreateTask)
    assert isinstance(message.task_id, str)
    assert isinstance(message.name, str)
    assert message.task_id == task_id
    assert message.name == name
    assert message.owners == [user_id]
    assert message.admins == [user_id]


@pytest.mark.task
@pytest.mark.library
def test_make_addresses():
    """Test the make addresses method for the message"""
    name = helper.task.name()
    task_id = helper.task.id()
    task_address = rbac.task.address(task_id)
    user_id = helper.user.id()
    user_address = rbac.user.address(user_id)
    signer_keypair = helper.user.key()
    owner_address = rbac.task.owner.address(task_id, user_id)
    admin_address = rbac.task.admin.address(task_id, user_id)
    message = rbac.task.make(
        task_id=task_id, name=name, owners=[user_id], admins=[user_id]
    )

    inputs, outputs = rbac.task.make_addresses(
        message=message, signer_keypair=signer_keypair
    )

    assert task_address in inputs
    assert user_address in inputs
    assert owner_address in inputs
    assert admin_address in inputs

    assert task_address in outputs
    assert user_address in outputs
    assert owner_address in outputs
    assert admin_address in outputs


@pytest.mark.task
@pytest.mark.create_task
def test_create():
    """Test creating a task"""
    user, keypair = helper.user.create()
    name = helper.task.name()
    task_id = helper.task.id()
    message = rbac.task.make(
        task_id=task_id, name=name, owners=[user.user_id], admins=[user.user_id]
    )

    status = rbac.task.new(signer_keypair=keypair, message=message)

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    task = rbac.task.get(object_id=task_id)
    assert task.task_id == message.task_id
    assert task.name == message.name
    assert rbac.task.owner.exists(object_id=task.task_id, related_id=user.user_id)
    assert rbac.task.admin.exists(object_id=task.task_id, related_id=user.user_id)


@pytest.mark.task
@pytest.mark.create_task2
def test_create_two_owners():
    """Test creating a task with two admin+owners"""
    user, keypair = helper.user.create()
    user2, _ = helper.user.create()
    name = helper.task.name()
    task_id = helper.task.id()
    message = rbac.task.make(
        task_id=task_id,
        name=name,
        owners=[user.user_id, user2.user_id],
        admins=[user.user_id, user2.user_id],
    )

    status = rbac.task.new(signer_keypair=keypair, message=message)

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    task = rbac.task.get(object_id=task_id)

    assert task.task_id == message.task_id
    assert task.name == message.name
    assert rbac.task.owner.exists(object_id=task.task_id, related_id=user.user_id)
    assert rbac.task.admin.exists(object_id=task.task_id, related_id=user.user_id)
    assert rbac.task.owner.exists(object_id=task.task_id, related_id=user2.user_id)
    assert rbac.task.admin.exists(object_id=task.task_id, related_id=user2.user_id)
