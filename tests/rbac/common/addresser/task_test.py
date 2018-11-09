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
from rbac.common.addresser.task import TaskAddress
from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.unit
class TestTaskAddresser(AddressAssertions):
    def test_import(self):
        self.assertIsInstance(addresser.task, TaskAddress)
        self.assertIsAddressClass(addresser.task)

    def test_address(self):
        task_id = addresser.task.unique_id()
        task_address = addresser.task.address(object_id=task_id)
        self.assertIsAddress(task_address)
        self.assertEqual(
            addresser.address_is(task_address), addresser.AddressSpace.TASKS_ATTRIBUTES
        )

    def test_address_deterministic(self):
        task_id1 = addresser.task.unique_id()
        task_address1 = addresser.task.address(object_id=task_id1)
        task_address2 = addresser.task.address(object_id=task_id1)
        self.assertIsAddress(task_address1)
        self.assertIsAddress(task_address2)
        self.assertEqual(task_address1, task_address2)
        self.assertEqual(
            addresser.address_is(task_address1), addresser.AddressSpace.TASKS_ATTRIBUTES
        )

    def test_address_random(self):
        task_id1 = addresser.task.unique_id()
        task_id2 = addresser.task.unique_id()
        task_address1 = addresser.task.address(object_id=task_id1)
        task_address2 = addresser.task.address(object_id=task_id2)
        self.assertIsAddress(task_address1)
        self.assertIsAddress(task_address2)
        self.assertNotEqual(task_address1, task_address2)
        self.assertEqual(
            addresser.address_is(task_address1), addresser.AddressSpace.TASKS_ATTRIBUTES
        )
        self.assertEqual(
            addresser.address_is(task_address2), addresser.AddressSpace.TASKS_ATTRIBUTES
        )

    def test_address_static(self):
        task_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        expected_address = (
            "bac00100006666326a1713a905b26359fc8da21111ff00000000000000000000000000"
        )
        task_address = addresser.task.address(object_id=task_id)
        self.assertIsAddress(task_address)
        self.assertEqual(task_address, expected_address)
        self.assertEqual(
            addresser.address_is(task_address), addresser.AddressSpace.TASKS_ATTRIBUTES
        )
