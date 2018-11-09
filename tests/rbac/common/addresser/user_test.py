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
from rbac.common.addresser.user import UserAddress
from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.wip
@pytest.mark.addressing
@pytest.mark.unit
class TestUserAddresser(AddressAssertions):
    def test_import(self):
        self.assertIsInstance(addresser.user, UserAddress)
        self.assertIsAddressClass(addresser.user)

    def test_address(self):
        user_id = addresser.user.unique_id()
        user_address = addresser.user.address(object_id=user_id)
        self.assertIsAddress(user_address)
        self.assertEqual(
            addresser.address_is(user_address), addresser.AddressSpace.USER
        )

    def test_address_deterministic(self):
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
