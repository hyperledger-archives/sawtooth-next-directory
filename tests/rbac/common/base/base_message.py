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
"""Base Message Test (via Create User)"""
# pylint: disable=no-member,invalid-name

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from rbac.common.sawtooth import batcher
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.library
@pytest.mark.base_message
def test_make_message():
    """Test making a message"""
    name = helper.user.name()
    keypair = helper.user.key()
    message = rbac.user.make(user_id=keypair.public_key, name=name)
    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.user_id, str)
    assert isinstance(message.name, str)
    assert message.user_id == keypair.public_key
    assert message.name == name


@pytest.mark.library
@pytest.mark.base_message
def test_make_payload():
    """Test making a payload with a message"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key
    user_address = rbac.user.address(object_id=user_id)
    message = rbac.user.make(user_id=user_id, name=name)

    payload = rbac.user.make_payload(message=message, signer_keypair=user_key)
    inputs = list(payload.inputs)
    outputs = list(payload.outputs)

    assert payload.message_type == protobuf.rbac_payload_pb2.RBACPayload.CREATE_USER
    assert user_address in inputs
    assert user_address in outputs


@pytest.mark.library
@pytest.mark.base_message
def test_batch_with_message():
    """Test making a batch with a message"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key
    message = rbac.user.make(user_id=user_id, name=name)

    batch = rbac.user.batch(signer_keypair=user_key, message=message)

    messages = batcher.unmake(batch)
    assert len(messages) == 1
    assert messages[0].user_id == user_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_with_kargs():
    """Test making a batch with key arguments"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key

    batch = rbac.user.batch(signer_keypair=user_key, user_id=user_id, name=name)

    messages = batcher.unmake(batch)
    assert len(messages) == 1
    assert messages[0].user_id == user_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_add_with_message():
    """Test making a batch with two messages"""
    name1 = helper.user.name()
    user_key1 = helper.user.key()
    user_id1 = user_key1.public_key
    message1 = rbac.user.make(user_id=user_id1, name=name1)

    name2 = helper.user.name()
    user_key2 = helper.user.key()
    user_id2 = user_key2.public_key
    message2 = rbac.user.make(user_id=user_id2, name=name2)

    batch = rbac.user.batch(signer_keypair=user_key1, message=message1)

    batch = rbac.user.batch(signer_keypair=user_key2, message=message2, batch=batch)

    messages = batcher.unmake(batch)
    assert len(messages) == 2
    assert messages[0].user_id == user_id1
    assert messages[0].name == name1
    assert messages[1].user_id == user_id2
    assert messages[1].name == name2


@pytest.mark.library
@pytest.mark.base_message
def test_batch_add_with_kargs():
    """Test making a batch with two messages using kargs"""
    name1 = helper.user.name()
    user_key1 = helper.user.key()
    user_id1 = user_key1.public_key

    name2 = helper.user.name()
    user_key2 = helper.user.key()
    user_id2 = user_key2.public_key

    batch = rbac.user.batch(signer_keypair=user_key1, user_id=user_id1, name=name1)

    batch = rbac.user.batch(
        signer_keypair=user_key2, user_id=user_id2, name=name2, batch=batch
    )

    messages = batcher.unmake(batch)
    assert len(messages) == 2
    assert messages[0].user_id == user_id1
    assert messages[0].name == name1
    assert messages[1].user_id == user_id2
    assert messages[1].name == name2


@pytest.mark.library
@pytest.mark.base_message
def test_batch_list_with_message():
    """Test making a batch list from a message"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key
    message = rbac.user.make(user_id=user_id, name=name)

    batch_list = rbac.user.batch_list(signer_keypair=user_key, message=message)

    messages = batcher.unmake(batch_list)
    assert len(messages) == 1
    assert messages[0].user_id == user_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_list_with_kargs():
    """Test making a batch list with key arguments"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key

    batch_list = rbac.user.batch_list(
        signer_keypair=user_key, user_id=user_id, name=name
    )

    messages = batcher.unmake(batch_list)
    assert len(messages) == 1
    assert messages[0].user_id == user_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_list_add_with_message():
    """Test making a batch list with two messages"""
    name1 = helper.user.name()
    user_key1 = helper.user.key()
    user_id1 = user_key1.public_key
    message1 = rbac.user.make(user_id=user_id1, name=name1)

    name2 = helper.user.name()
    user_key2 = helper.user.key()
    user_id2 = user_key2.public_key
    message2 = rbac.user.make(user_id=user_id2, name=name2)

    batch_list = rbac.user.batch_list(signer_keypair=user_key1, message=message1)

    batch_list = rbac.user.batch_list(
        signer_keypair=user_key2, message=message2, batch_list=batch_list
    )

    messages = batcher.unmake(batch_list)
    assert len(messages) == 2
    assert messages[0].user_id == user_id1
    assert messages[0].name == name1
    assert messages[1].user_id == user_id2
    assert messages[1].name == name2


@pytest.mark.library
@pytest.mark.base_message
def test_batch_list_add_with_kargs():
    """Test making a batch list with two messages using kargs"""
    name1 = helper.user.name()
    user_key1 = helper.user.key()
    user_id1 = user_key1.public_key

    name2 = helper.user.name()
    user_key2 = helper.user.key()
    user_id2 = user_key2.public_key

    batch_list = rbac.user.batch_list(
        signer_keypair=user_key1, user_id=user_id1, name=name1
    )

    batch_list = rbac.user.batch_list(
        signer_keypair=user_key2, user_id=user_id2, name=name2, batch_list=batch_list
    )

    messages = batcher.unmake(batch_list)
    assert len(messages) == 2
    assert messages[0].user_id == user_id1
    assert messages[0].name == name1
    assert messages[1].user_id == user_id2
    assert messages[1].name == name2


@pytest.mark.base_message
def test_create_with_kargs():
    """Test create passing named arguments"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key

    _, status = rbac.user.create(signer_keypair=user_key, user_id=user_id, name=name)
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name


@pytest.mark.base_message
def test_create_with_message():
    """Test create passing a message"""
    name = helper.user.name()
    user_key = helper.user.key()
    user_id = user_key.public_key
    message = rbac.user.make(user_id=user_id, name=name)

    _, status = rbac.user.create(signer_keypair=user_key, message=message)
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = rbac.user.get(object_id=user_id)
    assert user.user_id == user_id
    assert user.name == name


@pytest.mark.library
@pytest.mark.base_message
def test_make_payload_with_wrong_message_type():
    """Test making a payload with a wrong message type"""
    signer_keypair = helper.user.key()
    message = protobuf.user_state_pb2.User(
        user_id=helper.user.id(), name=helper.user.name(), metadata=None
    )
    with pytest.raises(TypeError):
        rbac.user.make_payload(message=message, signer_keypair=signer_keypair)
