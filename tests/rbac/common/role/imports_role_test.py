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
"""Imports Role test"""

# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.library
@pytest.mark.role
@pytest.mark.imports_role
def test_make():
    """Test making a message"""
    name = helper.role.name()
    role_id = helper.role.id()
    user_id = helper.user.id()
    message = rbac.role.imports.make(
        role_id=role_id, name=name, owners=[user_id], admins=[user_id]
    )
    assert isinstance(message, protobuf.role_transaction_pb2.ImportsRole)
    assert isinstance(message.role_id, str)
    assert isinstance(message.name, str)
    assert message.role_id == role_id
    assert message.name == name
    assert message.owners == [user_id]
    assert message.admins == [user_id]


@pytest.mark.library
@pytest.mark.role
@pytest.mark.imports_role
def test_make_addresses():
    """Test the make addresses method for the message"""
    name = helper.role.name()
    role_id = helper.role.id()
    role_address = rbac.role.address(role_id)
    user_id = helper.user.id()
    user_address = rbac.user.address(user_id)
    signer_user_id = helper.user.id()
    signer_keypair = helper.user.key()
    owner_address = rbac.role.owner.address(role_id, user_id)
    admin_address = rbac.role.admin.address(role_id, user_id)
    message = rbac.role.imports.make(
        role_id=role_id, name=name, owners=[user_id], admins=[user_id]
    )

    inputs, outputs = rbac.role.imports.make_addresses(
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

    status = rbac.role.imports.new(
        signer_keypair=keypair,
        signer_user_id=user.user_id,
        role_id=role_id,
        name=name,
        owners=[user.user_id],
        admins=[user.user_id],
        members=[user.user_id],
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    role = rbac.role.get(object_id=role_id)

    assert role.role_id == role_id
    assert role.name == name
    assert rbac.role.owner.exists(object_id=role.role_id, related_id=user.user_id)
    assert rbac.role.admin.exists(object_id=role.role_id, related_id=user.user_id)
    assert rbac.role.member.exists(object_id=role.role_id, related_id=user.user_id)
