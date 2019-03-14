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
"""Create Task Test"""
# pylint: disable=no-member

import pytest

from rbac.common import addresser
from rbac.common.user import User
from rbac.common.task import Task
from rbac.common import protobuf
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.task
@pytest.mark.library
@pytest.mark.address
def test_address():
    """Test the address method and that it is in sync with the addresser"""
    task_id = helper.task.id()
    address1 = Task().address(object_id=task_id)
    address2 = addresser.task.address(task_id)
    assert address1 == address2


@pytest.mark.task
@pytest.mark.library
def test_make():
    """Test making a message"""
    name = helper.task.name()
    task_id = helper.task.id()
    next_id = helper.user.id()
    message = Task().make(
        task_id=task_id, name=name, owners=[next_id], admins=[next_id]
    )
    assert isinstance(message, protobuf.task_transaction_pb2.CreateTask)
    assert isinstance(message.task_id, str)
    assert isinstance(message.name, str)
    assert message.task_id == task_id
    assert message.name == name
    assert message.owners == [next_id]
    assert message.admins == [next_id]


@pytest.mark.task
@pytest.mark.library
def test_make_addresses():
    """Test the make addresses method for the message"""
    name = helper.task.name()
    task_id = helper.task.id()
    task_address = Task().address(task_id)

    next_id = helper.user.id()
    user_address = User().address(next_id)
    signer_user_id = helper.user.id()
    owner_address = Task().owner.address(task_id, next_id)
    admin_address = Task().admin.address(task_id, next_id)
    message = Task().make(
        task_id=task_id, name=name, owners=[next_id], admins=[next_id]
    )

    inputs, outputs = Task().make_addresses(
        message=message, signer_user_id=signer_user_id
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
    message = Task().make(
        task_id=task_id, name=name, owners=[user.next_id], admins=[user.next_id]
    )

    status = Task().new(
        signer_keypair=keypair, signer_user_id=user.next_id, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    task = Task().get(object_id=task_id)
    assert task.task_id == message.task_id
    assert task.name == message.name
    assert Task().owner.exists(object_id=task.task_id, related_id=user.next_id)
    assert Task().admin.exists(object_id=task.task_id, related_id=user.next_id)


@pytest.mark.task
@pytest.mark.create_task2
def test_create_two_owners():
    """Test creating a task with two admin+owners"""
    user, keypair = helper.user.create()
    user2, _ = helper.user.create()
    name = helper.task.name()
    task_id = helper.task.id()
    message = Task().make(
        task_id=task_id,
        name=name,
        owners=[user.next_id, user2.next_id],
        admins=[user.next_id, user2.next_id],
    )

    status = Task().new(
        signer_keypair=keypair, signer_user_id=user.next_id, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    task = Task().get(object_id=task_id)

    assert task.task_id == message.task_id
    assert task.name == message.name
    assert Task().owner.exists(object_id=task.task_id, related_id=user.next_id)
    assert Task().admin.exists(object_id=task.task_id, related_id=user.next_id)
    assert Task().owner.exists(object_id=task.task_id, related_id=user2.next_id)
    assert Task().admin.exists(object_id=task.task_id, related_id=user2.next_id)
