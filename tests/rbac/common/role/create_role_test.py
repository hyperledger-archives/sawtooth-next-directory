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
"""Create Role test"""

# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class CreateRoleTest(TestAssertions):
    """Create Role test"""

    @pytest.mark.library
    @pytest.mark.address
    def test_address(self):
        """Test the address method and that it is in sync with the addresser"""
        role_id = helper.role.id()
        address1 = rbac.role.address(object_id=role_id)
        address2 = rbac.addresser.role.address(role_id)
        self.assertEqual(address1, address2)

    @pytest.mark.library
    def test_make(self):
        """Test making a message"""
        name = helper.role.name()
        role_id = helper.role.id()
        user_id = helper.user.id()
        message = rbac.role.make(
            role_id=role_id, name=name, owners=[user_id], admins=[user_id]
        )
        self.assertIsInstance(message, protobuf.role_transaction_pb2.CreateRole)
        self.assertIsInstance(message.role_id, str)
        self.assertIsInstance(message.name, str)
        self.assertEqual(message.role_id, role_id)
        self.assertEqual(message.name, name)
        self.assertEqual(message.owners, [user_id])
        self.assertEqual(message.admins, [user_id])

    @pytest.mark.library
    def test_make_addresses(self):
        """Test the make addresses method for the message"""
        name = helper.role.name()
        role_id = helper.role.id()
        role_address = rbac.role.address(role_id)
        user_id = helper.user.id()
        user_address = rbac.user.address(user_id)
        owner_address = rbac.role.owner.address(role_id, user_id)
        admin_address = rbac.role.admin.address(role_id, user_id)
        message = rbac.role.make(
            role_id=role_id, name=name, owners=[user_id], admins=[user_id]
        )

        inputs, outputs = rbac.role.make_addresses(message=message)

        self.assertIsInstance(inputs, list)
        self.assertIn(role_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(owner_address, inputs)
        self.assertIn(admin_address, inputs)
        self.assertEqual(
            len(inputs), 5
        )  # user_address will appear twice, as owner and admin
        self.assertEqual(inputs, outputs)

    @pytest.mark.library
    def test_make_payload(self):
        """Test making a payload for a CreateRole message"""
        name = helper.role.name()
        role_id = helper.role.id()
        user_id = helper.user.id()
        role_address = rbac.role.address(role_id)
        user_address = rbac.user.address(user_id)
        owner_address = rbac.role.owner.address(role_id, user_id)
        admin_address = rbac.role.admin.address(role_id, user_id)
        message = rbac.role.make(
            role_id=role_id, name=name, owners=[user_id], admins=[user_id]
        )

        payload = rbac.role.make_payload(message=message)

        self.assertEqual(
            payload.message_type, protobuf.rbac_payload_pb2.RBACPayload.CREATE_ROLE
        )
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(role_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(owner_address, inputs)
        self.assertIn(admin_address, inputs)
        self.assertEqual(
            len(inputs), 5
        )  # user_address will appear twice, as owner and admin
        self.assertEqual(inputs, outputs)

    @pytest.mark.integration
    def test_create(self):
        """Test creating a role"""
        user, keypair = helper.user.create()
        name = helper.role.name()
        role_id = helper.role.id()
        message = rbac.role.make(
            role_id=role_id, name=name, owners=[user.user_id], admins=[user.user_id]
        )

        role, status = rbac.role.create(
            signer_keypair=keypair, message=message, object_id=role_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(role, message, rbac.role.message_fields_not_in_state)
        self.assertTrue(
            rbac.role.owner.exists(object_id=role.role_id, target_id=user.user_id)
        )
        self.assertTrue(
            rbac.role.admin.exists(object_id=role.role_id, target_id=user.user_id)
        )
