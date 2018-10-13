# Copyright contributors to Hyperledger Sawtooth
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

import re
from unittest import TestCase

HEX_PATTERN = re.compile(r"^[0-9a-fA-F]{2,}$")


class CommonAssertions(TestCase):
    def assertIsString(self, value):
        """Value is a non-zero length string"""
        self.assertIsInstance(value, str)
        self.assertGreater(len(value), 0)

    def assertIsIntegerString(self, value):
        """Value is the string representation of an integer"""
        self.assertIsString(value)
        self.assertEqual(str(int(value)), value)

    def assertIsHexString(self, value):
        """Value is a hexadecimal string"""
        self.assertIsString(value)
        self.assertEqual(len(value) % 2, 0, "Expected even number length")
        self.assertTrue(HEX_PATTERN.match(value))
