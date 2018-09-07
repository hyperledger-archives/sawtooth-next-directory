# Copyright 2017 Intel Corporation
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

from base64 import b64decode
import sys
import logging
import time
import unittest
from uuid import uuid4
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from sawtooth_cli.rest_client import RestClient

import sawtooth_signing
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from rbac_addressing import addresser
from rbac_transaction_creation.protobuf import user_state_pb2
from rbac_transaction_creation.common import Key
from rbac_transaction_creation import manager_transaction_creation
from rbac_transaction_creation.user_transaction_creation import create_user
from rbac_transaction_creation import role_transaction_creation
from rbac_transaction_creation import task_transaction_creation


LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

BATCHER_PRIVATE_KEY = Secp256k1PrivateKey.new_random().as_hex()
BATCHER_KEY = Key(BATCHER_PRIVATE_KEY)
BATCHER_PUBLIC_KEY = BATCHER_KEY.public_key


def wait_until_status(url, status_code=200, tries=5):
    """Pause the program until the given url returns the required status.
    Args:
        url (str): The url to query.
        status_code (int, optional): The required status code. Defaults to 200.
        tries (int, optional): The number of attempts to request the url for
            the given status. Defaults to 5.
    Raises:
        AssertionError: If the status is not received in the given number of
            tries.
    """
    attempts = tries
    while attempts > 0:
        try:
            response = urlopen(url)
            if response.getcode() == status_code:
                return

        except HTTPError as err:
            if err.code == status_code:
                return

            LOGGER.debug('failed to read url: %s', str(err))
        except URLError as err:
            LOGGER.debug('failed to read url: %s', str(err))

        sleep_time = (tries - attempts + 1) * 2
        LOGGER.debug('Retrying in %s secs', sleep_time)
        time.sleep(sleep_time)

        attempts -= 1

    raise AssertionError(
        "{} is not available within {} attempts".format(url, tries))


def wait_for_rest_apis(endpoints, tries=5):
    """Pause the program until all the given REST API endpoints are available.
    Args:
        endpoints (list of str): A list of host:port strings.
        tries (int, optional): The number of attempts to request the url for
            availability.
    """

    for endpoint in endpoints:
        wait_until_status(
            'http://{}/blocks'.format(endpoint),
            status_code=200,
            tries=tries)


class TestBlockchain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = RBACClient('http://rest-api:8080')
        cls.key1, cls.user1 = make_key_and_name()
        cls.key2a, cls.user2a = make_key_and_name()
        cls.key3a, cls.user3a = make_key_and_name()
        cls.key2b, cls.user2b = make_key_and_name()
        cls.key_invalid, cls.user_invalid = make_key_and_name()
        cls.key3b, cls.user3b = make_key_and_name()

        cls.role_id1 = str(uuid4())
        cls.task_id1 = str(uuid4())
        cls.update_manager_proposal_id = str(uuid4())
        cls.add_role_admins_proposal_id = str(uuid4())
        cls.add_role_owners_proposal_id = str(uuid4())
        cls.add_role_members_proposal_id = str(uuid4())
        cls.add_role_tasks_proposal_id = str(uuid4())
        cls.add_task_admins_proposal_id = str(uuid4())
        cls.add_task_owners_proposal_id = str(uuid4())

        cls.remove_task_admins_proposal_id = str(uuid4())
        cls.remove_task_owners_proposal_id = str(uuid4())

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
                                / \
                               /   \
                         user2a    user2b
                         /              \
                        /                \
                      user3a              user3b

                UpdateUserManager Validation rules:

        """

        wait_for_rest_apis(['rest-api:8080'])

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                name=self.user1,
                user_name=self.user1,
                user_id=self.key1.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                name=self.user2a,
                user_name=self.user2a,
                user_id=self.key2a.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key3a,
                name=self.user2b,
                user_name=self.user2b,
                user_id=self.key2b.public_key,
                manager_id=self.key3a.public_key)[0]['status'],
            'INVALID',
            "The transaction is invalid because the public key given for "
            "the manager does not exist in state.")

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                name=self.user1,
                user_name=self.user1,
                user_id=self.key2a.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'INVALID',
            "The transaction is invalid because the User already exists.")

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                name=self.user2b,
                user_name=self.user2b,
                user_id=self.key2b.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'INVALID',
            "The signing key does not belong to the user or manager.")

        self.assertEqual(
            self.client.create_user(
                key=self.key_invalid,
                name=self.user_invalid[:4],
                user_name=self.user_invalid[:4],
                user_id=self.key_invalid.public_key,
                manager_id=None)[0]['status'],
            'INVALID',
            "The User's name must be at least 5 characters long.")

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                name=self.user3a,
                user_name=self.user3a,
                user_id=self.key3a.public_key,
                manager_id=self.key2a.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                name=self.user2b,
                user_name=self.user2b,
                user_id=self.key2b.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key3b,
                name=self.user3b,
                user_name=self.user3b,
                user_id=self.key3b.public_key,
                manager_id=self.key2b.public_key)[0]['status'],
            'COMMITTED')

        state_items = self.client.return_state()
        self.assertEqual(len(state_items), 5, "There are 5 users in state.")

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

        _, role1 = make_key_and_name()
        metadata = uuid4().hex

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role1,
                role_id=self.role_id1,
                metadata=metadata,
                admins=[self.key1.public_key, self.key2a.public_key],
                owners=[self.key2b.public_key])[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role1,
                role_id=self.role_id1,
                metadata=metadata,
                admins=[self.key2a.public_key],
                owners=[self.key2b.public_key])[0]['status'],
            "INVALID",
            "The Role Id must not already exist.")

        _, role2 = make_key_and_name()
        role_id2 = uuid4().hex

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role2,
                role_id=role_id2,
                metadata=metadata,
                admins=[self.key_invalid.public_key, self.key2a.public_key],
                owners=[self.key2b.public_key])[0]['status'],
            "INVALID",
            "All Admins listed must be Users")

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role2,
                role_id=role_id2,
                metadata=metadata,
                admins=[self.key2a.public_key],
                owners=[self.key_invalid.public_key, self.key2b.public_key])[0]['status'],
            "INVALID",
            "All Owners listed must be Users")

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
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The User must exist")

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key_invalid,
                proposal_id=uuid4().hex,
                user_id=self.key1.public_key,
                new_manager_id=self.key_invalid.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The manager must exist")

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key3b,
                proposal_id=uuid4().hex,
                user_id=self.key2a.public_key,
                new_manager_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The current manager must sign the txn.")

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key1,
                proposal_id=self.update_manager_proposal_id,
                user_id=self.key2a.public_key,
                new_manager_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_update_manager(
                key=self.key1,
                proposal_id=uuid4().hex,
                user_id=self.key2a.public_key,
                new_manager_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "There is already a proposal to make user2a have user2b "
            "as a manager.")

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
                manager_id=self.key2b.public_key
            )[0]['status'],
            "INVALID",
            "The txn signer must be the new manager listed on the proposal")

        self.assertEqual(
            self.client.confirm_update_manager(
                key=self.key2b,
                proposal_id=uuid4().hex,
                reason=uuid4().hex,
                user_id=uuid4().hex,
                manager_id=self.key2b.public_key)[0]['status'],
            "INVALID",
            "The proposal must exist")

        self.assertEqual(
            self.client.confirm_update_manager(
                key=self.key2b,
                proposal_id=self.update_manager_proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key2b.public_key)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.confirm_update_manager(
                key=self.key2b,
                proposal_id=self.update_manager_proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key2b.public_key)[0]['status'],
            "INVALID",
            "The proposal must be open")

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
                key=self.key2b,
                proposal_id=proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                new_manager_id=self.key3b.public_key,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_update_manager(
                key=self.key1,
                proposal_id=uuid4().hex,
                reason=uuid4().hex,
                user_id=self.key1.public_key,
                manager_id=self.key3b.public_key)[0]['status'],
            "INVALID",
            "The proposal does not exist")

        self.assertEqual(
            self.client.reject_update_manager(
                key=self.key3b,
                proposal_id=proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key3b.public_key)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_update_manager(
                key=self.key3b,
                proposal_id=proposal_id,
                reason=uuid4().hex,
                user_id=self.key2a.public_key,
                manager_id=self.key3b.public_key)[0]['status'],
            "INVALID",
            "The proposal is not open")

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
                    \                                \
                     user2b                          admins
                     /   \                             - user1
                    /   user2a                         - user2a
                  user3b    \
                            user3a
        """

        invalid_role_id = uuid4().hex
        invalid_user_id = uuid4().hex

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=invalid_role_id,
                user_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The role must exist")

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=invalid_user_id,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The user must exist")

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn must be signed by either the user or their manager")

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key2a,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key2a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The user must not already be an admin")

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key2a,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_add_role_admins(
                key=self.key2a,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "There must not be an open proposal for the same change.")

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
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer for ConfirmAddRoleAdmin must be an admin "
            "of the role.")

        self.assertEqual(
            self.client.confirm_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.confirm_add_role_admins(
                key=self.key1,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.confirm_add_role_admins(
                key=self.key1,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                key=self.key2b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The user is not a Role Admin.")

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_admins(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                key=self.key2b,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The role must exist.")

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key2b,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=uuid4().hex,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The user must exist")

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be the user or user's manager.")

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key2b,
                proposal_id=self.add_role_owners_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_add_role_owners(
                key=self.key2b,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "No open proposal can exist for the same state change.")

    def test_09_confirm_add_role_owners(self):
        """Tests the ConfirmAddRoleOwners validation rules.

        Notes:
            ConfirmAddRoleOwners validation rules
                - The proposal exists and is open.
                - The txn signer is a Role admin.

            At this point:
                user1                            role1
                    \                                 \
                     user2b                          admins
                     /   \                             - user1
                    /   user2a                         - user2a
                  user3b    \                          - user3a
                            user3a
        """

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key2b,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer for ConfirmAddRoleOwner must be an admin "
            "of the role.")

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key3a,
                proposal_id=self.add_role_owners_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.confirm_add_role_owners(
                key=self.key3a,
                proposal_id=self.add_role_admins_proposal_id,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer is not a Role Admin.")

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_owners(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

    def test_11_propose_add_role_members(self):
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
                    \                            /    \
                     user2b                  owners   admins
                     /   \                    - user3b - user1
                    /   user2a                         - user2a
                  user3b    \                          - user3a
                            user3a
        """

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key2b,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The role must exist.")

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key2b,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=uuid4().hex,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The user must exist")

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be the user or user's manager.")

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key1,
                proposal_id=self.add_role_members_proposal_id,
                role_id=self.role_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_add_role_members(
                key=self.key1,
                proposal_id=uuid4().hex,
                role_id=self.role_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "No open proposal can exist for the same state change.")

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
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer for ConfirmAddRoleMember must be an owner "
            "of the role.")

        self.assertEqual(
            self.client.confirm_add_role_members(
                key=self.key3b,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.confirm_add_role_members(
                key=self.key3b,
                proposal_id=self.add_role_members_proposal_id,
                role_id=self.role_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.confirm_add_role_members(
                key=self.key3b,
                proposal_id=self.add_role_members_proposal_id,
                role_id=self.role_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key2a,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer is not a Role Owner.")

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key3b,
                proposal_id=uuid4().hex,
                role_id=uuid4().hex,
                user_id=uuid4().hex,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_members(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "All admins must be users.")

        self.assertEqual(
            self.client.create_task(
                key=self.key1,
                task_id=uuid4().hex,
                task_name=uuid4().hex,
                admins=[self.key1.public_key],
                owners=[uuid4().hex],
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "All owners must be users")

        self.assertEqual(
            self.client.create_task(
                key=self.key1,
                task_id=self.task_id1,
                task_name=uuid4().hex,
                admins=[self.key1.public_key],
                owners=[self.key2a.public_key],
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.create_task(
                key=self.key1,
                task_id=self.task_id1,
                task_name=uuid4().hex,
                admins=[self.key1.public_key],
                owners=[self.key1.public_key],
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The task_id must not belong to another task.")

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
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be a Role Owner")

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=str(uuid4()),
                role_id=str(uuid4()),
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The role must exist.")

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=str(uuid4()),
                role_id=str(uuid4()),
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The task must exist.")

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=str(uuid4()),
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "No Proposal for the same Add Role Task can exist.")

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
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.confirm_add_role_tasks(
                key=self.key1,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be a Task Owner.")

        self.assertEqual(
            self.client.confirm_add_role_tasks(
                key=self.key2a,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.confirm_add_role_tasks(
                key=self.key2a,
                proposal_id=self.add_role_tasks_proposal_id,
                role_id=self.role_id1,
                task_id=self.task_id1,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_add_role_tasks(
                key=self.key3b,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key1,
                proposal_id=str(uuid4()),
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key2a,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be a Task Owner.")

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_role_tasks(
                key=self.key1,
                proposal_id=proposal_id,
                role_id=self.role_id1,
                task_id=task_id,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

    def test_18_propose_add_task_admins(self):
        """Tests the ProposeAddTaskAdmins validation rules.

        Notes:
            ProposeAddTaskAdmins validation rules.
                - The Task exists
                - The User exists
                - The txn signer is the User or the User's manager.
                - No open proposal exists for the same change.
                - The user is not already an Admin of the Task.
        """

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key2b.public_key,
                reason=str(uuid4()),
                metadata=str(uuid4()))[0]['status'],
            "INVALID",
            "The Task must exist.")

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key_invalid,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key_invalid.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The user must exist")

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key3a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be the user or user's manager")

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key2b,
                proposal_id=self.add_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_add_task_admins(
                key=self.key2b,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The must not be any open proposal for the same change.")

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
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.confirm_add_task_admins(
                key=self.key1,
                proposal_id=self.add_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.confirm_add_task_admins(
                key=self.key1,
                proposal_id=self.add_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                key=self.key2b,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.reject_add_task_admins(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_task_admins(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

    def test_21_propose_add_task_owners(self):
        """Tests the ProposeAddTaskOwners validation rules

        Notes:
            ProposeAddTaskOwners
                - The Task exists
                - The User exists
                - No open proposal exists for the same change.
                - The txn signer is the user or the Users manager.
                - The User is not already an Owner of the Task.
        """

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The Task must exist.")

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key2a,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=str(uuid4()),
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The User must exist.")

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key2a,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The User must not already be an Owner of the Task")

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key3a,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be the User or the Users manager.")

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.propose_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "There must not be an OPEN proposal for the same change.")

    def test_22_confirm_add_task_owners(self):
        """Tests the ConfirmAddTaskOwners validation rules

        Notes
            ConfirmAddTaskOwners validation rules
                - The proposal exists and is open.
                - The txn signer is a Task Admin.
        """

        self.assertEqual(
            self.client.confirm_add_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.confirm_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.confirm_add_task_owners(
                key=self.key1,
                proposal_id=self.add_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

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
                key=self.key2b,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must exist.")

        self.assertEqual(
            self.client.reject_add_task_owners(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.reject_add_task_owners(
                key=self.key1,
                proposal_id=proposal_id,
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex)[0]['status'],
            "INVALID",
            "The proposal must be open.")

    def test_24_propose_remove_task_admins(self):
        """Tests the ProposeRemoveTaskAdmins txn validation rules.

        Notes:
            ProposeRemoveTaskAdmins validation rules
                - No open proposal for the same change exists.
                - The user is an admin of the task.
                - The Task exists
                - The User exists.
                - The txn signer is the user or the user's manager.
        """

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The Task must exist.")

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=str(uuid4()),
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The User must exist.")

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key2a,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key2a.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The User must be an Admin of the Task.")

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key2b,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be the User or the User's Manager.")

        self.assertEqual(
            self.client.propose_delete_task_admins(
                key=self.key1,
                proposal_id=self.remove_task_admins_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")

    def test_25_propose_remove_task_owners(self):
        """Tests the ProposeRemoveTaskOwners txn validation rules.

        Notes:
            ProposeRemoveTaskAdmins validation rules
                - No open proposal for the same change exists.
                - The user is an Owner of the task.
                - The Task exists.
                - The User exists.
                - The txn signer is the user or the user's manager.
        """

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=str(uuid4()),
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The Task must exist.")

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key1,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=str(uuid4()),
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The User must exist.")

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key3b,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key3b.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The User must be an Owner of the Task.")

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key2b,
                proposal_id=str(uuid4()),
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "INVALID",
            "The txn signer must be the User or the User's Manager.")

        self.assertEqual(
            self.client.propose_delete_task_owners(
                key=self.key1,
                proposal_id=self.remove_task_owners_proposal_id,
                task_id=self.task_id1,
                user_id=self.key1.public_key,
                reason=uuid4().hex,
                metadata=uuid4().hex)[0]['status'],
            "COMMITTED")


class RBACClient(object):

    def __init__(self, url):
        self._client = RestClient(base_url=url)

    def return_state(self):
        items = []
        for item in self._client.list_state(subtree=addresser.NS)['data']:
            if addresser.address_is(item['address']) == addresser.AddressSpace.USER:
                user_container = user_state_pb2.UserContainer()
                user_container.ParseFromString(b64decode(item['data']))
                items.append((user_container, addresser.AddressSpace.USER))
        return items

    def create_user(self, key, name, user_name, user_id, manager_id=None):
        batch_list, signature = create_user(txn_key=key,
                                            batch_key=BATCHER_KEY,
                                            name=name,
                                            user_name=user_name,
                                            user_id=user_id,
                                            metadata=uuid4().hex,
                                            manager_id=manager_id)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def create_role(self, key, role_name, role_id, metadata, admins, owners):
        batch_list, signature = role_transaction_creation.create_role(
            txn_key=key,
            batch_key=BATCHER_KEY,
            role_name=role_name,
            role_id=role_id,
            metadata=metadata,
            admins=admins,
            owners=owners)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_update_manager(self,
                               key,
                               proposal_id,
                               user_id,
                               new_manager_id,
                               reason,
                               metadata):

        batch_list, signature = manager_transaction_creation.propose_manager(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=new_manager_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_update_manager(self,
                               key,
                               proposal_id,
                               reason,
                               user_id,
                               manager_id):
        batch_list, signature = manager_transaction_creation.confirm_manager(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            reason=reason,
            user_id=user_id,
            manager_id=manager_id)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_update_manager(self,
                              key,
                              proposal_id,
                              reason,
                              user_id,
                              manager_id):
        batch_list, signature = manager_transaction_creation.reject_manager(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            reason=reason,
            user_id=user_id,
            manager_id=manager_id)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_admins(self,
                                key,
                                proposal_id,
                                role_id,
                                user_id,
                                reason,
                                metadata):
        batch_list, signature = role_transaction_creation.propose_add_role_admins(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_admins(self,
                                key,
                                proposal_id,
                                role_id,
                                user_id,
                                reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_admins(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason)

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_admins(self,
                               key,
                               proposal_id,
                               role_id,
                               user_id,
                               reason):

        batch_list, signature = role_transaction_creation.reject_add_role_admins(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_owners(self,
                                key,
                                proposal_id,
                                role_id,
                                user_id,
                                reason,
                                metadata):
        batch_list, signature = role_transaction_creation.propose_add_role_owners(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_owners(self,
                                key,
                                proposal_id,
                                role_id,
                                user_id,
                                reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_owners(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_owners(self,
                               key,
                               proposal_id,
                               role_id,
                               user_id,
                               reason):
        batch_list, signature = role_transaction_creation.reject_add_role_owners(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_members(self,
                                 key,
                                 proposal_id,
                                 role_id,
                                 user_id,
                                 reason,
                                 metadata):
        batch_list, signature = role_transaction_creation.propose_add_role_members(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_members(self,
                                 key,
                                 proposal_id,
                                 role_id,
                                 user_id,
                                 reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_members(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_members(self,
                                key,
                                proposal_id,
                                role_id,
                                user_id,
                                reason):
        batch_list, signature = role_transaction_creation.reject_add_role_members(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_tasks(self,
                              key,
                              proposal_id,
                              role_id,
                              task_id,
                              reason,
                              metadata):
        batch_list, signature = role_transaction_creation.propose_add_role_tasks(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            task_id=task_id,
            reason=reason,
            metadata=metadata)

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_tasks(self,
                              key,
                              proposal_id,
                              role_id,
                              task_id,
                              reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_tasks(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            task_id=task_id,
            reason=reason)

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_tasks(self,
                              key,
                              proposal_id,
                              role_id,
                              task_id,
                              reason):
        batch_list, signature = role_transaction_creation.reject_add_role_tasks(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            role_id=role_id,
            task_id=task_id,
            reason=reason)

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def create_task(self,
                    key,
                    task_id,
                    task_name,
                    admins,
                    owners,
                    metadata):

        batch_list, signature = task_transaction_creation.create_task(
            txn_key=key,
            batch_key=BATCHER_KEY,
            task_id=task_id,
            task_name=task_name,
            admins=admins,
            owners=owners,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_task_admins(self,
                                key,
                                proposal_id,
                                task_id,
                                user_id,
                                reason,
                                metadata):
        batch_list, signature = task_transaction_creation.propose_add_task_admins(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_task_admins(self,
                                key,
                                proposal_id,
                                task_id,
                                user_id,
                                reason):
        batch_list, signature = task_transaction_creation.confirm_add_task_admins(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_task_admins(self,
                               key,
                               proposal_id,
                               task_id,
                               user_id,
                               reason):
        batch_list, signature = task_transaction_creation.reject_add_task_admins(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_task_owners(self,
                                key,
                                proposal_id,
                                task_id,
                                user_id,
                                reason,
                                metadata):
        batch_list, signature = task_transaction_creation.propose_add_task_owner(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_task_owners(self,
                                key,
                                proposal_id,
                                task_id,
                                user_id,
                                reason):
        batch_list, signature = task_transaction_creation.confirm_add_task_owners(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_task_owners(self,
                               key,
                               proposal_id,
                               task_id,
                               user_id,
                               reason):
        batch_list, signature = task_transaction_creation.reject_add_task_owners(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_delete_task_admins(self,
                                   key,
                                   proposal_id,
                                   task_id,
                                   user_id,
                                   reason,
                                   metadata):
        batch_list, signature = task_transaction_creation.propose_remove_task_admins(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_delete_task_owners(self,
                                   key,
                                   proposal_id,
                                   task_id,
                                   user_id,
                                   reason,
                                   metadata):

        batch_list, signature = task_transaction_creation.propose_remove_task_owners(
            txn_key=key,
            batch_key=BATCHER_KEY,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)


def make_key_and_name():
    context = sawtooth_signing.create_context('secp256k1')
    private_key = context.new_random_private_key()
    pubkey = context.get_public_key(private_key)

    key = Key(public_key=pubkey.as_hex(), private_key=private_key.as_hex())
    return key, uuid4().hex
