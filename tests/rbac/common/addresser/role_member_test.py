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

import logging
import pytest

from rbac.common import addresser
from rbac.common.addresser.role import RoleAddress
from rbac.common.addresser.role import RoleMemberAddress
from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.unit
class TestRoleMemberAddresser(AddressAssertions):
    def test_import(self):
        self.assertIsInstance(addresser.role, RoleAddress)
        self.assertIsInstance(addresser.role.member, RoleMemberAddress)
        self.assertIsAddressClass(addresser.role.member)

    def test_address(self):
        role_id = addresser.role.member.unique_id()
        user_id = addresser.user.unique_id()
        rel_address = addresser.role.member.address(
            object_id=role_id, target_id=user_id
        )
        self.assertIsAddress(rel_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_MEMBERS
        )

    def test_address_deterministic(self):
        role_id = addresser.role.member.unique_id()
        user_id = addresser.user.unique_id()
        rel_address1 = addresser.role.member.address(
            object_id=role_id, target_id=user_id
        )
        rel_address2 = addresser.role.member.address(
            object_id=role_id, target_id=user_id
        )
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.address_is(rel_address1), addresser.AddressSpace.ROLES_MEMBERS
        )

    def test_address_random(self):
        role_id1 = addresser.role.member.unique_id()
        user_id1 = addresser.user.unique_id()
        role_id2 = addresser.role.member.unique_id()
        user_id2 = addresser.user.unique_id()
        rel_address1 = addresser.role.member.address(
            object_id=role_id1, target_id=user_id1
        )
        rel_address2 = addresser.role.member.address(
            object_id=role_id2, target_id=user_id2
        )
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertNotEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.address_is(rel_address1), addresser.AddressSpace.ROLES_MEMBERS
        )
        self.assertEqual(
            addresser.address_is(rel_address2), addresser.AddressSpace.ROLES_MEMBERS
        )

    def test_address_static(self):
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f444809326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2833"
        rel_address = addresser.role.member.address(
            object_id=role_id, target_id=user_id
        )
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_MEMBERS
        )
