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
from rbac.common.crypto import hash_util
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestRoleAddresser(TestAssertions):
    """Test Role Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = hash_util.generate_12_byte_random_hex()
        role_address = addresser.role.address(object_id=role_id)
        self.assertIsAddress(role_address)
        self.assertEqual(
            addresser.address_is(role_address), addresser.AddressSpace.ROLES_ATTRIBUTES
        )

    def test_get_address_type(self):
        """Tests that get_address_type returns AddressSpace.USER if it is a role
        address, and None if it is of another address type"""
        role_address = addresser.role.address(hash_util.generate_12_byte_random_hex())
        other_address = addresser.user.address(hash_util.generate_12_byte_random_hex())
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
        role_address1 = addresser.role.address(hash_util.generate_12_byte_random_hex())
        role_address2 = addresser.role.address(hash_util.generate_12_byte_random_hex())
        other_address = addresser.user.address(hash_util.generate_12_byte_random_hex())
        self.assertTrue(addresser.role.addresses_are([role_address1]))
        self.assertTrue(addresser.role.addresses_are([role_address1, role_address2]))
        self.assertFalse(addresser.role.addresses_are([other_address]))
        self.assertFalse(addresser.role.addresses_are([role_address1, other_address]))
        self.assertFalse(addresser.role.addresses_are([other_address, role_address1]))
        self.assertTrue(addresser.role.addresses_are([]))

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id1 = hash_util.generate_12_byte_random_hex()
        role_address1 = addresser.role.address(object_id=role_id1)
        role_address2 = addresser.role.address(object_id=role_id1)
        self.assertIsAddress(role_address1)
        self.assertIsAddress(role_address2)
        self.assertEqual(role_address1, role_address2)
        self.assertEqual(
            addresser.address_is(role_address1), addresser.AddressSpace.ROLES_ATTRIBUTES
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        role_id1 = hash_util.generate_12_byte_random_hex()
        role_id2 = hash_util.generate_12_byte_random_hex()
        role_address1 = addresser.role.address(object_id=role_id1)
        role_address2 = addresser.role.address(object_id=role_id2)
        self.assertIsAddress(role_address1)
        self.assertIsAddress(role_address2)
        self.assertNotEqual(role_address1, role_address2)
        self.assertEqual(
            addresser.address_is(role_address1), addresser.AddressSpace.ROLES_ATTRIBUTES
        )
        self.assertEqual(
            addresser.address_is(role_address2), addresser.AddressSpace.ROLES_ATTRIBUTES
        )

    def test_address_static(self):
        """Tests address makes the expected output given a specific input"""
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        expected_address = (
            "bac00100005555326a1713a905b26359fc8da21111ff00000000000000000000000000"
        )
        role_address = addresser.role.address(object_id=role_id)
        self.assertIsAddress(role_address)
        self.assertEqual(role_address, expected_address)
        self.assertEqual(
            addresser.address_is(role_address), addresser.AddressSpace.ROLES_ATTRIBUTES
        )
