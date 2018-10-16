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
from tests.rbac.common.user.user_assertions import UserAssertions
from tests.rbac.common.user.test_user_data import UserTestData
from rbac.processor.protobuf import user_state_pb2

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.user_it
class TestUserManager(UserAssertions, UserTestData):
    def __init__(self, *args, **kwargs):
        UserAssertions.__init__(self, *args, **kwargs)
        UserTestData.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_user_manager_interface(self):
        self.assertTrue(callable(self.user.make))
        self.assertTrue(callable(self.user.make_with_key))
        self.assertTrue(callable(self.user.create))
        self.assertTrue(callable(self.user.get))

    @pytest.mark.unit
    def test_testdata_interface(self):
        self.assertTrue(callable(self.get_testdata_name))
        self.assertTrue(callable(self.get_testdata_username))
        self.assertTrue(callable(self.get_testdata_user))
        self.assertTrue(callable(self.get_testdata_user_with_key))

    @pytest.mark.unit
    def test_get_testdata_user_with_keys(self):
        user, keypair = self.get_testdata_user_with_key()
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(user.name, str)
        # self.assertIsInstance(user.user_name, str)
        self.assertIsInstance(keypair, Key)

    @pytest.mark.integration
    def test_create(self, user=None, keypair=None):
        if user is None:
            user, keypair = self.get_testdata_user_with_key()

        status = self.user.create(signer_keypair=keypair, user=user)
        self.assertEqual(status[0]["status"], "COMMITTED")
        check = self.user.get(user_id=user.user_id)
        self.assertEqual(check.name, user.name)
        return check, keypair

    @pytest.mark.integration
    def test_create_with_manager(self):
        manager, _ = self.test_create()

        user, user_keypair = self.get_testdata_user_with_key()
        user.manager_id = manager.user_id

        check_user, _ = self.test_create(user=user, keypair=user_keypair)
        self.assertEqual(check_user.manager_id, manager.user_id)
