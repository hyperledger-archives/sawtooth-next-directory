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
"""Test Role Addresser"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestRoleAddresser(TestAssertions):
    """Test Role Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = addresser.role.unique_id()
        role_address = addresser.role.address(object_id=role_id)
        self.assertIsAddress(role_address)
        self.assertEqual(
            addresser.get_address_type(role_address),
            addresser.AddressSpace.ROLES_ATTRIBUTES,
        )

    def test_get_address_type(self):
        """Tests that get_address_type returns AddressSpace.USER if it is a role
        address, and None if it is of another address type"""
        role_address = addresser.role.address(addresser.role.unique_id())
        other_address = addresser.user.address(addresser.user.unique_id())
        self.assertEqual(
            addresser.get_address_type(role_address),
            addresser.AddressSpace.ROLES_ATTRIBUTES,
        )
        self.assertEqual(
            addresser.role.get_address_type(role_address),
            addresser.AddressSpace.ROLES_ATTRIBUTES,
        )
        self.assertIsNone(addresser.role.get_address_type(other_address))

    def test_addresses_are(self):
        """Test that addresses_are returns True if all addresses are a role
        addresses, and False if any addresses are if a different address type"""
        role_address1 = addresser.role.address(addresser.role.unique_id())
        role_address2 = addresser.role.address(addresser.role.unique_id())
        other_address = addresser.user.address(addresser.user.unique_id())
        self.assertTrue(addresser.role.addresses_are([role_address1]))
        self.assertTrue(addresser.role.addresses_are([role_address1, role_address2]))
        self.assertFalse(addresser.role.addresses_are([other_address]))
        self.assertFalse(addresser.role.addresses_are([role_address1, other_address]))
        self.assertFalse(addresser.role.addresses_are([other_address, role_address1]))
        self.assertTrue(addresser.role.addresses_are([]))

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id1 = addresser.role.unique_id()
        role_address1 = addresser.role.address(object_id=role_id1)
        role_address2 = addresser.role.address(object_id=role_id1)
        self.assertIsAddress(role_address1)
        self.assertIsAddress(role_address2)
        self.assertEqual(role_address1, role_address2)
        self.assertEqual(
            addresser.get_address_type(role_address1),
            addresser.AddressSpace.ROLES_ATTRIBUTES,
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        role_id1 = addresser.role.unique_id()
        role_id2 = addresser.role.unique_id()
        role_address1 = addresser.role.address(object_id=role_id1)
        role_address2 = addresser.role.address(object_id=role_id2)
        self.assertIsAddress(role_address1)
        self.assertIsAddress(role_address2)
        self.assertNotEqual(role_address1, role_address2)
        self.assertEqual(
            addresser.get_address_type(role_address1),
            addresser.AddressSpace.ROLES_ATTRIBUTES,
        )
        self.assertEqual(
            addresser.get_address_type(role_address2),
            addresser.AddressSpace.ROLES_ATTRIBUTES,
        )

    def test_addresser_parse(self):
        """Test addresser.parse returns a parsed address"""
        role_id = addresser.role.unique_id()
        role_address = addresser.role.address(role_id)

        parsed = addresser.parse(role_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.ROLE)
        self.assertEqual(parsed.related_type, addresser.ObjectType.NONE)
        self.assertEqual(
            parsed.relationship_type, addresser.RelationshipType.ATTRIBUTES
        )
        self.assertEqual(parsed.address_type, addresser.AddressSpace.ROLES_ATTRIBUTES)
        self.assertEqual(parsed.object_id, role_id)
        self.assertEqual(parsed.related_id, None)
