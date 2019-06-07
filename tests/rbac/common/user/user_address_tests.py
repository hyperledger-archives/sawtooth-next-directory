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
"""Test Addressing a user and user objects"""
import pytest

from rbac.common import addresser
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper
from tests.rbac.test.assertions import assert_is_address
from tests.rbac.test.assertions import assert_is_identifier

LOGGER = get_default_logger(__name__)


@pytest.mark.library
@pytest.mark.addressing
@pytest.mark.user_address
def test_addressing_user():
    """Tests making a blockchain address for an next_id and that it:
    1. is a 35-byte non-zero hexadecimal string
    2. is unique - a different next_id yields a different address
    3. is deterministic - same next_id yields same address, even if different case
    4. the addresser recognizes the address as an next_id
    5. the addresser can parse the address into its components
    6. the identifier is a hash of the next_id"""
    next_id = helper.user.id()
    address = addresser.user.address(next_id)

    assert assert_is_address(address)
    assert address != addresser.user.address(helper.user.id())
    assert address == addresser.user.address(next_id)
    assert address == addresser.user.address(next_id.upper())

    assert addresser.get_address_type(address) == addresser.AddressSpace.USER

    parsed = addresser.parse(address)

    assert parsed.object_type == addresser.ObjectType.USER
    assert parsed.related_type == addresser.ObjectType.NONE
    assert parsed.relationship_type == addresser.RelationshipType.ATTRIBUTES
    assert assert_is_identifier(parsed.object_id)
    assert not parsed.related_id

    assert parsed.object_id == addresser.user.hash(next_id)


@pytest.mark.library
@pytest.mark.addressing
@pytest.mark.user_address
def test_addressing_user_email():
    """Tests making a blockchain address for an user email and that it:
    1. is a 35-byte non-zero hexadecimal string
    2. is unique - a different user email yields a different address
    3. is deterministic - same user email yields same address, even if different case
    4. the addresser recognizes the address as an user email
    5. the addresser can parse the address into its components
    6. the identifier is a hash of the user email"""
    next_id = helper.user.id()
    email = helper.user.email()
    address = addresser.user.email.address(next_id, email)

    assert assert_is_address(address)
    assert address != addresser.user.email.address(next_id, helper.user.email())
    assert address == addresser.user.email.address(next_id, email)
    assert address == addresser.user.email.address(next_id, email.upper())

    assert addresser.get_address_type(address) == addresser.AddressSpace.USER_EMAIL

    parsed = addresser.parse(address)

    assert parsed.object_type == addresser.ObjectType.USER
    assert parsed.related_type == addresser.ObjectType.EMAIL
    assert parsed.relationship_type == addresser.RelationshipType.OWNER
    assert assert_is_identifier(parsed.object_id)
    assert assert_is_identifier(parsed.related_id)

    assert parsed.object_id == addresser.user.hash(next_id)
    assert parsed.related_id == addresser.email.hash(email)
