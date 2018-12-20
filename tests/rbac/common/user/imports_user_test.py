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
"""Imports User Test"""
# pylint: disable=no-member,invalid-name

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from rbac.common.sawtooth import batcher
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.library
@pytest.mark.imports_user
def test_make():
    """Test making a create user message"""
    user_id = helper.user.id()
    name = helper.user.name()
    message = rbac.user.imports.make(user_id=user_id, name=name)
    assert isinstance(message, protobuf.user_transaction_pb2.ImportsUser)
    assert isinstance(message.user_id, str)
    assert isinstance(message.name, str)
    assert message.user_id == user_id
    assert message.name == name


@pytest.mark.user
@pytest.mark.library
@pytest.mark.imports_user
def test_make_addresses():
    """Test making addresses"""
    user_id = helper.user.id()
    name = helper.user.name()
    signer_keypair = helper.user.key()
    message = rbac.user.imports.make(user_id=user_id, name=name)
    inputs, outputs = rbac.user.imports.make_addresses(
        message=message, signer_keypair=signer_keypair
    )
    user_address = rbac.user.address(object_id=message.user_id)
    assert isinstance(inputs, set)
    assert isinstance(outputs, set)

    assert user_address in inputs
    assert user_address in outputs


@pytest.mark.user
@pytest.mark.library
@pytest.mark.imports_user
def test_batch():
    """Test creating a batch"""
    user_id = helper.user.id()
    name = helper.user.name()
    signer_keypair = helper.user.key()

    batch = rbac.user.imports.batch(
        signer_keypair=signer_keypair, user_id=user_id, name=name
    )
    messages = batcher.unmake(batch)
    assert isinstance(messages, list)
    assert len(messages) == 1
    assert messages[0].user_id == user_id
    assert messages[0].name == name


@pytest.mark.user
@pytest.mark.imports_user
def test_imports_user():
    """Test importing a user on the blockchain"""
    user_id = helper.user.id()
    name = helper.user.name()
    signer_keypair = helper.user.key()

    _, status = rbac.user.imports.create(
        signer_keypair=signer_keypair, user_id=user_id, name=name
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name


@pytest.mark.user
@pytest.mark.imports_user
def test_create_with_manager():
    """Test creating a user with a manager on the blockchain"""
    signer_keypair = helper.user.key()
    user_id = helper.user.id()
    name = helper.user.name()
    manager_id = helper.user.id()
    manager_name = helper.user.name()

    _, status = rbac.user.imports.create(
        signer_keypair=signer_keypair, user_id=manager_id, name=manager_name
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    manager = rbac.user.get(object_id=manager_id)
    assert manager.user_id == manager_id
    assert manager.name == manager_name

    _, status = rbac.user.imports.create(
        signer_keypair=signer_keypair, user_id=user_id, name=name, manager_id=manager_id
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name
    assert user.manager_id == manager_id


@pytest.mark.user
@pytest.mark.imports_user
def test_create_with_manager_not_in_state():
    """Test creating a user with a manager not in state"""
    signer_keypair = helper.user.key()
    user_id = helper.user.id()
    name = helper.user.name()
    manager_id = helper.user.id()

    _, status = rbac.user.imports.create(
        signer_keypair=signer_keypair, user_id=user_id, name=name, manager_id=manager_id
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name
    assert user.manager_id == manager_id


@pytest.mark.user
@pytest.mark.imports_user
def test_reimport_user():
    """Test running import user twice with same data (reimport)"""
    user_id = helper.user.id()
    name = helper.user.name()
    signer_keypair = helper.user.key()

    _, status = rbac.user.imports.create(
        signer_keypair=signer_keypair, user_id=user_id, name=name
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name

    _, status = rbac.user.imports.create(
        signer_keypair=signer_keypair, user_id=user_id, name=name
    )

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name
