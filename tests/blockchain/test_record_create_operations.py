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

import sys
import logging
import pytest
import unittest

from tests.blockchain.rbac_client import RbacClient
from tests.blockchain.integration_test_helper import IntegrationTestHelper
from rbac.transaction_creation.common import Key
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

BATCHER_PRIVATE_KEY = Secp256k1PrivateKey.new_random().as_hex()
BATCHER_KEY = Key(BATCHER_PRIVATE_KEY)

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


@pytest.mark.integration
class TestUserOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_helper = IntegrationTestHelper()
        cls.client = RbacClient(None, IntegrationTestHelper.get_batcher_key())
        cls.test_helper.wait_for_containers()

        cls.user_key, cls.user_name = cls.test_helper.make_key_and_name()
        cls.role_key, cls.role_name = cls.test_helper.make_key_and_name()

    def test_create_user(self):
        self.assertEqual(
            self.client.create_user(
                key=self.user_key,
                name=self.user_name,
                user_name=self.user_name,
                user_id=self.user_key.public_key,
            )[0]["status"],
            "COMMITTED",
        )

    def test_create_role_no_admin(self):
        response = self.client.create_role(
            key=self.role_key,
            role_name=self.role_name,
            role_id="role_id",
            metadata="",
            admins=[],
            owners=[],
        )[0]
        self.assertEqual(
            response["invalid_transactions"][0]["message"],
            "Role must have at least one admin",
        )
