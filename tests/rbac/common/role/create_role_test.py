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
"""Create Role test"""

# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
@pytest.mark.library
@pytest.mark.address
def test_address():
    """Test the address method and that it is in sync with the addresser"""
    role_id = helper.role.id()
    address1 = rbac.role.address(object_id=role_id)
    address2 = rbac.addresser.role.address(role_id)
    assert address1 == address2


@pytest.mark.role
@pytest.mark.library
def test_make():
    """Test making a message"""
    name = helper.role.name()
    description = helper.role.description()
    role_id = helper.role.id()
    user_id = helper.user.id()
    message = rbac.role.make(
        role_id=role_id,
        name=name,
        owners=[user_id],
        admins=[user_id],
        description=description,
    )
    assert isinstance(message, protobuf.role_transaction_pb2.CreateRole)
    assert isinstance(message.role_id, str)
    assert isinstance(message.name, str)
    assert message.role_id == role_id
    assert message.name == name
    assert message.owners == [user_id]
    assert message.admins == [user_id]
    assert message.description == description


@pytest.mark.role
@pytest.mark.library
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
    message = rbac.role.make(
        role_id=role_id, name=name, owners=[user_id], admins=[user_id]
    )

    inputs, outputs = rbac.role.make_addresses(
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
@pytest.mark.create_role
def test_create():
    """Test creating a role"""
    user, keypair = helper.user.create()
    name = helper.role.name()
    description = helper.role.description()
    role_id = helper.role.id()
    message = rbac.role.make(
        role_id=role_id,
        name=name,
        owners=[user.user_id],
        admins=[user.user_id],
        description=description,
    )

    status = rbac.role.new(
        signer_keypair=keypair, signer_user_id=user.user_id, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    role = rbac.role.get(object_id=role_id)

    assert role.role_id == message.role_id
    assert role.name == message.name
    assert role.description == message.description
    assert rbac.role.owner.exists(object_id=role.role_id, related_id=user.user_id)
    assert rbac.role.admin.exists(object_id=role.role_id, related_id=user.user_id)
