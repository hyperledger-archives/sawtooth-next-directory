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

import pytest
import unittest
import logging
from rbac.addressing import addresser
from rbac.addressing.addresser import AddressSpace

LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.addressing
class TestSysAdminAttributesAddresser(unittest.TestCase):
    def test_determine_sysadmin_addr(self):
        """Tests that a specific sysadmin_id generates the expected
        sysadmin address, and thus is probably deterministic.
        """

        expected_address = "9f4448000000000000000000000000\
0000000000000000000000000000000000000000"

        address = addresser.make_sysadmin_attr_address()

        self.assertEqual(
            len(address), addresser.ADDRESS_LENGTH, "The address is 70 characters"
        )

        self.assertTrue(
            addresser.is_address(address), "The address is 70 character hexidecimal"
        )

        self.assertTrue(
            addresser.namespace_ok(address), "The address has correct namespace prefix"
        )

        self.assertTrue(
            addresser.is_family_address(address),
            "The address is 70 character hexidecimal with family prefix",
        )

        self.assertEqual(
            address, expected_address, "The address is the one we expected it to be"
        )

        self.assertEqual(
            addresser.address_is(address),
            AddressSpace.SYSADMIN_ATTRIBUTES,
            "The address created must be a SysAdmin Attributes address.",
        )
