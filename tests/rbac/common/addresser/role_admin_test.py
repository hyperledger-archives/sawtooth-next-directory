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
"""Test Role Admin Addresser"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestRoleAdminAddresser(TestAssertions):
    """Test Role Admin Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = addresser.role.admin.unique_id()
        user_id = addresser.user.unique_id()
        rel_address = addresser.role.admin.address(
            object_id=role_id, related_id=user_id
        )
        self.assertIsAddress(rel_address)
        self.assertEqual(
            addresser.get_address_type(rel_address), addresser.AddressSpace.ROLES_ADMINS
        )

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = addresser.role.admin.unique_id()
        user_id = addresser.user.unique_id()
        rel_address1 = addresser.role.admin.address(
            object_id=role_id, related_id=user_id
        )
        rel_address2 = addresser.role.admin.address(
            object_id=role_id, related_id=user_id
        )
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.get_address_type(rel_address1),
            addresser.AddressSpace.ROLES_ADMINS,
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        role_id1 = addresser.role.admin.unique_id()
        user_id1 = addresser.user.unique_id()
        role_id2 = addresser.role.admin.unique_id()
        user_id2 = addresser.user.unique_id()
        rel_address1 = addresser.role.admin.address(
            object_id=role_id1, related_id=user_id1
        )
        rel_address2 = addresser.role.admin.address(
            object_id=role_id2, related_id=user_id2
        )
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertNotEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.get_address_type(rel_address1),
            addresser.AddressSpace.ROLES_ADMINS,
        )
        self.assertEqual(
            addresser.get_address_type(rel_address2),
            addresser.AddressSpace.ROLES_ADMINS,
        )

    def test_addresser_parse(self):
        """Test addresser.parse returns a parsed address"""
        role_id = addresser.role.unique_id()
        user_id = addresser.user.unique_id()
        rel_address = addresser.role.admin.address(role_id, user_id)

        parsed = addresser.parse(rel_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.ROLE)
        self.assertEqual(parsed.related_type, addresser.ObjectType.USER)
        self.assertEqual(parsed.relationship_type, addresser.RelationshipType.ADMIN)
        self.assertEqual(parsed.address_type, addresser.AddressSpace.ROLES_ADMINS)
        self.assertEqual(parsed.object_id, role_id)
        self.assertEqual(parsed.related_id, user_id)
