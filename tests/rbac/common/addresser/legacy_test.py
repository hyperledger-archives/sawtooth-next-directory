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

from rbac.common.crypto.keys import Key
from rbac.legacy import addresser as legacy
from rbac.common import addresser

from tests.rbac.common.addresser.address_assertions import AddressAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.unit
class TestAddressLegacyCompatibility(AddressAssertions):
    def test_legacy_attributes(self):
        self.assertEqual(addresser.family.name, legacy.FAMILY_NAME)
        self.assertEqual(addresser.family.version, legacy.FAMILY_VERSION)

    def test_legacy_address_space(self):
        self.assertEqual(
            addresser.AddressSpace.ROLES_ATTRIBUTES.value,
            legacy.AddressSpace.ROLES_ATTRIBUTES.value,
        )
        self.assertEqual(
            addresser.AddressSpace.ROLES_ADMINS.value,
            legacy.AddressSpace.ROLES_ADMINS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.ROLES_MEMBERS.value,
            legacy.AddressSpace.ROLES_MEMBERS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.ROLES_OWNERS.value,
            legacy.AddressSpace.ROLES_OWNERS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.ROLES_TASKS.value,
            legacy.AddressSpace.ROLES_TASKS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.PROPOSALS.value, legacy.AddressSpace.PROPOSALS.value
        )
        self.assertEqual(
            addresser.AddressSpace.TASKS_ADMINS.value,
            legacy.AddressSpace.TASKS_ADMINS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.TASKS_ATTRIBUTES.value,
            legacy.AddressSpace.TASKS_ATTRIBUTES.value,
        )
        self.assertEqual(
            addresser.AddressSpace.TASKS_OWNERS.value,
            legacy.AddressSpace.TASKS_OWNERS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.SYSADMIN_ADMINS.value,
            legacy.AddressSpace.SYSADMIN_ADMINS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.SYSADMIN_ATTRIBUTES.value,
            legacy.AddressSpace.SYSADMIN_ATTRIBUTES.value,
        )
        self.assertEqual(
            addresser.AddressSpace.SYSADMIN_MEMBERS.value,
            legacy.AddressSpace.SYSADMIN_MEMBERS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.SYSADMIN_OWNERS.value,
            legacy.AddressSpace.SYSADMIN_OWNERS.value,
        )
        self.assertEqual(
            addresser.AddressSpace.USER.value, legacy.AddressSpace.USER.value
        )

    def test_legacy_make_addresses(self):
        user_id = Key().public_key
        unique_id = addresser.role.unique_id()
        unique_id2 = addresser.task.unique_id()

        self.assertEqual(
            legacy.make_user_address(user_id=user_id),
            addresser.user.address(object_id=user_id),
        )

        self.assertEqual(
            legacy.make_role_attributes_address(role_id=unique_id),
            addresser.role.address(object_id=unique_id),
        )
        self.assertEqual(
            legacy.make_role_owners_address(role_id=unique_id, user_id=user_id),
            addresser.role.owner.address(object_id=unique_id, target_id=user_id),
        )
        self.assertEqual(
            legacy.make_role_admins_address(role_id=unique_id, user_id=user_id),
            addresser.role.admin.address(object_id=unique_id, target_id=user_id),
        )
        self.assertEqual(
            legacy.make_role_members_address(role_id=unique_id, user_id=user_id),
            addresser.role.member.address(object_id=unique_id, target_id=user_id),
        )
        self.assertEqual(
            legacy.make_role_tasks_address(role_id=unique_id, task_id=unique_id2),
            addresser.role.task.address(object_id=unique_id, target_id=unique_id2),
        )

        self.assertEqual(
            legacy.make_task_attributes_address(task_id=unique_id),
            addresser.task.address(object_id=unique_id),
        )
        self.assertEqual(
            legacy.make_task_owners_address(task_id=unique_id, user_id=user_id),
            addresser.task.owner.address(object_id=unique_id, target_id=user_id),
        )
        self.assertEqual(
            legacy.make_task_admins_address(task_id=unique_id, user_id=user_id),
            addresser.task.admin.address(object_id=unique_id, target_id=user_id),
        )

        self.assertEqual(
            legacy.make_sysadmin_attr_address(), addresser.sysadmin.address()
        )
        self.assertEqual(
            legacy.make_sysadmin_owners_address(user_id=user_id),
            addresser.sysadmin.owner.address(object_id=user_id),
        )
        self.assertEqual(
            legacy.make_sysadmin_admins_address(user_id=user_id),
            addresser.sysadmin.admin.address(object_id=user_id),
        )
        self.assertEqual(
            legacy.make_sysadmin_members_address(user_id=user_id),
            addresser.sysadmin.member.address(object_id=user_id),
        )
