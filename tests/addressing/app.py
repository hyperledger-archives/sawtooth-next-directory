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
from hashlib import sha512
from rbac.addressing import addresser

LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.addressing
class TestAddresser(unittest.TestCase):
    def test_namespace(self):
        self.assertEqual(addresser.FAMILY_NAME, "rbac")

        namespace = sha512(addresser.FAMILY_NAME.encode()).hexdigest()[:6]

        self.assertEqual(addresser.NS, namespace)
        self.assertEqual(addresser.NS, "9f4448")

    def test_short_address(self):
        """Tests that an address that is too short does not validate.
        """

        address = "9f444847e7570f3f6f7d2c1635f6de\
eabc1f4d78d9d42b64b70e1819f244138c1e38"

        self.assertFalse(
            len(address) == addresser.ADDRESS_LENGTH, "The address is not 70 characters"
        )

        self.assertFalse(
            addresser.is_address(address), "The address is not 70 character hexidecimal"
        )

        self.assertFalse(
            addresser.is_family_address(address),
            "The address is not 70 character hexidecimal with family prefix",
        )

        with self.assertRaises(ValueError):
            addresser.address_is(address)

    def test_long_address(self):
        """Tests that an address that is too long does not validate.
        """

        address = "9f444847e7570f3f6f7d2c1635f6de\
eabc1f4d78d9d42b64b70e1819f244138c1e38d6fe"

        self.assertFalse(
            len(address) == addresser.ADDRESS_LENGTH, "The address is not 70 characters"
        )

        self.assertFalse(
            addresser.is_address(address), "The address is not 70 character hexidecimal"
        )

        self.assertFalse(
            addresser.is_family_address(address),
            "The address is not 70 character hexidecimal with family prefix",
        )

        with self.assertRaises(ValueError):
            addresser.address_is(address)

    def test_nonhex_address(self):
        """Tests that an address that is not hex does not validate.
        """

        address = "9f444847e7570f3f6f7d2c1635f6de\
eabc1f4d78d9d42b64b70e1819f244138c1e38X6"

        self.assertFalse(
            addresser.is_address(address), "The address is not 70 character hexidecimal"
        )

        self.assertFalse(
            addresser.is_family_address(address),
            "The address is not 70 character hexidecimal with family prefix",
        )

        with self.assertRaises(ValueError):
            addresser.address_is(address)

    def test_wrong_family_address(self):
        """Tests that an address with the wrong family prefix
        does not validate.
        """

        address = "8f444847e7570f3f6f7d2c1635f6de\
eabc1f4d78d9d42b64b70e1819f244138c1e38d6"

        self.assertEqual(
            len(address), addresser.ADDRESS_LENGTH, "The address is 70 characters"
        )

        self.assertTrue(
            addresser.is_address(address), "The address is 70 character hexidecimal"
        )

        self.assertFalse(
            addresser.namespace_ok(address),
            "The address does not have correct namespace prefix",
        )

        self.assertFalse(
            addresser.is_family_address(address),
            "The address is not 70 character hexidecimal with family prefix",
        )

        with self.assertRaises(ValueError):
            addresser.address_is(address)
