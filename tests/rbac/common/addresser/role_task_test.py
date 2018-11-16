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
"""Test Task Addresser"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestRoleTaskAddresser(TestAssertions):
    """Test Task Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = addresser.role.task.unique_id()
        task_id = addresser.task.unique_id()
        rel_address = addresser.role.task.address(object_id=role_id, target_id=task_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_TASKS
        )

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = addresser.role.task.unique_id()
        task_id = addresser.task.unique_id()
        rel_address1 = addresser.role.task.address(object_id=role_id, target_id=task_id)
        rel_address2 = addresser.role.task.address(object_id=role_id, target_id=task_id)
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.address_is(rel_address1), addresser.AddressSpace.ROLES_TASKS
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        role_id1 = addresser.role.task.unique_id()
        task_id1 = addresser.task.unique_id()
        role_id2 = addresser.role.task.unique_id()
        task_id2 = addresser.task.unique_id()
        rel_address1 = addresser.role.task.address(
            object_id=role_id1, target_id=task_id1
        )
        rel_address2 = addresser.role.task.address(
            object_id=role_id2, target_id=task_id2
        )
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertNotEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.address_is(rel_address1), addresser.AddressSpace.ROLES_TASKS
        )
        self.assertEqual(
            addresser.address_is(rel_address2), addresser.AddressSpace.ROLES_TASKS
        )

    def test_address_static(self):
        """Tests address makes the expected output given a specific input"""
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        task_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = (
            "bac00100005555326a1713a905b26359fc8da26666bbe7570f3f6f7d2c1635f6deea00"
        )
        rel_address = addresser.role.task.address(object_id=role_id, target_id=task_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_TASKS
        )
