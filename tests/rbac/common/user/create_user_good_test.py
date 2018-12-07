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
"""Create User Test"""
# pylint: disable=no-member,invalid-name

import logging
import pytest

from rbac.common import rbac
from rbac.common.crypto.keys import Key
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.library
@pytest.mark.address
def test_address():
    """Test the address method and that it is in sync with the addresser"""
    user_id = helper.user.id()
    address1 = rbac.user.address(object_id=user_id)
    address2 = rbac.addresser.user.address(user_id)
    assert address1 == address2


@pytest.mark.user
@pytest.mark.library
def test_make():
    """Test making a create user message"""
    name = helper.user.name()
    keypair = helper.user.key()
    message = rbac.user.make(user_id=keypair.public_key, name=name)
    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.user_id, str)
    assert isinstance(message.name, str)
    assert message.user_id == keypair.public_key
    assert message.name == name


@pytest.mark.user
@pytest.mark.skip("TODO: support metadata")
def test_make_with_metadata():
    """test making a create user message with metadata"""
    name = helper.user.name()
    keypair = helper.user.key()
    metadata = {"employeeId": "12345", "mobile": "555-1212"}
    message = rbac.user.make(user_id=keypair.public_key, name=name, metadata=metadata)
    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.user_id, str)
    assert isinstance(message.name, str)
    assert message.user_id == keypair.public_key
    assert message.name == name
    assert message.metadata == metadata


@pytest.mark.user
@pytest.mark.library
def test_make_with_key():
    """Test making a create user message with key generation"""
    name = helper.user.name()
    message, keypair = rbac.user.make_with_key(name=name)
    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.user_id, str)
    assert isinstance(message.name, str)
    assert isinstance(keypair, Key)
    assert message.user_id == keypair.public_key
    assert message.name == name


@pytest.mark.user
@pytest.mark.library
def test_make_addresses():
    """Test making addresses without manager"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key
    message = rbac.user.make(user_id=user_id, name=name)
    inputs, outputs = rbac.user.make_addresses(message=message, signer_keypair=user_key)
    user_address = rbac.user.address(object_id=message.user_id)

    assert isinstance(inputs, set)
    assert isinstance(outputs, set)

    assert user_address in inputs
    assert user_address in outputs


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_with_manager():
    """Test making addresses with manager"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key
    user_address = rbac.user.address(object_id=user_id)
    manager_id = helper.user.id()
    manager_address = rbac.user.address(object_id=manager_id)

    message = rbac.user.make(user_id=user_id, name=name, manager_id=manager_id)
    inputs, outputs = rbac.user.make_addresses(message=message, signer_keypair=user_key)

    assert isinstance(inputs, set)
    assert isinstance(outputs, set)

    assert user_address in inputs
    assert user_address in outputs
    assert manager_address in inputs
    assert manager_address in outputs


@pytest.mark.user
@pytest.mark.create_user
def test_create_user():
    """Test creating a user on the blockchain"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key

    _, status = rbac.user.create(signer_keypair=user_key, user_id=user_id, name=name)
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name


@pytest.mark.user
@pytest.mark.integration
def test_create_with_manager():
    """Test creating a user with a manager on the blockchain"""
    user_key = helper.user.key()
    user_id = user_key.public_key
    name = helper.user.name()
    manager_key = helper.user.key()
    manager_id = manager_key.public_key
    manager_name = helper.user.name()

    _, status = rbac.user.create(
        signer_keypair=manager_key, user_id=manager_id, name=manager_name
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    manager = rbac.user.get(object_id=manager_id)
    assert manager.user_id == manager_id
    assert manager.name == manager_name

    _, status = rbac.user.create(
        signer_keypair=user_key, user_id=user_id, name=name, manager_id=manager_id
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name
    assert user.manager_id == manager_id
