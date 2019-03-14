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
"""Base Message Test (via Create User)"""
# pylint: disable=no-member,invalid-name

import pytest

from rbac.common.user import User
from rbac.common import protobuf
from rbac.common.sawtooth.batcher import unmake
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.library
@pytest.mark.base_message
def test_make_message():
    """Test making a message"""
    name = helper.user.name()
    keypair = helper.user.key()
    message = User().make(next_id=keypair.public_key, name=name)
    assert isinstance(message, protobuf.user_transaction_pb2.CreateUser)
    assert isinstance(message.next_id, str)
    assert isinstance(message.name, str)
    assert message.next_id == keypair.public_key
    assert message.name == name


@pytest.mark.library
@pytest.mark.base_message
def test_make_payload():
    """Test making a payload with a message"""
    name = helper.user.name()
    user_key = helper.user.key()
    next_id = user_key.public_key
    user_address = User().address(object_id=next_id)
    message = User().make(next_id=next_id, name=name)

    payload = User().make_payload(
        message=message, signer_user_id=next_id, signer_keypair=user_key
    )
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
    next_id = user_key.public_key
    message = User().make(next_id=next_id, name=name)

    batch = User().batch(
        signer_user_id=next_id, signer_keypair=user_key, message=message
    )

    messages = unmake(batch)
    assert len(messages) == 1
    assert messages[0].next_id == next_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_with_kargs():
    """Test making a batch with key arguments"""
    name = helper.user.name()
    user_key = helper.user.key()
    next_id = user_key.public_key

    batch = User().batch(
        signer_user_id=next_id, signer_keypair=user_key, next_id=next_id, name=name
    )

    messages = unmake(batch)
    assert len(messages) == 1
    assert messages[0].next_id == next_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_add_with_message():
    """Test making a batch with two messages"""
    name1 = helper.user.name()
    user_key1 = helper.user.key()
    user_id1 = user_key1.public_key
    message1 = User().make(next_id=user_id1, name=name1)

    name2 = helper.user.name()
    user_key2 = helper.user.key()
    user_id2 = user_key2.public_key
    message2 = User().make(next_id=user_id2, name=name2)

    batch = User().batch(
        signer_user_id=user_id1, signer_keypair=user_key1, message=message1
    )

    batch = User().batch(
        signer_user_id=user_id2, signer_keypair=user_key2, message=message2, batch=batch
    )

    messages = unmake(batch)
    assert len(messages) == 2
    assert messages[0].next_id == user_id1
    assert messages[0].name == name1
    assert messages[1].next_id == user_id2
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

    batch = User().batch(
        signer_user_id=user_id1, signer_keypair=user_key1, next_id=user_id1, name=name1
    )

    batch = User().batch(
        signer_user_id=user_id2,
        signer_keypair=user_key2,
        next_id=user_id2,
        name=name2,
        batch=batch,
    )

    messages = unmake(batch)
    assert len(messages) == 2
    assert messages[0].next_id == user_id1
    assert messages[0].name == name1
    assert messages[1].next_id == user_id2
    assert messages[1].name == name2


@pytest.mark.library
@pytest.mark.base_message
def test_batch_list_with_message():
    """Test making a batch list from a message"""
    name = helper.user.name()
    user_key = helper.user.key()
    next_id = user_key.public_key
    message = User().make(next_id=next_id, name=name)

    batch_list = User().batch_list(
        signer_user_id=next_id, signer_keypair=user_key, message=message
    )

    messages = unmake(batch_list)
    assert len(messages) == 1
    assert messages[0].next_id == next_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_list_with_kargs():
    """Test making a batch list with key arguments"""
    name = helper.user.name()
    user_key = helper.user.key()
    next_id = user_key.public_key

    batch_list = User().batch_list(
        signer_user_id=next_id, signer_keypair=user_key, next_id=next_id, name=name
    )

    messages = unmake(batch_list)
    assert len(messages) == 1
    assert messages[0].next_id == next_id
    assert messages[0].name == name


@pytest.mark.library
@pytest.mark.base_message
def test_batch_list_add_with_message():
    """Test making a batch list with two messages"""
    name1 = helper.user.name()
    user_key1 = helper.user.key()
    user_id1 = user_key1.public_key
    message1 = User().make(next_id=user_id1, name=name1)

    name2 = helper.user.name()
    user_key2 = helper.user.key()
    user_id2 = user_key2.public_key
    message2 = User().make(next_id=user_id2, name=name2)

    batch_list = User().batch_list(
        signer_user_id=user_id2, signer_keypair=user_key1, message=message1
    )

    batch_list = User().batch_list(
        signer_user_id=user_id2,
        signer_keypair=user_key2,
        message=message2,
        batch_list=batch_list,
    )

    messages = unmake(batch_list)
    assert len(messages) == 2
    assert messages[0].next_id == user_id1
    assert messages[0].name == name1
    assert messages[1].next_id == user_id2
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

    batch_list = User().batch_list(
        signer_user_id=user_id1, signer_keypair=user_key1, next_id=user_id1, name=name1
    )

    batch_list = User().batch_list(
        signer_user_id=user_id2,
        signer_keypair=user_key2,
        next_id=user_id2,
        name=name2,
        batch_list=batch_list,
    )

    messages = unmake(batch_list)
    assert len(messages) == 2
    assert messages[0].next_id == user_id1
    assert messages[0].name == name1
    assert messages[1].next_id == user_id2
    assert messages[1].name == name2


@pytest.mark.base_message
def test_create_with_kargs():
    """Test create passing named arguments"""
    name = helper.user.name()
    user_key = helper.user.key()
    next_id = user_key.public_key

    status = User().new(
        signer_user_id=next_id, signer_keypair=user_key, next_id=next_id, name=name
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)
    assert user.next_id == next_id
    assert user.name == name


@pytest.mark.base_message
def test_create_with_message():
    """Test create passing a message"""
    name = helper.user.name()
    user_key = helper.user.key()
    next_id = user_key.public_key
    message = User().make(next_id=next_id, name=name)

    status = User().new(
        signer_user_id=next_id, signer_keypair=user_key, message=message
    )
    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    user = User().get(object_id=next_id)
    assert user.next_id == next_id
    assert user.name == name


@pytest.mark.library
@pytest.mark.base_message
def test_make_payload_with_wrong_message_type():
    """Test making a payload with a wrong message type"""
    signer_keypair = helper.user.key()
    next_id = helper.user.id()
    message = protobuf.user_state_pb2.User(
        next_id=next_id, name=helper.user.name(), metadata=None
    )
    with pytest.raises(TypeError):
        User().make_payload(
            message=message, signer_user_id=next_id, signer_keypair=signer_keypair
        )
