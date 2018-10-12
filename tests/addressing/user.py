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
from uuid import uuid4
from rbac.addressing import addresser
from rbac.addressing.addresser import AddressSpace

LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.addressing
class TestUserAddresser(unittest.TestCase):
    def test_deterministic_user_address(self):
        """Tests that a specific user_id generates the expected
        user address, and thus is probably deterministic.
        """

        ident = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f444847e7570f3f6f7d2c1635f6de\
eabc1f4d78d9d42b64b70e1819f244138c1e38d6"
        address = addresser.make_user_address(ident)

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
            AddressSpace.USER,
            "The User address created must be found to be a User address.",
        )

    def test_generated_user_address(self):
        """Tests the Users address creation function as well as the
        address_is function.
        """

        ident = uuid4().hex
        address = addresser.make_user_address(ident)

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
            addresser.address_is(address),
            AddressSpace.USER,
            "The address created must be found to be a User address.",
        )
