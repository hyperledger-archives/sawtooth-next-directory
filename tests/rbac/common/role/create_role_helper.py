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
"""Create Role test helper"""

# pylint: disable=no-member

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.assertions import TestAssertions
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper

LOGGER = logging.getLogger(__name__)


class TestHelper(TestAssertions):
    """A minimal test helper required by this test helper"""

    def __init__(self, *args, **kwargs):
        TestAssertions.__init__(self, *args, **kwargs)
        self.user = CreateUserTestHelper()


# pylint: disable=invalid-name
helper = TestHelper()


class CreateRoleTestHelper(TestAssertions):
    """Create Role test helper"""

    def id(self):
        """Get a test role_id (not created)"""
        return rbac.addresser.role.unique_id()

    def name(self):
        """Get a random name"""
        return "Role" + str(random.randint(1000, 10000))

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def message(self):
        """Get a test data CreateRole message"""
        role_id = self.id()
        name = self.name()
        message = rbac.role.make(role_id=role_id, name=name)
        self.assertIsInstance(message, protobuf.role_transaction_pb2.CreateRole)
        self.assertEqual(message.role_id, role_id)
        self.assertEqual(message.name, name)
        return message

    def create(self):
        """Create a test role"""
        user, keypair = helper.user.create()
        message = self.message()
        message.admins.extend([user.user_id])
        message.owners.extend([user.user_id])

        role, status = rbac.role.create(
            signer_keypair=keypair, message=message, object_id=message.role_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(role, message, rbac.role.message_fields_not_in_state)
        self.assertTrue(
            rbac.role.owner.exists(object_id=role.role_id, target_id=user.user_id)
        )
        self.assertTrue(
            rbac.role.admin.exists(object_id=role.role_id, target_id=user.user_id)
        )
        return role, user, keypair
