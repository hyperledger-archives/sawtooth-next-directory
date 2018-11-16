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
"""Test Legacy Addresser"""
# pylint: disable=invalid-name

import logging
import pytest

from rbac.common.crypto.keys import Key
from rbac.legacy import addresser as legacy
from rbac.common import addresser

from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.skip("tests version 1.0 address schema compatibility")
@pytest.mark.addressing
@pytest.mark.library
class TestAddressLegacyCompatibility(TestAssertions):
    """Test Legacy Addresser"""

    def test_legacy_attributes(self):
        """Test equality of the legacy addresser and new addresser classes"""
        self.assertEqual(addresser.family.name, legacy.FAMILY_NAME)
        self.assertEqual(addresser.family.version, legacy.FAMILY_VERSION)

    def test_legacy_address_space(self):
        """Test equality of the legacy addresser and new addresser classes"""
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
        """Test equality of the legacy addresser and new addresser classes"""
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

    def test_proposal_address_static(self):
        """Test addreser makes expected address"""
        object_id = "cb048d507eec42a5845e20eed982d5d2"
        target_id = "f1e916b663164211a9ac34516324681a"
        expected_address = "9f4448e3b874e90b2bcf58e65e0727\
91ea499543ee52fc9d0449fc1e41f77d4d4f926e"
        proposal_address = addresser.proposal.address(
            object_id=object_id, target_id=target_id
        )
        self.assertIsAddress(proposal_address)
        self.assertEqual(proposal_address, expected_address)
        self.assertEqual(
            addresser.address_is(proposal_address), addresser.AddressSpace.PROPOSALS
        )

    def test_role_admin_address_static(self):
        """Test addreser makes expected address"""
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f444809326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d28f7"
        rel_address = addresser.role.admin.address(object_id=role_id, target_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_ADMINS
        )

    def test_role_member_address_static(self):
        """Test addreser makes expected address"""
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f444809326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2833"
        rel_address = addresser.role.member.address(
            object_id=role_id, target_id=user_id
        )
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_MEMBERS
        )

    def test_role_owner_address_static(self):
        """Test addreser makes expected address"""
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f444809326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2893"
        rel_address = addresser.role.owner.address(object_id=role_id, target_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_OWNERS
        )

    def test_role_task_address_static(self):
        """Test addreser makes expected address"""
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        task_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f444809326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d28c5"
        rel_address = addresser.role.task.address(object_id=role_id, target_id=task_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.ROLES_TASKS
        )

    def test_role_address_static(self):
        """Test addreser makes expected address"""
        role_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        expected_address = "9f444809326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2800"
        role_address = addresser.role.address(object_id=role_id)
        self.assertIsAddress(role_address)
        self.assertEqual(role_address, expected_address)
        self.assertEqual(
            addresser.address_is(role_address), addresser.AddressSpace.ROLES_ATTRIBUTES
        )

    def test_sysadmin_admin_address_static(self):
        """Test addreser makes expected address"""
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f4448000000000000000000000000\
00000000000000000000000000000000000000f7"
        rel_address = addresser.sysadmin.admin.address(object_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.SYSADMIN_ADMINS
        )

    def test_sysadmin_member_address_static(self):
        """Test addreser makes expected address"""
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f4448000000000000000000000000\
0000000000000000000000000000000000000083"
        rel_address = addresser.sysadmin.member.address(object_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.SYSADMIN_MEMBERS
        )

    def test_sysadmin_owner_address_static(self):
        """Test addreser makes expected address"""
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f4448000000000000000000000000\
00000000000000000000000000000000000000de"
        rel_address = addresser.sysadmin.owner.address(object_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.SYSADMIN_OWNERS
        )

    def test_sysadmin_address_static(self):
        """Test addreser makes expected address"""
        expected_address = "9f4448000000000000000000000000\
0000000000000000000000000000000000000000"
        sysadmin_address = addresser.sysadmin.address()
        self.assertIsAddress(sysadmin_address)
        self.assertEqual(sysadmin_address, expected_address)
        self.assertEqual(
            addresser.address_is(sysadmin_address),
            addresser.AddressSpace.SYSADMIN_ATTRIBUTES,
        )

    def test_task_admin_address_static(self):
        """Test addreser makes expected address"""
        task_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f44481e326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2848"
        rel_address = addresser.task.admin.address(object_id=task_id, target_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.TASKS_ADMINS
        )

    def test_task_owner_address_static(self):
        """Test addreser makes expected address"""
        task_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f44481e326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2808"
        rel_address = addresser.task.owner.address(object_id=task_id, target_id=user_id)
        self.assertIsAddress(rel_address)
        self.assertEqual(rel_address, expected_address)
        self.assertEqual(
            addresser.address_is(rel_address), addresser.AddressSpace.TASKS_OWNERS
        )

    def test_task_address_static(self):
        """Test addreser makes expected address"""
        task_id = "99968acb8f1a48b3a4bc21e2cd252e67"
        expected_address = "9f44481e326a1713a905b26359fc8d\
a2817c1a5f67de6f464701f0c10042da345d2800"
        task_address = addresser.task.address(object_id=task_id)
        self.assertIsAddress(task_address)
        self.assertEqual(task_address, expected_address)
        self.assertEqual(
            addresser.address_is(task_address), addresser.AddressSpace.TASKS_ATTRIBUTES
        )

    def test_user_address_static(self):
        """Test addreser makes expected address"""
        user_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f444847e7570f3f6f7d2c1635f6de\
eabc1f4d78d9d42b64b70e1819f244138c1e38d6"
        user_address = addresser.user.address(object_id=user_id)
        self.assertIsAddress(user_address)
        self.assertEqual(user_address, expected_address)
        self.assertEqual(
            addresser.address_is(user_address), addresser.AddressSpace.USER
        )
