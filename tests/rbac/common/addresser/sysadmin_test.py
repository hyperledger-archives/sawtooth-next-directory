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
from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.unit
class TestSysAdminAddresser(AddressAssertions):
    def test_import(self):
        self.assertIsInstance(addresser.sysadmin, SysAdminAddress)
        self.assertIsAddressClass(addresser.sysadmin)

    def test_address(self):
        sysadmin_id = addresser.sysadmin.unique_id()
        sysadmin_address = addresser.sysadmin.address()
        self.assertIsAddress(sysadmin_address)
        self.assertEqual(
            addresser.address_is(sysadmin_address),
            addresser.AddressSpace.SYSADMIN_ATTRIBUTES,
        )

    def test_address_static(self):
        expected_address = "9f4448000000000000000000000000\
0000000000000000000000000000000000000000"
        sysadmin_address = addresser.sysadmin.address()
        self.assertIsAddress(sysadmin_address)
        self.assertEqual(sysadmin_address, expected_address)
        self.assertEqual(
            addresser.address_is(sysadmin_address),
            addresser.AddressSpace.SYSADMIN_ATTRIBUTES,
        )
