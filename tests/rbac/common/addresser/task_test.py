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
class TestTaskAddresser(TestAssertions):
    """Test Task Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        task_id = addresser.task.unique_id()
        task_address = addresser.task.address(object_id=task_id)
        self.assertIsAddress(task_address)
        self.assertEqual(
            addresser.get_address_type(task_address),
            addresser.AddressSpace.TASKS_ATTRIBUTES,
        )

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        task_id1 = addresser.task.unique_id()
        task_address1 = addresser.task.address(object_id=task_id1)
        task_address2 = addresser.task.address(object_id=task_id1)
        self.assertIsAddress(task_address1)
        self.assertIsAddress(task_address2)
        self.assertEqual(task_address1, task_address2)
        self.assertEqual(
            addresser.get_address_type(task_address1),
            addresser.AddressSpace.TASKS_ATTRIBUTES,
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        task_id1 = addresser.task.unique_id()
        task_id2 = addresser.task.unique_id()
        task_address1 = addresser.task.address(object_id=task_id1)
        task_address2 = addresser.task.address(object_id=task_id2)
        self.assertIsAddress(task_address1)
        self.assertIsAddress(task_address2)
        self.assertNotEqual(task_address1, task_address2)
        self.assertEqual(
            addresser.get_address_type(task_address1),
            addresser.AddressSpace.TASKS_ATTRIBUTES,
        )
        self.assertEqual(
            addresser.get_address_type(task_address2),
            addresser.AddressSpace.TASKS_ATTRIBUTES,
        )

    def test_addresser_parse(self):
        """Test addresser.parse returns a parsed address"""
        task_id = addresser.task.unique_id()
        task_address = addresser.task.address(task_id)

        parsed = addresser.parse(task_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.TASK)
        self.assertEqual(parsed.related_type, addresser.ObjectType.NONE)
        self.assertEqual(
            parsed.relationship_type, addresser.RelationshipType.ATTRIBUTES
        )
        self.assertEqual(parsed.address_type, addresser.AddressSpace.TASKS_ATTRIBUTES)
        self.assertEqual(parsed.object_id, task_id)
        self.assertEqual(parsed.related_id, None)
