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
"""Test the Create Role test helper"""

# pylint: disable=no-member

import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper


LOGGER = get_default_logger(__name__)


@pytest.mark.role
@pytest.mark.library
def test_id():
    """Test get a random role_id"""
    role_id1 = helper.role.id()
    role_id2 = helper.role.id()
    assert isinstance(role_id1, str)
    assert isinstance(role_id2, str)
    assert role_id1 != role_id2


@pytest.mark.role
@pytest.mark.library
def test_name():
    """Test get a random name"""
    name1 = helper.role.name()
    name2 = helper.role.name()
    assert isinstance(name1, str)
    assert isinstance(name2, str)
    assert len(name1) > 4
    assert len(name2) > 4
    assert name1 != name2


@pytest.mark.role
@pytest.mark.library
def test_reason():
    """Test get a random reason"""
    reason1 = helper.role.reason()
    reason2 = helper.role.reason()
    assert isinstance(reason1, str)
    assert isinstance(reason2, str)
    assert len(reason1) > 4
    assert len(reason2) > 4
    assert reason1 != reason2


@pytest.mark.role
@pytest.mark.library
def test_message():
    """Test getting a test create role message"""
    message = helper.role.message()
    assert isinstance(message, protobuf.role_transaction_pb2.CreateRole)
    assert isinstance(message.role_id, str)
    assert isinstance(message.name, str)


@pytest.mark.role
@pytest.mark.integration
def test_create():
    """Test getting a created test role"""
    role, user, keypair = helper.role.create()
    assert isinstance(role, protobuf.role_state_pb2.RoleAttributes)
    assert isinstance(user, protobuf.user_state_pb2.User)
    assert isinstance(role.role_id, str)
    assert isinstance(role.name, str)
    assert isinstance(keypair, Key)
