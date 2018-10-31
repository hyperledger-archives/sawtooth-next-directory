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
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import user_state_pb2
from rbac.common.protobuf import user_transaction_pb2
from tests.rbac.common.user.user_manager_test import UserManagerTest
from rbac.common.role.role_manager import RoleManager
from rbac.common.protobuf import role_transaction_pb2
from tests.rbac.common.role.role_assertions import RoleAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
@pytest.mark.role_it
class RoleManagerTest(RoleManager, RoleAssertions):
    def __init__(self, *args, **kwargs):
        """Test the RoleManager class"""
        RoleAssertions.__init__(self, *args, **kwargs)
        RoleManager.__init__(self)
        self.user = UserManagerTest()

    def get_testunit_user_role(self):
        """Get a test data for a role, user and key with the user
        as the role owner and admin. User has not been created."""
        user, keypair = self.user.get_testdata_user_with_key()
        self.assertIsInstance(user, user_transaction_pb2.CreateUser)
        self.assertIsInstance(keypair, Key)
        name = self.get_testdata_rolename()
        role_id = uuid4().hex
        role = self.make(
            role_id=role_id, name=name, admins=[user.user_id], owners=[user.user_id]
        )
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role, user, keypair

    def get_testdata_user_role(self):
        """Get a test data for a role, user and key with the user
        as the role owner and admin. User has been created."""
        user, keypair = self.user.test_create()
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertIsInstance(keypair, Key)
        name = self.get_testdata_rolename()
        role_id = uuid4().hex
        role = self.make(
            role_id=role_id, name=name, admins=[user.user_id], owners=[user.user_id]
        )
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role, user, keypair

    def get_testdata_role(self, role_id=None):
        """Get a test data for a role"""
        name = self.get_testdata_rolename()
        if role_id is None:
            role_id = uuid4().hex
        role = self.make(role_id=role_id, name=name)
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role

    def get_testdata_rolename(self):
        """Get a random name for a role"""
        return "Role" + str(random.randint(1000, 10000))

    def get_testdata_reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    @pytest.mark.unit
    def test_role_manager_interface(self):
        """Check the expected RoleManager methods exist"""
        self.assertIsInstance(self, RoleManagerTest)
        self.assertTrue(callable(self.make))
        self.assertTrue(callable(self.create))
        self.assertTrue(callable(self.get))

    @pytest.mark.unit
    def test_role_manager_test_interface(self):
        """Check the expected RoleManager test methods exist"""
        self.assertTrue(callable(self.get_testdata_rolename))
        self.assertTrue(callable(self.get_testdata_role))

    @pytest.mark.unit
    def test_role_manager_user_interface(self):
        """Check the expected UserManager methods exist"""
        self.assertIsInstance(self.user, UserManagerTest)
        self.assertTrue(callable(self.user.make))
        self.assertTrue(callable(self.user.create))
        self.assertTrue(callable(self.user.get))

    @pytest.mark.unit
    def test_role_manager_user_test_interface(self):
        """Check the expected UserManager test methods exist"""
        self.assertIsInstance(self.user, UserManagerTest)
        self.assertTrue(callable(self.user.get_testdata_name))
        self.assertTrue(callable(self.user.get_testdata_username))
        self.assertTrue(callable(self.user.get_testdata_user))
        self.assertTrue(callable(self.user.get_testdata_user_with_key))

    @pytest.mark.unit
    def test_get_testdata_role(self):
        """Test getting a test data CreateRole message"""
        role = self.get_testdata_role()
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test the make addresses method for a CreateRole message"""
        self.assertTrue(callable(self.user.get_testdata_user))
        self.assertTrue(callable(self.get_testdata_role))
        self.assertTrue(callable(self.make_addresses))
        _, keypair = self.user.get_testdata_user_with_key()
        message = self.get_testdata_role()
        inputs, outputs = self.make_addresses(
            message=message, signer_public_key=keypair.public_key
        )
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making a payload for a CreateRole message"""
        self.assertTrue(callable(self.user.get_testdata_user))
        self.assertTrue(callable(self.get_testdata_role))
        self.assertTrue(callable(self.make_payload))
        _, keypair = self.user.get_testdata_user_with_key()
        message = self.get_testdata_role()
        payload = self.make_payload(
            message=message, signer_public_key=keypair.public_key
        )
        self.assertValidPayload(
            payload=payload, message=message, message_type=RBACPayload.CREATE_ROLE
        )

    @pytest.mark.integration
    def test_create(self, role=None, user=None, keypair=None):
        """Test creating a role"""
        if user is None and role is None:
            role, user, keypair = self.get_testdata_user_role()
        if user is None:
            user, keypair = self.user.test_create()
        if role is None:
            role = self.get_testdata_role()
            role.admins = [user.user_id]
            role.owners = [user.user_id]
        self.assertIsInstance(role, role_transaction_pb2.CreateRole)

        got, status, transaction, _, _, _ = self.create(
            signer_keypair=keypair, message=role, do_get=True
        )
        self.assertValidTransaction(
            transaction=transaction,
            payload=self.make_payload(
                message=role, signer_public_key=keypair.public_key
            ),
            signer_public_key=keypair.public_key,
        )
        self.assertStatusSuccess(status)
        self.assertCreateRoleResult(role, got)
        self.assertTrue(self.check_owner(role_id=role.role_id, user_id=user.user_id))
        self.assertTrue(self.check_admin(role_id=role.role_id, user_id=user.user_id))
        return got, user, keypair

    @pytest.mark.unit
    def test_make_propose_member(self):
        """Test a message proposing a member of a role"""
        role, user, keypair = self.get_testunit_user_role()
        message = self.make_propose_member(
            role_id=role.role_id,
            user_id=user.user_id,
            reason=self.get_testdata_reason(),
        )
        self.assertIsInstance(message, role_transaction_pb2.ProposeAddRoleMember)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.user_id, user.user_id)

    @pytest.mark.unit
    def test_make_propose_owner(self):
        """Test a message proposing an owner of a role"""
        role, user, keypair = self.get_testunit_user_role()
        message = self.make_propose_owner(
            role_id=role.role_id,
            user_id=user.user_id,
            reason=self.get_testdata_reason(),
        )
        self.assertIsInstance(message, role_transaction_pb2.ProposeAddRoleOwner)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.user_id, user.user_id)

    @pytest.mark.unit
    def test_make_propose_admin(self):
        """Test message proposing an admin of a role"""
        role, user, keypair = self.get_testunit_user_role()
        message = self.make_propose_admin(
            role_id=role.role_id,
            user_id=user.user_id,
            reason=self.get_testdata_reason(),
        )
        self.assertIsInstance(message, role_transaction_pb2.ProposeAddRoleAdmin)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.user_id, user.user_id)

    @pytest.mark.integration
    def test_propose_member(self, role=None, user=None, keypair=None):
        """Test a proposing a member of a role"""
        role, user, keypair = self.test_create(role=role, user=user, keypair=keypair)
        message = self.make_propose_member(
            role_id=role.role_id,
            user_id=user.user_id,
            reason=self.get_testdata_reason(),
        )
        self.assertIsInstance(message, role_transaction_pb2.ProposeAddRoleMember)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.user_id, user.user_id)

        got, status, transaction, _, _, _ = self.create(
            signer_keypair=keypair, message=message, do_get=False
        )
        self.assertValidTransaction(
            transaction=transaction,
            payload=self.make_payload(
                message=message, signer_public_key=keypair.public_key
            ),
            signer_public_key=keypair.public_key,
        )
        self.assertStatusSuccess(status)
        # self.assertProposeMemberResult(role, got)
        return got, user, keypair

    @pytest.mark.integration
    def test_propose_owner(self, role=None, user=None, keypair=None):
        """Test a proposing an owner of a role"""
        role, _, _ = self.test_create(role=role, user=user, keypair=keypair)
        user, keypair = self.user.test_create()
        message = self.make_propose_owner(
            role_id=role.role_id,
            user_id=user.user_id,
            reason=self.get_testdata_reason(),
        )
        self.assertIsInstance(message, role_transaction_pb2.ProposeAddRoleOwner)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.user_id, user.user_id)

        got, status, transaction, _, _, _ = self.create(
            signer_keypair=keypair, message=message, do_get=False
        )
        self.assertValidTransaction(
            transaction=transaction,
            payload=self.make_payload(
                message=message, signer_public_key=keypair.public_key
            ),
            signer_public_key=keypair.public_key,
        )
        self.assertStatusSuccess(status)
        # self.assertProposeOwnerResult(role, got)
        return got, user, keypair

    @pytest.mark.integration
    def test_propose_admin(self, role=None, user=None, keypair=None):
        """Test a proposing an admin of a role"""
        role, _, _ = self.test_create(role=role, user=user, keypair=keypair)
        user, keypair = self.user.test_create()
        message = self.make_propose_admin(
            role_id=role.role_id,
            user_id=user.user_id,
            reason=self.get_testdata_reason(),
        )
        self.assertIsInstance(message, role_transaction_pb2.ProposeAddRoleAdmin)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.user_id, user.user_id)

        got, status, transaction, _, _, _ = self.create(
            signer_keypair=keypair, message=message, do_get=False
        )
        self.assertValidTransaction(
            transaction=transaction,
            payload=self.make_payload(
                message=message, signer_public_key=keypair.public_key
            ),
            signer_public_key=keypair.public_key,
        )
        self.assertStatusSuccess(status)
        # self.assertProposeAdminResult(role, got)
        return got, user, keypair
