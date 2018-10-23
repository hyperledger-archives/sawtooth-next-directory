# Copyright contributors to Hyperledger Sawtooth
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
import random
from uuid import uuid4

from rbac.common.crypto.keys import Key
from rbac.common.protobuf import user_state_pb2
from tests.rbac.common.user.user_manager_test import UserManagerTest
from rbac.common.role.role_manager import RoleManager

# from rbac.common.proposal.proposal_manager import ProposalManager
# from tests.rbac.common.user.test_user_manager import TestUserManager
from rbac.common.protobuf import role_transaction_pb2
from tests.rbac.common.manager.test_assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
@pytest.mark.role_it
class RoleManagerTest(RoleManager, TestAssertions):
    def __init__(self, *args, **kwargs):
        TestAssertions.__init__(self, *args, **kwargs)
        RoleManager.__init__(self)
        self.user = UserManagerTest()

    def get_data_user_role(self):
        user, keypair = self.user.test_create()
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertIsInstance(keypair, Key)
        name = self.get_data_rolename()
        role_id = uuid4().hex
        role = self.make(
            role_id=role_id, name=name, admins=[user.user_id], owners=[user.user_id]
        )
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role, user, keypair

    def get_data_role(self, role_id=None):
        name = self.get_data_rolename()
        if role_id is None:
            role_id = uuid4().hex
        role = self.make(role_id=role_id, name=name)
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role

    def get_data_rolename(self):
        return "Role" + str(random.randint(1000, 10000))

    @pytest.mark.unit
    def test_role_manager_interface(self):
        self.assertIsInstance(self, RoleManagerTest)
        self.assertTrue(callable(self.make))
        self.assertTrue(callable(self.create))
        self.assertTrue(callable(self.get))

    @pytest.mark.unit
    def test_role_manager_test_interface(self):
        self.assertTrue(callable(self.get_data_rolename))
        self.assertTrue(callable(self.get_data_role))

    @pytest.mark.unit
    def test_role_manager_user_interface(self):
        self.assertIsInstance(self.user, UserManagerTest)
        self.assertTrue(callable(self.user.make))
        self.assertTrue(callable(self.user.create))
        self.assertTrue(callable(self.user.get))

    @pytest.mark.unit
    def test_role_manager_user_test_interface(self):
        self.assertIsInstance(self.user, UserManagerTest)
        self.assertTrue(callable(self.user.get_test_name))
        self.assertTrue(callable(self.user.get_test_username))
        self.assertTrue(callable(self.user.get_test_user))
        self.assertTrue(callable(self.user.get_test_user_with_key))

    @pytest.mark.unit
    def test_get_data_role(self):
        role = self.get_data_role()
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)

    @pytest.mark.integration
    def test_create(self, role=None, user=None, keypair=None):
        if user is None and role is None:
            role, user, keypair = self.get_data_user_role()
        if user is None:
            user, keypair = self.user.test_create()
        if role is None:
            role = self.get_data_role()
            role.admins = [user.user_id]
            role.owners = [user.user_id]
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)

        status = self.create(signer_keypair=keypair, role=role)
        self.assertEqual(status[0]["status"], "COMMITTED")
        check = self.get(role_id=role.role_id)
        self.assertEqual(check.name, role.name)
        self.assertTrue(self.check_owner(role_id=role.role_id, user_id=user.user_id))
        self.assertTrue(self.check_admin(role_id=role.role_id, user_id=user.user_id))
        return role, user, keypair
