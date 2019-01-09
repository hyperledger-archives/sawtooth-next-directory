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
"""Test Create User Test Helper"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.crypto.keys import PUBLIC_KEY_PATTERN
from rbac.common.crypto.keys import PRIVATE_KEY_PATTERN
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.library
def test_id():
    """Test get a random user_id"""
    user_id1 = helper.user.id()
    user_id2 = helper.user.id()
    assert isinstance(user_id1, str)
    assert isinstance(user_id2, str)
    assert user_id1 != user_id2


@pytest.mark.user
@pytest.mark.library
def test_key():
    """Test get a generated keypair"""
    key1 = helper.user.key()
    key2 = helper.user.key()
    assert isinstance(key1, Key)
    assert isinstance(key2, Key)
    assert PUBLIC_KEY_PATTERN.match(key1.public_key)
    assert PUBLIC_KEY_PATTERN.match(key2.public_key)
    assert PRIVATE_KEY_PATTERN.match(key1.private_key)
    assert PRIVATE_KEY_PATTERN.match(key2.private_key)
    assert key1.public_key != key2.public_key
    assert key1.private_key != key2.private_key


@pytest.mark.user
@pytest.mark.library
def test_name():
    """Test get a random name"""
    name1 = helper.user.name()
    name2 = helper.user.name()
    assert isinstance(name1, str)
    assert isinstance(name2, str)
    assert len(name1) > 4
    assert len(name2) > 4
    assert name1 != name2


@pytest.mark.user
@pytest.mark.library
def test_username():
    """Test get a random username"""
    username1 = helper.user.username()
    username2 = helper.user.username()
    assert isinstance(username1, str)
    assert isinstance(username2, str)
    assert len(username1) > 4
    assert len(username2) > 4
    assert username1 != username2


@pytest.mark.user
@pytest.mark.library
def test_reason():
    """Test get a random reason"""
    reason1 = helper.user.reason()
    reason2 = helper.user.reason()
    assert isinstance(reason1, str)
    assert isinstance(reason2, str)
    assert len(reason1) > 4
    assert len(reason2) > 4
    assert reason1 != reason2


@pytest.mark.user
@pytest.mark.library
def test_message():
    """Test getting a test create user message with key"""
    message, keypair = helper.user.message()

    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.user_id, str)
    assert isinstance(message.name, str)
    assert isinstance(keypair, Key)


@pytest.mark.user
@pytest.mark.library
def test_message_with_manager():
    """Test getting a test create user and manager message"""
    user, user_key, manager, manager_key = helper.user.message_with_manager()

    assert isinstance(user, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(manager, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(user.user_id, str)
    assert isinstance(manager.user_id, str)
    assert isinstance(user.name, str)
    assert isinstance(manager.name, str)
    assert isinstance(user_key, Key)
    assert isinstance(manager_key, Key)
    assert user.manager_id == manager.user_id
    assert user.user_id != manager.user_id


@pytest.mark.user
@pytest.mark.integration
def test_create():
    """Test getting a created test user"""
    user, keypair = helper.user.create()

    assert isinstance(user, protobuf.user_state_pb2.User)
    assert isinstance(user.user_id, str)
    assert isinstance(user.name, str)
    assert isinstance(keypair, Key)


@pytest.mark.user
def test_imports():
    """Test getting a created test user"""
    user = helper.user.imports()

    assert isinstance(user, protobuf.user_state_pb2.User)
    assert isinstance(user.user_id, str)
    assert isinstance(user.name, str)


@pytest.mark.user
@pytest.mark.integration
def test_create_with_manager():
    """Test getting a created test user with manager"""
    user, user_key, manager, manager_key = helper.user.create_with_manager()

    assert isinstance(user, protobuf.user_state_pb2.User)
    assert isinstance(manager, protobuf.user_state_pb2.User)
    assert isinstance(user.user_id, str)
    assert isinstance(manager.user_id, str)
    assert isinstance(user.name, str)
    assert isinstance(manager.name, str)
    assert isinstance(user_key, Key)
    assert isinstance(manager_key, Key)
    assert user.manager_id == manager.user_id
    assert user.user_id != manager.user_id


@pytest.mark.user
@pytest.mark.integration
def test_create_with_grand_manager():
    """Test getting a created test user with manager and their manager"""
    user, user_key, manager, manager_key, grandmgr, grandmgr_key = (
        helper.user.create_with_grand_manager()
    )

    assert isinstance(user, protobuf.user_state_pb2.User)
    assert isinstance(manager, protobuf.user_state_pb2.User)
    assert isinstance(grandmgr, protobuf.user_state_pb2.User)
    assert isinstance(user.user_id, str)
    assert isinstance(manager.user_id, str)
    assert isinstance(grandmgr.user_id, str)
    assert isinstance(user.name, str)
    assert isinstance(manager.name, str)
    assert isinstance(grandmgr.name, str)
    assert isinstance(user_key, Key)
    assert isinstance(manager_key, Key)
    assert isinstance(grandmgr_key, Key)
    assert user.manager_id == manager.user_id
    assert manager.manager_id == grandmgr.user_id
    assert user.user_id != manager.user_id
    assert manager.user_id != grandmgr.user_id
