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
from uuid import uuid4
import pytest

from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.role.role_manager import RoleManager

# from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
# from rbac.common.sawtooth import batcher

from tests.rbac.common.role.role_test_helper import RoleTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class CreateRoleTest(RoleTestHelper):
    def __init__(self, *args, **kwargs):
        RoleTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.role, RoleManager)
        self.assertTrue(callable(self.role.address))
        self.assertTrue(callable(self.role.make))
        self.assertTrue(callable(self.role.make_addresses))
        self.assertTrue(callable(self.role.make_payload))
        self.assertTrue(callable(self.role.create))
        self.assertTrue(callable(self.role.send))
        self.assertTrue(callable(self.role.get))

    @pytest.mark.unit
    def test_helper_interface(self):
        """Verify the expected user test helper interface"""
        self.assertTrue(callable(self.get_testdata_name))
        self.assertTrue(callable(self.get_testdata_username))
        self.assertTrue(callable(self.get_testdata_user))
        self.assertTrue(callable(self.get_testdata_user_with_key))
        self.assertTrue(callable(self.get_testdata_reason))
        self.assertTrue(callable(self.get_testdata_user_created))
        self.assertTrue(callable(self.get_testdata_user_created_with_manager))
        self.assertTrue(callable(self.get_testdata_rolename))
        self.assertTrue(callable(self.get_testdata_role))
        self.assertTrue(callable(self.get_testunit_user_role))
        self.assertTrue(callable(self.get_testdata_user_role))

    @pytest.mark.unit
    @pytest.mark.address
    def test_address(self):
        """Test the address method and that it is in sync with the addresser"""
        self.assertTrue(callable(self.role.address))

        role = self.get_testdata_role()
        self.assertIsInstance(role, protobuf.role_transaction_pb2.CreateRole)
        self.assertIsInstance(role.role_id, str)
        address1 = self.role.address(object_id=role.role_id)
        address2 = addresser.role.address(role.role_id)
        self.assertEqual(address1, address2)

    @pytest.mark.unit
    def test_make(self):
        """Test getting a test data user with keys"""
        self.assertTrue(callable(self.role.make))
        name = self.get_testdata_rolename()
        role_id = uuid4().hex
        message = self.role.make(role_id=role_id, name=name)
        self.assertIsInstance(message, protobuf.role_transaction_pb2.CreateRole)
        self.assertIsInstance(message.role_id, str)
        self.assertIsInstance(message.name, str)
        self.assertEqual(message.role_id, role_id)
        self.assertEqual(message.name, name)

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test the make addresses method for a CreateRole message"""
        self.assertTrue(callable(self.role.make_addresses))
        self.assertTrue(callable(self.get_testdata_user_with_key))
        self.assertTrue(callable(self.get_testdata_role))

        message, user, _ = self.get_testunit_user_role()
        inputs, outputs = self.role.make_addresses(message=message)

        role_address = addresser.role.address(message.role_id)
        user_address = addresser.user.address(user.user_id)
        owner_address = addresser.role.owner.address(message.role_id, user.user_id)
        admin_address = addresser.role.admin.address(message.role_id, user.user_id)

        self.assertIsInstance(inputs, list)
        self.assertIn(role_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(owner_address, inputs)
        self.assertIn(admin_address, inputs)
        self.assertEqual(inputs, outputs)

    # @pytest.mark.skip(reason="This test is too entangled to troubleshoot easily")
    # @pytest.mark.unit
    # def test_make_payload(self):
    #     """Test making a payload for a CreateRole message"""
    #     self.assertTrue(callable(self.get_testdata_user_with_key))
    #     self.assertTrue(callable(self.get_testdata_role))
    #
    #     message, user, _ = self.get_testunit_user_role()
    #     payload = batcher.make_payload(message=message)
    #     self.assertEqual(payload.message_type, RBACPayload.CREATE_ROLE)
    #
    #     role_address = addresser.role.address(message.role_id)
    #     user_address = addresser.user.address(user.user_id)
    #     owner_address = addresser.role.owner.address(message.role_id, user.user_id)
    #     admin_address = addresser.role.admin.address(message.role_id, user.user_id)
    #
    #     inputs = list(payload.inputs)
    #     outputs = list(payload.outputs)
    #     self.assertIsInstance(inputs, list)
    #     self.assertIn(role_address, inputs)
    #     self.assertIn(user_address, inputs)
    #     self.assertIn(owner_address, inputs)
    #     self.assertIn(admin_address, inputs)
    #     self.assertEqual(inputs, outputs)

    @pytest.mark.integration
    def test_create(self, role=None, user=None, keypair=None):
        """Test creating a role"""
        self.assertTrue(callable(self.role.create))
        self.assertTrue(callable(self.get_testdata_user_role))

        if user is None and role is None:
            role, user, keypair = self.get_testdata_user_role()
        if user is None:
            user, keypair = self.get_testdata_user_created()
        if role is None:
            role = self.get_testdata_role()
            role.admins = [user.user_id]
            role.owners = [user.user_id]
        self.assertIsInstance(role, protobuf.role_transaction_pb2.CreateRole)

        got, status = self.role.create(
            signer_keypair=keypair, message=role, object_id=role.role_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, role, self.role.message_fields_not_in_state)
        self.assertTrue(
            self.role.owner.exists(object_id=role.role_id, target_id=user.user_id)
        )
        self.assertTrue(
            self.role.admin.exists(object_id=role.role_id, target_id=user.user_id)
        )
        # self.assertFalse(
        #    self.role.member.exists(object_id=role.role_id, target_id=user.user_id)
        # )
        return got, user, keypair
