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
"""Test User Addresser"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.wip
class TestUserAddresser(TestAssertions):
    """Test User Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        user_id = addresser.user.unique_id()
        user_address = addresser.user.address(object_id=user_id)
        self.assertIsAddress(user_address)
        self.assertEqual(
            addresser.address_is(user_address), addresser.AddressSpace.USER
        )

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        user_id1 = addresser.user.unique_id()
        user_address1 = addresser.user.address(object_id=user_id1)
        user_address2 = addresser.user.address(object_id=user_id1)
        self.assertIsAddress(user_address1)
        self.assertIsAddress(user_address2)
        self.assertEqual(user_address1, user_address2)
        self.assertEqual(
            addresser.address_is(user_address1), addresser.AddressSpace.USER
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        user_id1 = addresser.user.unique_id()
        user_id2 = addresser.user.unique_id()
        user_address1 = addresser.user.address(object_id=user_id1)
        user_address2 = addresser.user.address(object_id=user_id2)
        self.assertIsAddress(user_address1)
        self.assertIsAddress(user_address2)
        self.assertNotEqual(user_address1, user_address2)
        self.assertEqual(
            addresser.address_is(user_address1), addresser.AddressSpace.USER
        )
        self.assertEqual(
            addresser.address_is(user_address2), addresser.AddressSpace.USER
        )

    def test_address_static(self):
        """Tests address makes the expected output given a specific input"""
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = (
            "bac00100003333e7570f3f6f7d2c1635f6deea1111ff00000000000000000000000000"
        )
        user_address = addresser.user.address(object_id=user_id)
        self.assertIsAddress(user_address)
        self.assertEqual(user_address, expected_address)
        self.assertEqual(
            addresser.address_is(user_address), addresser.AddressSpace.USER
        )
