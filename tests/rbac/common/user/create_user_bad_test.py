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
"""Create User Bad Test"""
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
def test_make_with_self_manager():
    """Test creating a user with self as manager"""
    user_key = helper.user.key()
    user_id = user_key.public_key
    name = helper.user.name()

    with pytest.raises(ValueError):
        rbac.user.new(
            signer_user_id=user_id,
            signer_keypair=user_key,
            user_id=user_id,
            name=name,
            metadata=None,
            manager_id=user_id,
        )


@pytest.mark.user
@pytest.mark.integration
def test_with_self_manager():
    """Test creating a user with self as manager"""
    user_key = helper.user.key()
    user_id = user_key.public_key
    name = helper.user.name()

    message = protobuf.user_transaction_pb2.CreateUser(
        user_id=user_id, name=name, metadata=None, manager_id=user_id
    )
    inputs, outputs = rbac.user.make_addresses(message=message, signer_user_id=user_id)
    payload = batcher.make_payload(
        message=message,
        message_type=rbac.user.message_type,
        inputs=inputs,
        outputs=outputs,
        signer_user_id=user_id,
        signer_public_key=user_key.public_key,
    )

    status = rbac.user.send(signer_keypair=user_key, payload=payload)

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.user
@pytest.mark.integration
def test_with_manager_not_in_state():
    """Test creating a user with manager not in state"""
    user_key = helper.user.key()
    user_id = user_key.public_key
    manager_key = helper.user.key()
    manager_id = manager_key.public_key
    name = helper.user.name()

    message = protobuf.user_transaction_pb2.CreateUser(
        user_id=user_id, name=name, metadata=None, manager_id=manager_id
    )
    inputs, outputs = rbac.user.make_addresses(message=message, signer_user_id=user_id)
    payload = batcher.make_payload(
        message=message,
        message_type=rbac.user.message_type,
        inputs=inputs,
        outputs=outputs,
        signer_user_id=user_id,
        signer_public_key=user_key.public_key,
    )

    status = rbac.user.send(signer_keypair=user_key, payload=payload)

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.skip("skip pending change in signer verification")
@pytest.mark.user
@pytest.mark.library
def test_make_payload_with_other_signer():
    """Test with signer is neither user nor manager"""
    user_key = helper.user.key()
    user_id = user_key.public_key
    manager_key = helper.user.key()
    manager_id = manager_key.public_key
    other_id = helper.user.id()
    other_key = helper.user.key()
    name = helper.user.name()

    message = protobuf.user_transaction_pb2.CreateUser(
        user_id=user_id, name=name, metadata=None, manager_id=manager_id
    )

    rbac.user.make_payload(
        message=message, signer_user_id=user_id, signer_keypair=user_key
    )
    rbac.user.make_payload(
        message=message, signer_user_id=manager_id, signer_keypair=manager_key
    )


@pytest.mark.user
@pytest.mark.integration
def test_with_other_signer():
    """Test with signer is neither user nor manager"""
    user_key = helper.user.key()
    user_id = user_key.public_key
    manager_key = helper.user.key()
    manager_id = manager_key.public_key
    other_id = helper.user.id()
    other_key = helper.user.key()
    name = helper.user.name()

    message = protobuf.user_transaction_pb2.CreateUser(
        user_id=user_id, name=name, metadata=None, manager_id=manager_id
    )
    inputs, outputs = rbac.user.make_addresses(message=message, signer_user_id=other_id)
    payload = batcher.make_payload(
        message=message,
        message_type=rbac.user.message_type,
        inputs=inputs,
        outputs=outputs,
        signer_user_id=other_id,
        signer_public_key=other_key.public_key,
    )

    status = rbac.user.send(signer_keypair=other_key, payload=payload)

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"
