# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Test Addresser"""
import pytest

from rbac.common import addresser
from rbac.common.logs import get_default_logger
from tests.rbac.common.assertions import TestAssertions

LOGGER = get_default_logger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestAddresser(TestAssertions):
    """Test Addresser"""

    def test_family_props(self):
        """Test the addresser family has the expected properties"""
        self.assertIsInstance(addresser.family.name, str)
        self.assertIsInstance(addresser.family.version, str)
        self.assertIsInstance(addresser.family.pattern.pattern, str)

    def test_unique_id(self):
        """Test unique_id returns unique identifiers"""
        unique_id1 = addresser.role.unique_id()
        unique_id2 = addresser.role.unique_id()

        self.assertIsIdentifier(unique_id1)
        self.assertIsIdentifier(unique_id2)
        self.assertNotEqual(unique_id1, unique_id2)

    def test_hash(self):
        """Test hash returns unique identifiers"""
        hash1 = addresser.role.hash(addresser.role.unique_id())
        hash2 = addresser.role.hash(addresser.role.unique_id())

        self.assertIsIdentifier(hash1)
        self.assertIsIdentifier(hash2)
        self.assertNotEqual(hash1, hash2)
