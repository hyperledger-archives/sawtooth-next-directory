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
"""Common assertion helpers"""
# pylint: disable=no-member,invalid-name

import re
from unittest import TestCase
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)
HEX_PATTERN = re.compile(r"^[0-9a-fA-F]{2,}$")


class CommonAssertions(TestCase):
    """Common assertion helpers"""

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

    def assertHasProp(self, item, name):
        """Tests an object has the named property, and that
        retrieving that property does not throw an exception"""
        self.assertIsInstance(item, object)
        self.assertIsInstance(name, str)
        self.assertTrue(
            hasattr(item, name), "Expected {}.{} to exist".format(item, name)
        )
        getattr(item, name)

    def assertHasProps(self, item, names):
        """Tests an object has the named properties, and that
        retrieving those properties does not throw an exception"""
        self.assertIsInstance(item, object)
        self.assertIsInstance(names, list)
        for name in names:
            self.assertHasProp(item, name)

    def assertHasMethod(self, item, name):
        """Tests an object has the named method"""
        self.assertIsInstance(item, object)
        self.assertIsInstance(name, str)
        self.assertTrue(
            hasattr(item, name), "Expected {}.{} to exist".format(item, name)
        )
        method = getattr(item, name)
        self.assertTrue(
            callable(method), "Expected {}.{} to be callable".format(item, name)
        )

    def assertHasMethods(self, item, names):
        """Tests an object has all the named methods"""
        self.assertIsInstance(item, object)
        self.assertIsInstance(names, list)
        for name in names:
            self.assertHasMethod(item, name)
