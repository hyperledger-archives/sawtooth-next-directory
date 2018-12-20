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
"""Test Addressing an email"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac import helper
from tests.rbac.test.assertions import assert_is_address
from tests.rbac.test.assertions import assert_is_identifier

LOGGER = logging.getLogger(__name__)


@pytest.mark.library
@pytest.mark.addressing
@pytest.mark.address_email
def test_addressing_email():
    """Tests making a blockchain address for an email and that it:
    1. is a 35-byte non-zero hexadecimal string
    2. is unique - a different email yields a different address
    3. is deterministic - same email yields same address, even if different case
    4. the addresser recognizes the address as an email
    5. the addresser can parse the address into its components
    6. the identifier is a hash of the email"""
    email = helper.user.email()
    address = addresser.email.address(email)

    assert assert_is_address(address)
    assert address != addresser.email.address(helper.user.email())
    assert address == addresser.email.address(email)
    assert address == addresser.email.address(email.upper())

    assert addresser.get_address_type(address) == addresser.AddressSpace.EMAIL

    parsed = addresser.parse(address)

    assert parsed.object_type == addresser.ObjectType.EMAIL
    assert parsed.related_type == addresser.ObjectType.NONE
    assert parsed.relationship_type == addresser.RelationshipType.NONE
    assert assert_is_identifier(parsed.object_id)
    assert not parsed.related_id

    assert parsed.object_id == addresser.email.hash(email)
