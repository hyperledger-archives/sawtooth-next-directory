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
""" Add Key test: test adding a new public key to a user
"""
# pylint: disable=no-member,invalid-name

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.add_key
@pytest.mark.library
def test_make():
    """ Test making a add key message
    """
    user_id = helper.user.id()
    keypair = helper.user.key()
    message = rbac.key.make(user_id=user_id, key_id=keypair.public_key)
    assert isinstance(message, protobuf.key_transaction_pb2.AddKey)
    assert message.user_id == user_id
    assert message.key_id == keypair.public_key


@pytest.mark.add_key
@pytest.mark.library
def test_make_addresses():
    """ Test making add key addresses
    """
    user_id = helper.user.id()
    keypair = helper.user.key()
    message = rbac.key.make(user_id=user_id, key_id=keypair.public_key)
    inputs, outputs = rbac.key.make_addresses(message=message, signer_user_id=user_id)

    user_address = rbac.user.address(object_id=user_id)
    key_address = rbac.key.address(object_id=keypair.public_key)
    user_key_address = rbac.user.key.address(
        object_id=user_id, related_id=keypair.public_key
    )

    assert isinstance(inputs, set)
    assert isinstance(outputs, set)

    assert user_address in inputs
    assert key_address in inputs
    assert user_key_address in inputs

    assert inputs == outputs


@pytest.mark.add_key
def test_add_key():
    """ Test adding a key to blockchain with user assignment
    """
    user = helper.user.imports()
    new_key = helper.user.key()

    status = rbac.key.new(
        signer_keypair=new_key,
        signer_user_id=user.user_id,
        user_id=user.user_id,
        key_id=new_key.public_key,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    assert rbac.user.key.exists(object_id=user.user_id, related_id=new_key.public_key)
