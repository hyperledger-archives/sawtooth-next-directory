# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Test suite for user operations"""

import unittest
import pytest

from tests.blockchain.rbac_client_helper_class import RbacClient
from tests.blockchain.integration_test_helper import IntegrationTestHelper
from rbac.common.crypto.keys import Key
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)

BATCHER_KEY = Key()


@pytest.mark.blockchain
class TestUserOperations(unittest.TestCase):
    """User operations."""

    @classmethod
    def setUpClass(cls):
        cls.test_helper = IntegrationTestHelper()
        cls.client = RbacClient(None, IntegrationTestHelper.get_batcher_key())
        cls.test_helper.wait_for_containers()

        cls.user_key, cls.username = cls.test_helper.make_key_and_name()
        cls.role_key, cls.role_name = cls.test_helper.make_key_and_name()

    def test_create_user(self):
        """Create user."""
        self.assertEqual(
            self.client.create_user(
                key=self.user_key,
                name=self.username,
                username=self.username,
                next_id=self.user_key.public_key,
            )[0]["status"],
            "COMMITTED",
        )

    def test_create_role_no_admin(self):
        """Create role without admin."""
        with self.assertRaises(ValueError) as err:
            self.client.create_role(
                key=self.role_key,
                role_name=self.role_name,
                role_id="role_id",
                metadata="",
                admins=[],
                owners=[],
            )
        assert str(err.exception) == "New roles must have administrators."
