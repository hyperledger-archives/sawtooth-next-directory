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
"""Imports Role test"""

# pylint: disable=no-member

import pytest

from rbac.common.role import Role
from rbac.common.user import User
from rbac.common import protobuf
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.library
@pytest.mark.role
@pytest.mark.imports_role
def test_make():
    """Test making a message"""
    name = helper.role.name()
    role_id = helper.role.id()
    next_id = helper.user.id()
    message = Role().imports.make(
        role_id=role_id, name=name, owners=[next_id], admins=[next_id]
    )
    assert isinstance(message, protobuf.role_transaction_pb2.ImportsRole)
    assert isinstance(message.role_id, str)
    assert isinstance(message.name, str)
    assert message.role_id == role_id
    assert message.name == name
    assert message.owners == [next_id]
    assert message.admins == [next_id]


@pytest.mark.library
@pytest.mark.role
@pytest.mark.imports_role
def test_make_addresses():
    """Test the make addresses method for the message"""
    name = helper.role.name()
    role_id = helper.role.id()
    role_address = Role().address(role_id)
    next_id = helper.user.id()
    user_address = User().address(next_id)
    signer_user_id = helper.user.id()
    owner_address = Role().owner.address(role_id, next_id)
    admin_address = Role().admin.address(role_id, next_id)
    message = Role().imports.make(
        role_id=role_id, name=name, owners=[next_id], admins=[next_id]
    )

    inputs, outputs = Role().imports.make_addresses(
        message=message, signer_user_id=signer_user_id
    )

    assert role_address in inputs
    assert user_address in inputs
    assert owner_address in inputs
    assert admin_address in inputs

    assert role_address in outputs
    assert user_address in outputs
    assert owner_address in outputs
    assert admin_address in outputs


@pytest.mark.role
@pytest.mark.imports_role
def test_create():
    """Test importing a role"""
    user, keypair = helper.user.create()
    name = helper.role.name()
    role_id = helper.role.id()

    status = Role().imports.new(
        signer_keypair=keypair,
        signer_user_id=user.next_id,
        role_id=role_id,
        name=name,
        owners=[user.next_id],
        admins=[user.next_id],
        members=[user.next_id],
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    role = Role().get(object_id=role_id)

    assert role.role_id == role_id
    assert role.name == name
    assert Role().owner.exists(object_id=role.role_id, related_id=user.next_id)
    assert Role().admin.exists(object_id=role.role_id, related_id=user.next_id)
    assert Role().member.exists(object_id=role.role_id, related_id=user.next_id)
