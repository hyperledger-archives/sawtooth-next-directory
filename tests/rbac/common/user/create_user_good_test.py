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
"""Create User Test"""
# pylint: disable=no-member,invalid-name
import pytest

from rbac.common import addresser
from rbac.common.key import Key
from rbac.common.user import User
from rbac.common import protobuf
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.user
@pytest.mark.library
@pytest.mark.address
def test_address():
    """Test the address method and that it is in sync with the addresser"""
    next_id = helper.user.id()
    address1 = User().address(object_id=next_id)
    address2 = addresser.user.address(next_id)
    assert address1 == address2


@pytest.mark.user
@pytest.mark.library
def test_make():
    """Test making a create user message"""
    next_id = helper.user.id()
    name = helper.user.name()
    username = helper.user.username()
    email = helper.user.email()
    keypair = helper.user.key()
    message = User().make(
        next_id=next_id,
        name=name,
        username=username,
        email=email,
        key=keypair.public_key,
    )
    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.next_id, str)
    assert isinstance(message.name, str)
    assert message.next_id == next_id
    assert message.name == name
    assert message.username == username
    assert message.email == email
    assert message.key == keypair.public_key


@pytest.mark.user
@pytest.mark.skip("TODO: support metadata")
def test_make_with_metadata():
    """test making a create user message with metadata"""
    next_id = helper.user.id()
    name = helper.user.name()
    email = helper.user.email()
    keypair = helper.user.key()
    metadata = {"employeeId": "12345", "mobile": "555-1212"}
    message = User().make(
        next_id=next_id,
        name=name,
        email=email,
        key=keypair.public_key,
        metadata=metadata,
    )
    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.next_id, str)
    assert isinstance(message.name, str)
    assert message.next_id == next_id
    assert message.name == name
    assert message.email == email
    assert message.key == keypair.public_key
    assert message.metadata == metadata


@pytest.mark.user
@pytest.mark.library
def test_make_addresses():
    """Test making addresses without manager"""
    name = helper.user.name()
    email = helper.user.email()
    user_key = helper.user.key()
    next_id = helper.user.id()
    message = User().make(
        next_id=next_id, name=name, email=email, key=user_key.public_key
    )
    inputs, outputs = User().make_addresses(message=message, signer_user_id=next_id)

    user_address = User().address(object_id=message.next_id)
    key_address = Key().address(object_id=user_key.public_key)
    user_key_address = User().key.address(
        object_id=message.next_id, related_id=user_key.public_key
    )

    assert isinstance(inputs, set)
    assert isinstance(outputs, set)

    assert user_address in inputs
    assert key_address in inputs
    assert user_key_address in inputs

    assert user_address in outputs
    assert key_address in outputs
    assert user_key_address in outputs


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_with_manager():
    """Test making addresses with manager"""
    name = helper.user.name()
    email = helper.user.email()
    helper.user.key()
    next_id = helper.user.id()
    user_address = User().address(object_id=next_id)
    manager_id = helper.user.id()
    manager_address = User().address(object_id=manager_id)

    message = User().make(
        next_id=next_id, name=name, email=email, manager_id=manager_id
    )
    inputs, outputs = User().make_addresses(message=message, signer_user_id=next_id)

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
    username = helper.user.username()
    email = helper.user.email()
    user_key = helper.user.key()
    next_id = helper.user.id()

    status = User().new(
        signer_user_id=next_id,
        signer_keypair=user_key,
        next_id=next_id,
        name=name,
        username=username,
        email=email,
        key=user_key.public_key,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)

    assert user.next_id == next_id
    assert user.name == name
    assert user.username == username
    assert user.email == email

    assert User().key.exists(object_id=user.next_id, related_id=user_key.public_key)


@pytest.mark.user
@pytest.mark.create_user_with_manager
def test_create_with_manager():
    """Test creating a user with a manager on the blockchain"""
    user_key = helper.user.key()
    next_id = helper.user.id()
    username = helper.user.username()
    name = helper.user.name()
    email = helper.user.email()
    manager_key = helper.user.key()
    manager_id = manager_key.public_key
    manager_username = helper.user.username()
    manager_name = helper.user.name()
    manager_email = helper.user.email()

    status = User().new(
        signer_user_id=manager_id,
        signer_keypair=manager_key,
        next_id=manager_id,
        name=manager_name,
        username=manager_username,
        email=manager_email,
        key=manager_key.public_key,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    manager = User().get(object_id=manager_id)

    assert manager.next_id == manager_id
    assert manager.username == manager_username
    assert manager.name == manager_name
    assert manager.email == manager_email

    status = User().new(
        signer_user_id=next_id,
        signer_keypair=user_key,
        next_id=next_id,
        name=name,
        username=username,
        email=email,
        manager_id=manager_id,
        key=user_key.public_key,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)

    assert user.next_id == next_id
    assert user.username == username
    assert user.name == name
    assert user.email == email
    assert user.manager_id == manager_id

    assert User().key.exists(object_id=user.next_id, related_id=user_key.public_key)
    # assert User().manager.exists(object_id=user.next_id, related_id=user.manager_id)
    # assert User().direct_report.exists(object_id=user.manager_id, related_id=user.next_id)
    # assert User().email.exists(object_id=user.next_id, related_id=user.email)
