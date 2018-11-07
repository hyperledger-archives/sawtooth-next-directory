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
from rbac.common.addresser.sysadmin import SysAdminAddress
from rbac.common.addresser.sysadmin import SysAdminMemberAddress
from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.unit
class TestSysAdminMemberAddresser(AddressAssertions):
    def test_import(self):
        self.assertIsInstance(addresser.sysadmin, SysAdminAddress)
        self.assertIsInstance(addresser.sysadmin.member, SysAdminMemberAddress)
        self.assertIsAddressClass(addresser.sysadmin.member)

    def test_address(self):
        user_id = addresser.user.unique_id()
        rel_address = addresser.sysadmin.member.address(object_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.SYSADMIN_MEMBERS
        )

    def test_address_deterministic(self):
        user_id = addresser.user.unique_id()
        rel_address1 = addresser.sysadmin.member.address(object_id=user_id)
        rel_address2 = addresser.sysadmin.member.address(object_id=user_id)
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.address_is(rel_address1), addresser.AddressSpace.SYSADMIN_MEMBERS
        )

    @pytest.mark.skip("hash collision on legacy addressing scheme can cause match")
    def test_address_random(self):
        user_id1 = addresser.user.unique_id()
        user_id2 = addresser.user.unique_id()
        rel_address1 = addresser.sysadmin.member.address(object_id=user_id1)
        rel_address2 = addresser.sysadmin.member.address(object_id=user_id2)
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertNotEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.address_is(rel_address1), addresser.AddressSpace.SYSADMIN_MEMBERS
        )
        self.assertEqual(
            addresser.address_is(rel_address2), addresser.AddressSpace.SYSADMIN_MEMBERS
        )

    def test_address_static(self):
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f4448000000000000000000000000\
0000000000000000000000000000000000000083"
        rel_address = addresser.sysadmin.member.address(object_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.SYSADMIN_MEMBERS
        )
