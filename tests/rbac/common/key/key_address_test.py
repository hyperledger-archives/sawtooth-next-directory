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
"""Test addressing a key and its relationships"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac import helper
from tests.rbac.test.assertions import assert_is_address
from tests.rbac.test.assertions import assert_is_identifier

LOGGER = logging.getLogger(__name__)


@pytest.mark.library
@pytest.mark.addressing
@pytest.mark.key_address
def test_addressing_key():
    """Tests making a blockchain address for a public key and that it:
    1. is a 35-byte non-zero hexadecimal string
    2. is unique - a different public key yields a different address
    3. is deterministic - same public key yields same address
    4. the addresser recognizes the address as a public key
    5. the addresser can parse the address into its components
    6. the identifier is a hash of the public key"""
    key = helper.user.key().public_key
    address = addresser.key.address(key)

    assert assert_is_address(address)
    assert address != addresser.key.address(helper.user.key().public_key)
    assert address == addresser.key.address(key)
    assert address == addresser.key.address(key.upper())

    assert addresser.get_address_type(address) == addresser.AddressSpace.KEY
    assert addresser.get_address_type(address) == addresser.AddressSpace.KEY

    parsed = addresser.parse(address)

    assert parsed.object_type == addresser.ObjectType.KEY
    assert parsed.related_type == addresser.ObjectType.NONE
    assert parsed.relationship_type == addresser.RelationshipType.NONE
    assert assert_is_identifier(parsed.object_id)
    assert not parsed.related_id

    assert parsed.object_id == addresser.key.hash(key)


@pytest.mark.library
@pytest.mark.addressing
@pytest.mark.key_address
def test_addressing_user_key():
    """Tests making a blockchain address that is a user-key assignment:
    1. is a 35-byte non-zero hexadecimal string
    2. is unique - a different public user-key yields a different address
    3. is deterministic - same public user-key yields same address
    4. the addresser recognizes the address as a user-key
    5. the addresser can parse the address into its components
    6. the identifier is a hash of the user id
    7. the related identifier is a hash of the public key
    """
    key = helper.user.key().public_key
    user_id = helper.user.id()
    address = addresser.user.key.address(user_id, key)

    assert assert_is_address(address)
    assert address != addresser.user.key.address(user_id, helper.user.key().public_key)
    assert address != addresser.user.key.address(helper.user.id(), key)
    assert address == addresser.user.key.address(user_id, key)

    assert addresser.get_address_type(address) == addresser.AddressSpace.USER_KEY
    assert addresser.get_address_type(address) == addresser.AddressSpace.USER_KEY

    parsed = addresser.parse(address)

    assert parsed.object_type == addresser.ObjectType.USER
    assert parsed.related_type == addresser.ObjectType.KEY
    assert parsed.relationship_type == addresser.RelationshipType.OWNER
    assert assert_is_identifier(parsed.object_id)

    assert parsed.object_id == addresser.user.hash(user_id)
    assert parsed.related_id == addresser.key.hash(key)
