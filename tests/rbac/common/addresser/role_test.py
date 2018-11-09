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
from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.unit
class TestRoleAddresser(AddressAssertions):
    def test_import(self):
        self.assertIsInstance(addresser.role, RoleAddress)
        self.assertIsAddressClass(addresser.role)

    def test_address(self):
        role_id = addresser.role.unique_id()
        role_address = addresser.role.address(object_id=role_id)
        self.assertIsAddress(role_address)
        self.assertEqual(
            addresser.address_is(role_address), addresser.AddressSpace.ROLES_ATTRIBUTES
        )

    def test_address_deterministic(self):
        role_id1 = addresser.role.unique_id()
        role_address1 = addresser.role.address(object_id=role_id1)
        role_address2 = addresser.role.address(object_id=role_id1)
        self.assertIsAddress(role_address1)
        self.assertIsAddress(role_address2)
        self.assertEqual(role_address1, role_address2)
        self.assertEqual(
            addresser.address_is(role_address1), addresser.AddressSpace.ROLES_ATTRIBUTES
        )

    def test_address_random(self):
        role_id1 = addresser.role.unique_id()
        role_id2 = addresser.role.unique_id()
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
