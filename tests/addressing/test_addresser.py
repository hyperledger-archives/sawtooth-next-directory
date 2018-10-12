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
import logging
import unittest
from uuid import uuid4

from rbac.addressing import addresser
from rbac.addressing.addresser import AddressSpace

LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.addressing
class TestAddresser(unittest.TestCase):
    def test_sysadmin_addresses(self):
        """Tests the SysAdmin address creation functions as well as the
        address_is function.

        Notes:
            1. Create a SysAdmin address.
                - SysAdmin Attributes
                - SysAdmin Members
                - SysAdmin Owners
                - SysAdmin Admins
            2. Assert that the address_is function returns the correct
               address type.
        """

        sysadmin_address = addresser.make_sysadmin_attr_address()

        self.assertEqual(
            len(sysadmin_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(sysadmin_address),
            AddressSpace.SYSADMIN_ATTRIBUTES,
            "The SysAdmin Attributes address created must be found "
            "to be a SysAdmin Attributes address.",
        )

        sysadmin_members_address = addresser.make_sysadmin_members_address(
            user_id=uuid4().hex
        )

        self.assertEqual(
            len(sysadmin_members_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(sysadmin_members_address),
            AddressSpace.SYSADMIN_MEMBERS,
            "The SysAdmin Members address created must be found to "
            "be a SysAdmin Members address.",
        )

        sysadmin_owners_address = addresser.make_sysadmin_owners_address(
            user_id=uuid4().hex
        )

        self.assertEqual(
            len(sysadmin_owners_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(sysadmin_owners_address),
            AddressSpace.SYSADMIN_OWNERS,
            "The SysAdmin Owners address created must be found to "
            "be a SysAdmin Owners address.",
        )

        sysadmin_admins_address = addresser.make_sysadmin_admins_address(
            user_id=uuid4().hex
        )

        self.assertEqual(
            len(sysadmin_admins_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(sysadmin_admins_address),
            AddressSpace.SYSADMIN_ADMINS,
            "The SysAdmin Admins address created must be found to "
            "be a SysAdmin Admins address.",
        )

    def test_role_addresses(self):
        """Tests the Role address creation functions as well as the
        address_is function.

        Notes:
            1. Create an address of a particular type:
                - Role Attributes
                - Role Members
                - Role Owners
                - Role Admins
                - Role Tasks
            2. Assert that address_is returns the correct address type.

        """

        role_address = addresser.make_role_attributes_address(role_id=uuid4().hex)

        self.assertEqual(len(role_address), 70, "The address is a well-formed address.")

        self.assertEqual(
            addresser.address_is(role_address),
            AddressSpace.ROLES_ATTRIBUTES,
            "The Role Attributes address created must "
            "be found to be a Role Attributes address.",
        )

        role_members_address = addresser.make_role_members_address(
            role_id=uuid4().hex, user_id=uuid4().hex
        )

        self.assertEqual(
            len(role_members_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(role_members_address),
            AddressSpace.ROLES_MEMBERS,
            "The Role Members address created must be "
            "found to be a Role Members address.",
        )

        role_owners_address = addresser.make_role_owners_address(
            role_id=uuid4().hex, user_id=uuid4().hex
        )

        self.assertEqual(
            len(role_owners_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(role_owners_address),
            AddressSpace.ROLES_OWNERS,
            "The Role Owners address created must be found to be "
            "a Role Members address.",
        )

        role_admins_address = addresser.make_role_admins_address(
            role_id=uuid4().hex, user_id=uuid4().hex
        )

        self.assertEqual(
            len(role_admins_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(role_admins_address),
            AddressSpace.ROLES_ADMINS,
            "The Role Admins address created must be "
            "found to be a Role Admins address.",
        )

        role_tasks_address = addresser.make_role_tasks_address(
            role_id=uuid4().hex, task_id=uuid4().hex
        )

        self.assertEqual(
            len(role_tasks_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(role_tasks_address),
            AddressSpace.ROLES_TASKS,
            "The Role Tasks address created must be "
            "found to be a Role Tasks address.",
        )

    def test_task_addresses(self):
        """Tests the Task address creation functions as well as the
        address_is function.

        Notes:
            1. Create an address of a particular type:
                - Task Attributes
                - Task Owners
                - Task Admins
            2. Assert that address_is returns the correct address type.

        """

        task_address = addresser.make_task_attributes_address(uuid4().hex)

        self.assertEqual(len(task_address), 70, "The address is a well-formed address.")

        self.assertEqual(
            addresser.address_is(task_address),
            AddressSpace.TASKS_ATTRIBUTES,
            "The Task Attributes address created must be "
            "found to be a Task Attributes address.",
        )

        task_owners_address = addresser.make_task_owners_address(
            task_id=uuid4().hex, user_id=uuid4().hex
        )

        self.assertEqual(
            len(task_owners_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(task_owners_address),
            AddressSpace.TASKS_OWNERS,
            "The Task Owners address created must be "
            "found to be a Task Owners address.",
        )

        task_admins_address = addresser.make_task_admins_address(
            task_id=uuid4().hex, user_id=uuid4().hex
        )

        self.assertEqual(
            len(task_admins_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(task_admins_address),
            AddressSpace.TASKS_ADMINS,
            "The Task Admins address created must be "
            "found to be a Task Admins address.",
        )

    def test_proposal_addresses(self):
        """Tests the Proposal address creation function as well as the
        address_is function.

        Notes:
            1. Create a Proposal address.
            2. Assert that address_is returns the correct address type.

        """

        proposal_address = addresser.make_proposal_address(
            object_id=uuid4().hex, related_id=uuid4().hex
        )

        self.assertEqual(
            len(proposal_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(proposal_address),
            AddressSpace.PROPOSALS,
            "The Proposals address created must be found " "to be a Proposals address.",
        )

    def test_users_address(self):
        """Tests the Users address creation function as well as the
        address_is function.

        Notes:
            1. Create a Users address.
            2. Assert that address_is returns the correct address type.

        """

        users_address = addresser.make_user_address(user_id=uuid4().hex)

        self.assertEqual(
            len(users_address), 70, "The address is a well-formed address."
        )

        self.assertEqual(
            addresser.address_is(users_address),
            AddressSpace.USER,
            "The User address created must be found " "to be a User address.",
        )
