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
"""Imports User Test"""
# pylint: disable=no-member,invalid-name
import pytest

from rbac.common.user import User
from rbac.common import protobuf
from rbac.common.sawtooth import batcher
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.user
@pytest.mark.library
@pytest.mark.imports_user
def test_make():
    """Test making a create user message"""
    next_id = helper.user.id()
    name = helper.user.name()
    message = User().imports.make(next_id=next_id, name=name)
    assert isinstance(message, protobuf.user_transaction_pb2.ImportsUser)
    assert isinstance(message.next_id, str)
    assert isinstance(message.name, str)
    assert message.next_id == next_id
    assert message.name == name


@pytest.mark.user
@pytest.mark.library
@pytest.mark.imports_user
def test_make_addresses():
    """Test making addresses"""
    next_id = helper.user.id()
    name = helper.user.name()
    message = User().imports.make(next_id=next_id, name=name)
    inputs, outputs = User().imports.make_addresses(
        message=message, signer_user_id=next_id
    )
    user_address = User().address(object_id=message.next_id)
    assert isinstance(inputs, set)
    assert isinstance(outputs, set)

    assert user_address in inputs
    assert user_address in outputs


@pytest.mark.user
@pytest.mark.library
@pytest.mark.imports_user
def test_batch():
    """Test creating a batch"""
    next_id = helper.user.id()
    name = helper.user.name()
    signer_keypair = helper.user.key()

    batch = User().imports.batch(
        signer_user_id=next_id,
        signer_keypair=signer_keypair,
        next_id=next_id,
        name=name,
    )
    messages = batcher.unmake(batch)
    assert isinstance(messages, list)
    assert len(messages) == 1
    assert messages[0].next_id == next_id
    assert messages[0].name == name


@pytest.mark.user
@pytest.mark.imports_user
def test_imports_user():
    """Test importing a user on the blockchain"""
    next_id = helper.user.id()
    name = helper.user.name()
    signer_keypair = helper.user.key()

    status = User().imports.new(
        signer_user_id=next_id,
        signer_keypair=signer_keypair,
        next_id=next_id,
        name=name,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)

    assert user.next_id == next_id
    assert user.name == name


@pytest.mark.user
@pytest.mark.imports_user
def test_create_with_manager():
    """Test creating a user with a manager on the blockchain"""
    signer_keypair = helper.user.key()
    next_id = helper.user.id()
    name = helper.user.name()
    manager_id = helper.user.id()
    manager_name = helper.user.name()

    status = User().imports.new(
        signer_user_id=next_id,
        signer_keypair=signer_keypair,
        next_id=manager_id,
        name=manager_name,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    manager = User().get(object_id=manager_id)

    assert manager.next_id == manager_id
    assert manager.name == manager_name

    status = User().imports.new(
        signer_user_id=next_id,
        signer_keypair=signer_keypair,
        next_id=next_id,
        name=name,
        manager_id=manager_id,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)

    assert user.next_id == next_id
    assert user.name == name
    assert user.manager_id == manager_id


@pytest.mark.user
@pytest.mark.imports_user
def test_create_with_manager_not_in_state():
    """Test creating a user with a manager not in state"""
    signer_keypair = helper.user.key()
    next_id = helper.user.id()
    name = helper.user.name()
    manager_id = helper.user.id()

    status = User().imports.new(
        signer_user_id=next_id,
        signer_keypair=signer_keypair,
        next_id=next_id,
        name=name,
        manager_id=manager_id,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)

    assert user.next_id == next_id
    assert user.name == name
    assert user.manager_id == manager_id


@pytest.mark.user
@pytest.mark.imports_user
def test_reimport_user():
    """Test running import user twice with same data (re-import)"""
    next_id = helper.user.id()
    name = helper.user.name()
    signer_keypair = helper.user.key()

    status = User().imports.new(
        signer_user_id=next_id,
        signer_keypair=signer_keypair,
        next_id=next_id,
        name=name,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)
    assert user.next_id == next_id
    assert user.name == name

    status = User().imports.new(
        signer_user_id=next_id,
        signer_keypair=signer_keypair,
        next_id=next_id,
        name=name,
    )

    user = User().get(object_id=next_id)
    assert user.next_id == next_id
    assert user.name == name
