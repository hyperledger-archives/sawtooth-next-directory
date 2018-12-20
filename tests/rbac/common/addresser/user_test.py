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
"""Test User Addresser"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestUserAddresser(TestAssertions):
    """Test User Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        user_id = addresser.user.unique_id()
        user_address = addresser.user.address(user_id)
        self.assertIsAddress(user_address)
        self.assertEqual(
            addresser.get_address_type(user_address), addresser.AddressSpace.USER
        )

    def test_unique_id(self):
        """Tests that unique_id generates a unique identifier and is unique"""
        id1 = addresser.user.unique_id()
        id2 = addresser.user.unique_id()
        self.assertIsIdentifier(id1)
        self.assertIsIdentifier(id2)
        self.assertNotEqual(id1, id2)

    def test_get_address_type(self):
        """Tests that get_address_type returns AddressSpace.USER if it is a user
        address, and None if it is of another address type"""
        user_address = addresser.user.address(addresser.user.unique_id())
        role_address = addresser.role.address(addresser.role.unique_id())
        self.assertEqual(
            addresser.get_address_type(user_address), addresser.AddressSpace.USER
        )
        self.assertEqual(
            addresser.user.get_address_type(user_address), addresser.AddressSpace.USER
        )
        self.assertIsNone(addresser.user.get_address_type(role_address))
        self.assertEqual(
            addresser.get_address_type(role_address),
            addresser.AddressSpace.ROLES_ATTRIBUTES,
        )

    def test_get_addresser(self):
        """Test that get_addresser returns the addresser class if it is a
        user address, and None if it is of another address type"""
        user_address = addresser.user.address(addresser.user.unique_id())
        other_address = addresser.role.address(addresser.role.unique_id())
        self.assertIsInstance(
            addresser.get_addresser(user_address), type(addresser.user)
        )
        self.assertIsInstance(
            addresser.user.get_addresser(user_address), type(addresser.user)
        )
        self.assertIsNone(addresser.user.get_addresser(other_address))

    def test_user_parse(self):
        """Test addresser.user.parse returns a parsed address if it is a user address"""
        user_id = addresser.user.unique_id()
        user_address = addresser.user.address(user_id)
        parsed = addresser.user.parse(user_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.USER)
        self.assertEqual(parsed.related_type, addresser.ObjectType.NONE)
        self.assertEqual(
            parsed.relationship_type, addresser.RelationshipType.ATTRIBUTES
        )
        self.assertEqual(parsed.address_type, addresser.AddressSpace.USER)
        self.assertEqual(parsed.object_id, user_id)
        self.assertEqual(parsed.related_id, None)

    def test_addresser_parse(self):
        """Test addresser.parse returns a parsed address"""
        user_id = addresser.user.unique_id()
        user_address = addresser.user.address(user_id)
        parsed = addresser.parse(user_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.USER)
        self.assertEqual(parsed.related_type, addresser.ObjectType.NONE)
        self.assertEqual(
            parsed.relationship_type, addresser.RelationshipType.ATTRIBUTES
        )
        self.assertEqual(parsed.address_type, addresser.AddressSpace.USER)
        self.assertEqual(parsed.object_id, user_id)
        self.assertEqual(parsed.related_id, None)

    def test_parse_other(self):
        """Test that parse returns None if it is not a user address"""
        other_address = addresser.role.address(addresser.role.unique_id())
        self.assertIsNone(addresser.user.parse(other_address))

    def test_addresses_are(self):
        """Test that addresses_are returns True if all addresses are a user
        addresses, and False if any addresses are if a different address type"""
        user_address1 = addresser.user.address(addresser.user.unique_id())
        user_address2 = addresser.user.address(addresser.user.unique_id())
        other_address = addresser.role.address(addresser.role.unique_id())
        self.assertTrue(addresser.user.addresses_are([user_address1]))
        self.assertTrue(addresser.user.addresses_are([user_address1, user_address2]))
        self.assertFalse(addresser.user.addresses_are([other_address]))
        self.assertFalse(addresser.user.addresses_are([user_address1, other_address]))
        self.assertFalse(addresser.user.addresses_are([other_address, user_address1]))
        self.assertTrue(addresser.user.addresses_are([]))

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        user_id1 = addresser.user.unique_id()
        user_address1 = addresser.user.address(user_id1)
        user_address2 = addresser.user.address(user_id1)
        self.assertIsAddress(user_address1)
        self.assertIsAddress(user_address2)
        self.assertEqual(user_address1, user_address2)
        self.assertEqual(
            addresser.get_address_type(user_address1), addresser.AddressSpace.USER
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        user_id1 = addresser.user.unique_id()
        user_id2 = addresser.user.unique_id()
        user_address1 = addresser.user.address(user_id1)
        user_address2 = addresser.user.address(user_id2)
        self.assertIsAddress(user_address1)
        self.assertIsAddress(user_address2)
        self.assertNotEqual(user_address1, user_address2)
        self.assertEqual(
            addresser.get_address_type(user_address1), addresser.AddressSpace.USER
        )
        self.assertEqual(
            addresser.get_address_type(user_address2), addresser.AddressSpace.USER
        )
