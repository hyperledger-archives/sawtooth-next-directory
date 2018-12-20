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
"""Address assertion helpers"""
# pylint: disable=invalid-name

import logging
import re as regex
from rbac.common import addresser
from tests.rbac.common.assertions.key import KeyAssertions

LOGGER = logging.getLogger(__name__)

PATTERN_ADDRESS = regex.compile(r"^[0-9a-f]{70}$")
PATTERN_IDENTIFIER = regex.compile(r"^[0-9a-f]{24}$")
ADDRESS_CLASS_METHODS = ["address", "get_address_type", "hash", "unique_id"]
ADDRESS_CLASS_PROPS = ["address_type"]


class AddressAssertions(KeyAssertions):
    """Address assertion helpers"""

    def assertIsAddressClass(self, value):
        """Has the properties and methods expected of an address class"""
        self.assertHasMethods(value, ADDRESS_CLASS_METHODS)
        self.assertHasProps(value, ADDRESS_CLASS_PROPS)

    def assertIsAddress(self, value):
        """Is a 70 character hex string with the correct transaction family prefix"""
        self.assertIsInstance(value, str)
        self.assertEqual(
            len(value),
            70,
            "Expected address to be 70 characters, got {}; {}".format(
                len(value), value
            ),
        )
        self.assertTrue(
            PATTERN_ADDRESS.match(value),
            "Expected address to a lowercase 70 characater hexadecimal string. Got {}".format(
                value
            ),
        )
        self.assertTrue(
            addresser.family.is_family(value),
            "Expected address to be of the correct transaction family. Got {}".format(
                value
            ),
        )

    def assertIsIdentifier(self, value):
        """Tests the value id an identifier (24 character hexadecimal value)"""
        self.assertIsInstance(value, str)
        self.assertTrue(
            PATTERN_IDENTIFIER.match(value),
            "Expected id to a lowercase 24 characater hexadecimal string. Got {}".format(
                value
            ),
        )
