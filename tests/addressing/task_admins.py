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
class TestTaskAdminsAddresser(unittest.TestCase):
    def test_determine_task_admin_addr(self):
        """Tests that a specific task_id and admin_id generates the
        expected task admin address, and thus is probably deterministic.
        """

        task_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        admin_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f44481e326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2848"
        address = addresser.make_task_admins_address(task_id, admin_id)

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
            AddressSpace.TASKS_ADMINS,
            "The address created must be a Task Attributes address.",
        )

    def test_generated_task_admin_addr(self):
        """Tests the task admin address creation function as well as the
        address_is function.
        """

        task_id = uuid4().hex
        admin_id = uuid4().hex
        address = addresser.make_task_admins_address(task_id, admin_id)

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
            AddressSpace.TASKS_ADMINS,
            "The address created must be a Task Attributes address.",
        )
