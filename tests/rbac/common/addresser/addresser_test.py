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
from rbac.common.addresser.address_space import AddressSpace
from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.unit
class TestAddresser(AddressAssertions):
    def test_import(self):
        self.assertEqual(addresser.AddressSpace, AddressSpace)
        self.assertIsInstance(addresser.family.name, str)
        self.assertIsInstance(addresser.family.version, str)
        self.assertIsInstance(addresser.family.pattern.pattern, str)
        self.assertTrue(callable(addresser.family.is_family))
        self.assertTrue(callable(addresser.address_is))

    def test_unique_id(self):
        self.assertTrue(callable(addresser.role.unique_id))

        unique_id1 = addresser.role.unique_id()
        unique_id2 = addresser.role.unique_id()

        self.assertIsInstance(unique_id1, str)
        self.assertIsInstance(unique_id2, str)
        self.assertEqual(len(unique_id1), 24)
        self.assertEqual(len(unique_id2), 24)
        self.assertNotEqual(unique_id1, unique_id2)

    def test_hash(self):
        self.assertTrue(callable(addresser.role.hash))

        hash1 = addresser.role.hash(addresser.role.unique_id())
        hash2 = addresser.role.hash(addresser.role.unique_id())

        self.assertIsInstance(hash1, str)
        self.assertIsInstance(hash2, str)
        self.assertEqual(len(hash1), 24)
        self.assertEqual(len(hash2), 24)
        self.assertNotEqual(hash1, hash2)
