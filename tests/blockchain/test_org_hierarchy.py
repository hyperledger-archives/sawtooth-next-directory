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
import unittest
from uuid import uuid4
import pytest
from tests.blockchain.rbac_client import RbacClient
from tests.blockchain.integration_test_helper import IntegrationTestHelper

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@pytest.mark.blockchain
class TestOrgHierarchy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_helper = IntegrationTestHelper()
        cls.client = RbacClient(None, IntegrationTestHelper.get_batcher_key())
        cls.key1, cls.user1 = cls.test_helper.make_key_and_name()
        cls.key2a, cls.user2a = cls.test_helper.make_key_and_name()
        cls.key3a, cls.user3a = cls.test_helper.make_key_and_name()
        cls.key_manager, cls.user2b = cls.test_helper.make_key_and_name()
        cls.key_invalid, cls.user_invalid = cls.test_helper.make_key_and_name()
        cls.key3b, cls.user3b = cls.test_helper.make_key_and_name()

        cls.role_id1 = str(uuid4())
        cls.task_id1 = str(uuid4())
        cls.task_id2 = str(uuid4())
        cls.update_manager_proposal_id = str(uuid4())
        cls.add_role_admins_proposal_id = str(uuid4())
        cls.add_role_owners_proposal_id = str(uuid4())
        cls.add_role_members_proposal_id = str(uuid4())
        cls.add_role_tasks_proposal_id = str(uuid4())
        cls.add_task_admins_proposal_id = str(uuid4())
        cls.add_task_owners_proposal_id = str(uuid4())

        cls.remove_task_admins_proposal_id = str(uuid4())
        cls.remove_task_owners_proposal_id = str(uuid4())

        cls.test_helper.wait_for_containers()

    def test_00_create_users(self):
        """Tests that the validation rules within the transaction processor
        are applied correctly.

        Notes:
            1. User
                CreateUser Validation rules:
                - Public key given for manager must be in state as a User.
                - User must not already exist.
                - The signing public key must belong to the user or manager.
                - The User must have a name longer than 4 characters.
                Create 5 Users,
                                user1
                                / |
                               /   |
                         user2a    user2b
                         /              |
                        /                |
                      user3a              user3b

                UpdateUserManager Validation rules:

        """

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                name=self.user1,
                username=self.user1,
                user_id=self.key1.public_key,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                name=self.user2a,
                username=self.user2a,
                user_id=self.key2a.public_key,
                manager_id=self.key1.public_key,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key3a,
                name=self.user2b,
                username=self.user2b,
                user_id=self.key_manager.public_key,
                manager_id=self.key3a.public_key,
            )[0]["status"],
            "INVALID",
            "The transaction is invalid because the public key given for "
            "the manager does not exist in state.",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                name=self.user1,
                username=self.user1,
                user_id=self.key2a.public_key,
                manager_id=self.key1.public_key,
            )[0]["status"],
            "INVALID",
            "The transaction is invalid because the User already exists.",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                name=self.user2b,
                username=self.user2b,
                user_id=self.key_manager.public_key,
                manager_id=self.key1.public_key,
            )[0]["status"],
            "INVALID",
            "The signing key does not belong to the user or manager.",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key_invalid,
                name=self.user_invalid[:4],
                username=self.user_invalid[:4],
                user_id=self.key_invalid.public_key,
                manager_id=None,
            )[0]["status"],
            "INVALID",
            "The User's name must be at least 5 characters long.",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                name=self.user3a,
                username=self.user3a,
                user_id=self.key3a.public_key,
                manager_id=self.key2a.public_key,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                name=self.user2b,
                username=self.user2b,
                user_id=self.key_manager.public_key,
                manager_id=self.key1.public_key,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.create_user(
                key=self.key3b,
                name=self.user3b,
                username=self.user3b,
                user_id=self.key3b.public_key,
                manager_id=self.key_manager.public_key,
            )[0]["status"],
            "COMMITTED",
        )

    def test_01_create_roles(self):
        """Tests that the CreateRole validation rules are correct.

        Notes:
            Role:
                CreateRole Validation rules
                    - There isn't already a Role with the same id
                    - The Admins listed are Users.

                Role1
                    - Admins
                        - user1
                        - user2a
                    - Owners
                        - user2b
                    - Members
                        - user3a
                        - user3b

        """

        _, role1 = self.test_helper.make_key_and_name()
        metadata = uuid4().hex

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role1,
                role_id=self.role_id1,
                metadata=metadata,
                admins=[self.key1.public_key, self.key2a.public_key],
                owners=[self.key_manager.public_key],
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role1,
                role_id=self.role_id1,
                metadata=metadata,
                admins=[self.key2a.public_key],
                owners=[self.key_manager.public_key],
            )[0]["status"],
            "INVALID",
            "The Role Id must not already exist.",
        )

        _, role2 = self.test_helper.make_key_and_name()
        role_id2 = uuid4().hex

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role2,
                role_id=role_id2,
                metadata=metadata,
                admins=[self.key_invalid.public_key, self.key2a.public_key],
                owners=[self.key_manager.public_key],
            )[0]["status"],
            "INVALID",
            "All Admins listed must be Users",
        )

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role2,
                role_id=role_id2,
                metadata=metadata,
                admins=[self.key2a.public_key],
                owners=[self.key_invalid.public_key, self.key_manager.public_key],
            )[0]["status"],
            "INVALID",
            "All Owners listed must be Users",
        )

    def test_02_propose_update_user_manager(self):
        """Tests that the ProposeUpdateUserManager validation rules are
        correct.

        Notes:
            ProposeUpdateUserManager Validation rules
                - The user exists.
                - The manager exists as a user.
                - The transaction header signer's public key is the User's
                  current manager.
                - No open proposal for the same change exists.
        """

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key1,
                proposal_id=uuid4().hex,
                user_id=self.key_invalid.public_key,
                new_manager_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must exist",
        )

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key_invalid,
                proposal_id=uuid4().hex,
                user_id=self.key1.public_key,
                new_manager_id=self.key_invalid.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The manager must exist",
        )

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key3b,
                proposal_id=uuid4().hex,
                user_id=self.key2a.public_key,
                new_manager_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The current manager must sign the txn.",
        )

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key1,
                proposal_id=self.update_manager_proposal_id,
                user_id=self.key2a.public_key,
                new_manager_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key1,
                proposal_id=uuid4().hex,
                user_id=self.key2a.public_key,
                new_manager_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "There is already a proposal to make user2a have user2b " "as a manager.",
        )

    def test_03_confirm_update_manager_proposal(self):
        """Tests the ConfirmUpdateUserManager validation rules.

        Notes:
            ConfirmUpdateUserManager validation rules
                - The txn signer is the new manager
                - The Proposal exists and is OPEN.
        """

        self.assertEqual(
            self.client.confirm_update_manager(
                key=self.key1,
                proposal_id=self.update_manager_proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key_manager.public_key,
            )[0]["status"],
            "INVALID",
            "The txn signer must be the new manager listed on the proposal",
        )

        self.assertEqual(
            self.client.confirm_update_manager(
                key=self.key_manager,
                proposal_id=uuid4().hex,
                reason=uuid4().hex,
                user_id=uuid4().hex,
                manager_id=self.key_manager.public_key,
            )[0]["status"],
            "INVALID",
            "The proposal must exist",
        )

        self.assertEqual(
            self.client.confirm_update_manager(
                key=self.key_manager,
                proposal_id=self.update_manager_proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key_manager.public_key,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.confirm_update_manager(
                key=self.key_manager,
                proposal_id=self.update_manager_proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key_manager.public_key,
            )[0]["status"],
            "INVALID",
            "The proposal must be open",
        )

    def test_04_reject_update_manager_proposal(self):
        """Tests the RejectUpdateUserManager validation rules.

        Notes:
            RejectUpdateUserManager validation rules
                - The proposal is open and exists.
                - The manager's id is the header signer pubkey.

        """

        proposal_id = uuid4().hex

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key_manager,
                proposal_id=proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                new_manager_id=self.key3b.public_key,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_update_manager(
                key=self.key1,
                proposal_id=uuid4().hex,
                reason=uuid4().hex,
                user_id=self.key1.public_key,
                manager_id=self.key3b.public_key,
            )[0]["status"],
            "INVALID",
            "The proposal does not exist",
        )

        self.assertEqual(
            self.client.reject_update_manager(
                key=self.key3b,
                proposal_id=proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key3b.public_key,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_update_manager(
                key=self.key3b,
                proposal_id=proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key3b.public_key,
            )[0]["status"],
            "INVALID",
            "The proposal is not open",
        )

    def test_05_propose_add_role_admins(self):
        """Tests the ProposeAddRoleAdmins validation rules.

        Notes:
            ProposeAddRoleAdmins validation rules
                - No proposal exists for the same change.
                - The user is not already an admin.
                - The txn is signed by either the User or their manager.
                - The User exists.
                - The Role exists.

            At this point:
                user1                            role1
                    |                                |
                     user2b                          admins
                     /   |                             - user1
                    /   user2a                         - user2a
                  user3b    |
                            user3a
        """

        invalid_role_id = uuid4().hex
        invalid_user_id = uuid4().hex

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=invalid_role_id,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The role must exist",
        )

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=invalid_user_id,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The user must exist",
        )

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn must be signed by either the user or their manager",
        )

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key2a,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key2a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The user must not already be an admin",
        )

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key2a,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key2a,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "There must not be an open proposal for the same change.",
        )

    def test_06_confirm_add_role_admins(self):
        """Tests the ConfirmAddRoleAdmins validation rules.

        Notes:
            ConfirmAddRoleAdmins validation rules
                - The txn signer is a Role Admin for the role.
                - The proposal exists and is open.
        """

        self.assertEqual(
            self.client.confirm_add_role_admins(
                key=self.key3b,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer for ConfirmAddRoleAdmin must be an admin " "of the role.",
        )

        self.assertEqual(
            self.client.confirm_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.confirm_add_role_admins(
                key=self.key1,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.confirm_add_role_admins(
                key=self.key1,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_07_reject_add_role_admins(self):
        """Tests the RejectAddRoleAdmins validation rules.

        Notes:
            RejectAddRoleAdmins validation rules
                - The txn signer is a role admin.
                - The proposal exists and is open.
        """

        proposal_id = uuid4().hex

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key_manager,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The user is not a Role Admin.",
        )

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_08_propose_add_role_owners(self):
        """Tests the ProposeAddRoleOwners validation rules.

        Notes:
            ProposeAddRoleOwners validation rules
                - The Role exists.
                - The User exists.
                - The txn signer is either the User or the User's manager.
                - No open proposal exists for the same change.
                - The User is not already an Owner of the Role.
        """

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key_manager,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The role must exist.",
        )

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key_manager,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=uuid4().hex,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The user must exist",
        )

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be the user or user's manager.",
        )

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key_manager,
                proposal_id=self.add_role_owners_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key_manager,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "No open proposal can exist for the same state change.",
        )

    def test_09_confirm_add_role_owners(self):
        # pylint: disable=W1401
        """Tests the ConfirmAddRoleOwners validation rules.

        Notes:
            ConfirmAddRoleOwners validation rules
                - The proposal exists and is open.
                - The txn signer is a Role admin.

            At this point:
                user1                            role1
                    |                                 |
                     user2b                          admins
                     /   |                             - user1
                    /   user2a                         - user2a
                  user3b    |                          - user3a
                            user3a
        """

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key_manager,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer for ConfirmAddRoleOwner must be an admin " "of the role.",
        )

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key3a,
                proposal_id=self.add_role_owners_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key3a,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_10_reject_add_role_owners(self):
        """Tests the RejectAddRoleOwners validation rules.

        Notes:
            RejectAddRoleOwners validation rules
                - The txn signer is an admin of the Role
                - The proposal exists and is open.
        """

        proposal_id = uuid4().hex

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer is not a Role Admin.",
        )

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_11_propose_add_role_members(self):
        # pylint: disable=W1401
        """Tests the ProposeAddRoleMembers validation rules.

        Notes:
            ProposeAddRoleMembers validation rules
                - The Role exists.
                - The User exists.
                - The txn signer is either the User or the User's manager.
                - No open proposal exists for the same change.
                - The User is not already a Member of the Role.

            At this point:
                user1                            role1
                    |                            /    |
                     user2b                  owners   admins
                     /   |                    - user3b - user1
                    /   user2a                         - user2a
                  user3b    |                          - user3a
                            user3a
        """

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key_manager,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The role must exist.",
        )

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key_manager,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=uuid4().hex,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The user must exist",
        )

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be the user or user's manager.",
        )

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key1,
                proposal_id=self.add_role_members_proposal_id,
                role_id=self.role_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "No open proposal can exist for the same state change.",
        )

    def test_12_confirm_add_role_members(self):
        """Tests the ConfirmAddRoleMembers validation rules.

        Notes:
            ConfirmAddRoleMembers validation rules
                - The proposal exists and is open.
                - The txn signer is a Role owner.
        """

        self.assertEqual(
            self.client.confirm_add_role_members(
                key=self.key1,
                proposal_id=self.add_role_members_proposal_id,
                role_id=self.role_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer for ConfirmAddRoleMember must be an owner " "of the role.",
        )

        self.assertEqual(
            self.client.confirm_add_role_members(
                key=self.key3b,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.confirm_add_role_members(
                key=self.key3b,
                proposal_id=self.add_role_members_proposal_id,
                role_id=self.role_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.confirm_add_role_members(
                key=self.key3b,
                proposal_id=self.add_role_members_proposal_id,
                role_id=self.role_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_13_reject_add_role_members(self):
        """Tests the RejectAddRoleMembers validation rules.

        Notes:
            RejectAddRoleMembers validation rules
                - The txn signer is an owner of the Role
                - The proposal exists and is open.
        """

        proposal_id = uuid4().hex

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key2a,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer is not a Role Owner.",
        )

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key3b,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_14_create_task(self):
        """Tests the CreateTask validation rules.

        Notes:
            CreateTask validation rules
                - The admins listed are users.
                - The task_id is not used already.

        """

        self.assertEqual(
            self.client.create_task(
                key=self.key1,
                task_id=uuid4().hex,
                task_name=uuid4().hex,
                admins=[uuid4().hex],
                owners=[self.key1.public_key],
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "All admins must be users.",
        )

        self.assertEqual(
            self.client.create_task(
                key=self.key1,
                task_id=uuid4().hex,
                task_name=uuid4().hex,
                admins=[self.key1.public_key],
                owners=[uuid4().hex],
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "All owners must be users",
        )

        self.assertEqual(
            self.client.create_task(
                key=self.key1,
                task_id=self.task_id1,
                task_name=uuid4().hex,
                admins=[self.key1.public_key],
                owners=[self.key2a.public_key],
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.create_task(
                key=self.key1,
                task_id=self.task_id1,
                task_name=uuid4().hex,
                admins=[self.key1.public_key],
                owners=[self.key1.public_key],
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The task_id must not belong to another task.",
        )

    def test_15_propose_add_role_tasks(self):
        """Tests the ProposeAddRoleTasks validation rules.

        Notes:
            ProposeAddRoleTask validation rules
                - The txn is signed by a role owner.
                - The Role exists.
                - THe Task exists.
                - The Task isn't already part of the Role.
                - No open proposal exists for the same change.

        """

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key1,
                proposal_id=str(uuid4()),
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be a Role Owner",
        )

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=str(uuid4()),
                role_id=str(uuid4()),
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The role must exist.",
        )

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=str(uuid4()),
                role_id=str(uuid4()),
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The task must exist.",
        )

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=str(uuid4()),
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "No Proposal for the same Add Role Task can exist.",
        )

    def test_16_confirm_add_role_tasks(self):
        """Tests the ConfirmAddRoleTasks validation rules.

        Notes:
            ConfirmAddRoleTasks validation rules
                - The Proposal exists and is open.
                - The txn signer is an Owner of the Task

        """

        self.assertEqual(
            self.client.confirm_add_role_tasks(
                key=self.key2a,
                proposal_id=str(uuid4()),
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.confirm_add_role_tasks(
                key=self.key1,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be a Task Owner.",
        )

        self.assertEqual(
            self.client.confirm_add_role_tasks(
                key=self.key2a,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.confirm_add_role_tasks(
                key=self.key2a,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_17_reject_add_role_tasks(self):
        """Tests the RejectAddRoleTasks validation rules.

        Notes:
            RejectAddRoleTasks validation rules
                - The Proposal exists and is open.
                - The txn signer is an Owner of the Task

        """

        proposal_id = str(uuid4())
        task_id = str(uuid4())

        self.assertEqual(
            self.client.create_task(
                self.key1,
                task_id=task_id,
                task_name=uuid4().hex,
                admins=[self.key1.public_key],
                owners=[self.key1.public_key],
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key1,
                proposal_id=str(uuid4()),
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key2a,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be a Task Owner.",
        )

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_18_propose_add_task_admins(self):
        """Tests the ProposeAddTaskAdmins validation rules.

        Notes:
            ProposeAddTaskAdmins validation rules.
                - The Task exists
                - The User exists
                - The txn signer is the User, the User's manager, or the Task Admin/Owner.
                - No open proposal exists for the same change.
                - The User is not already an Admin of the Task.
        """

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key_manager.public_key,
                reason=str(uuid4()),
                metadata=str(uuid4()),
            )[0]["status"],
            "INVALID",
            "The Task must exist.",
        )

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key_invalid,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key_invalid.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must exist",
        )

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id2,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be the User,  User's manager, or the Task Admin/Owner.",
        )

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key_manager,
                proposal_id=self.add_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must not already be an Admin of the Task",
        )

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key_manager,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "There must not be any OPEN proposal for the same change.",
        )

    def test_19_confirm_add_task_admins(self):
        """Tests the ConfirmAddTaskAdmins validation rules

        Notes
            ConfirmAddTaskAdmins validation rules
                - The proposal exists and is open.
                - The txn signer is a Task Admin.
        """

        self.assertEqual(
            self.client.confirm_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.confirm_add_task_admins(
                key=self.key1,
                proposal_id=self.add_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.confirm_add_task_admins(
                key=self.key1,
                proposal_id=self.add_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_20_reject_add_task_admins(self):
        """Tests the RejectAddTaskAdmins validation rules

        Notes
            RejectAddTaskAdmins validation rules
                - The proposal exists and is open.
                - The txn signer is a Task Admin.
        """

        proposal_id = str(uuid4())

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key_manager,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.reject_add_task_admins(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_task_admins(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_21_propose_add_task_owners(self):
        """Tests the ProposeAddTaskOwners validation rules

        Notes:
            ProposeAddTaskOwners
                - The Task exists
                - The User exists
                - The txn signer is the User, the User's manager, or the Task Admin/Owner.
                - No open proposal exists for the same change.
                - The User is not already an Owner of the Task.
       """

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The Task must exist.",
        )

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key2a,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=str(uuid4()),
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must exist.",
        )

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key3a,
                proposal_id=str(uuid4()),
                task_id=self.task_id2,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be the User,  User's manager, or the Task Admin/Owner.",
        )

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key2a,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must not already be an Owner of the Task",
        )

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "There must not be an OPEN proposal for the same change.",
        )

    def test_22_confirm_add_task_owners(self):
        """Tests the ConfirmAddTaskOwners validation rules

        Notes
            ConfirmAddTaskOwners validation rules
                - The proposal exists and is open.
                - The txn signer is a Task Owner.
        """

        self.assertEqual(
            self.client.confirm_add_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.confirm_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.confirm_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_23_reject_add_task_owners(self):
        """Tests the RejectAddTaskOwners validation rules

        Notes:
            RejectAddTaskOwners validation rules
                - The proposal exists and is open
                - The txn signer is a Task admin
        """

        proposal_id = str(uuid4())

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key_manager,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key_manager.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must exist.",
        )

        self.assertEqual(
            self.client.reject_add_task_owners(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

        self.assertEqual(
            self.client.reject_add_task_owners(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The proposal must be open.",
        )

    def test_24_propose_remove_task_admins(self):
        """Tests the ProposeRemoveTaskAdmins txn validation rules.

        Notes:
            ProposeRemoveTaskAdmins validation rules
                - No open proposal for the same change exists.
                - The user is an admin of the task.
                - The Task exists
                - The User exists.
                - The txn signer is the User, the User's manager, or the Task Admin/Owner.
        """

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The Task must exist.",
        )

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=str(uuid4()),
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must exist.",
        )

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key2a,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must be an Admin of the Task.",
        )

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key_manager,
                proposal_id=str(uuid4()),
                task_id=self.task_id2,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be the User, User's manager, or the Task Admin/Owner.",
        )

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key1,
                proposal_id=self.remove_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )

    def test_25_propose_remove_task_owners(self):
        """Tests the ProposeRemoveTaskOwners txn validation rules.

        Notes:
            ProposeRemoveTaskAdmins validation rules
                - No open proposal for the same change exists.
                - The user is an Owner of the task.
                - The Task exists.
                - The User exists.
                - The txn signer is the User, the User's manager, or the Task Admin/Owner.
        """

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The Task must exist.",
        )

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=str(uuid4()),
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must exist.",
        )

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key3b,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The User must be an Owner of the Task.",
        )

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key_manager,
                proposal_id=str(uuid4()),
                task_id=self.task_id2,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "INVALID",
            "The txn signer must be the User, User's manager, or the Task Admin/Owner.",
        )

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key1,
                proposal_id=self.remove_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex,
            )[0]["status"],
            "COMMITTED",
        )
