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
"""Test SysAdmin Addresser"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestSysAdminAddresser(TestAssertions):
    """Test SysAdmin Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        sysadmin_address = addresser.sysadmin.address()
        self.assertIsAddress(sysadmin_address)
        self.assertEqual(
            addresser.get_address_type(sysadmin_address),
            addresser.AddressSpace.SYSADMIN_ATTRIBUTES,
        )

    def test_addresser_parse(self):
        """Test addresser.parse returns a parsed address"""
        user_id = addresser.user.unique_id()
        sysadmin_address = addresser.sysadmin.address()

        parsed = addresser.parse(sysadmin_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.SYSADMIN)
        self.assertEqual(parsed.related_type, addresser.ObjectType.NONE)
        self.assertEqual(
            parsed.relationship_type, addresser.RelationshipType.ATTRIBUTES
        )
        self.assertEqual(
            parsed.address_type, addresser.AddressSpace.SYSADMIN_ATTRIBUTES
        )
        self.assertEqual(parsed.object_id, "000000000000000000000000")
        self.assertEqual(parsed.related_id, None)
