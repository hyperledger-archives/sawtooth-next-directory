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
import logging
import time
import unittest
from uuid import uuid4
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from sawtooth_cli.rest_client import RestClient

import sawtooth_signing as signing

from rbac_addressing import addresser
from rbac_transaction_creation.protobuf import user_state_pb2
from rbac_transaction_creation.common import Key
from rbac_transaction_creation import manager_transaction_creation
from rbac_transaction_creation.user_transaction_creation import create_user
from rbac_transaction_creation.role_transaction_creation import create_role


LOGGER = logging.getLogger(__name__)


BATCHER_PRIVATE_KEY = signing.generate_privkey()
BATCHER_PUBLIC_KEY = signing.generate_pubkey(BATCHER_PRIVATE_KEY)

BATCHER_KEY = Key(public_key=BATCHER_PUBLIC_KEY,
                  private_key=BATCHER_PRIVATE_KEY)


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

        cls.role_id1 = uuid4().hex
        cls.update_manager_proposal_id = uuid4().hex

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
                user_name=self.user1,
                user_id=self.key1.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                user_name=self.user2a,
                user_id=self.key2a.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key3a,
                user_name=self.user2b,
                user_id=self.key2b.public_key,
                manager_id=self.key3a.public_key)[0]['status'],
            'INVALID',
            "The transaction is invalid because the public key given for "
            "the manager does not exist in state.")

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                user_name=self.user1,
                user_id=self.key2a.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'INVALID',
            "The transaction is invalid because the User already exists.")

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                user_name=self.user2b,
                user_id=self.key2b.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'INVALID',
            "The signing key does not belong to the user or manager.")

        self.assertEqual(
            self.client.create_user(
                key=self.key_invalid,
                user_name=self.user_invalid[:4],
                user_id=self.key_invalid.public_key,
                manager_id=None)[0]['status'],
            'INVALID',
            "The User's name must be at least 5 characters long.")

        self.assertEqual(
            self.client.create_user(
                key=self.key2a,
                user_name=self.user3a,
                user_id=self.key3a.public_key,
                manager_id=self.key2a.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key1,
                user_name=self.user2b,
                user_id=self.key2b.public_key,
                manager_id=self.key1.public_key)[0]['status'],
            'COMMITTED')

        self.assertEqual(
            self.client.create_user(
                key=self.key3b,
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
                admins=[self.key1.public_key, self.key2a.public_key])[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.create_role(
                key=self.key1,
                role_name=role1,
                role_id=self.role_id1,
                metadata=metadata,
                admins=[self.key2a.public_key])[0]['status'],
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
                admins=[self.key_invalid.public_key, self.key2b.public_key])[0]['status'],
            "INVALID",
            "All Admins listed must be Users")

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

    def create_user(self, key, user_name, user_id, manager_id=None):
        batch_list, signature = create_user(key,
                                            BATCHER_KEY,
                                            user_name,
                                            user_id,
                                            uuid4().hex,
                                            manager_id)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def create_role(self, key, role_name, role_id, metadata, admins):
        batch_list, signature = create_role(txn_key=key,
                                            batch_key=BATCHER_KEY,
                                            role_name=role_name,
                                            role_id=role_id,
                                            metadata=metadata,
                                            admins=admins)
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


def make_key_and_name():
    private_key = signing.generate_privkey()
    pubkey = signing.generate_pubkey(private_key)

    key = Key(public_key=pubkey, private_key=private_key)
    return key, uuid4().hex
