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
# pylint: disable=no-member,too-few-public-methods

import logging

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper
from tests.rbac.testdata.role import RoleTestData

LOGGER = logging.getLogger(__name__)


class StubTestHelper:
    """A minimal test helper required by this test helper"""

    def __init__(self):
        self.user = CreateUserTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class CreateRoleTestHelper(RoleTestData):
    """Create Role test helper"""

    def message(self):
        """Get a test data CreateRole message"""
        role_id = self.id()
        name = self.name()
        user_id = helper.user.id()
        message = rbac.role.make(
            role_id=role_id, name=name, owners=[user_id], admins=[user_id]
        )
        assert isinstance(message, protobuf.role_transaction_pb2.CreateRole)
        assert message.role_id == role_id
        assert message.name == name
        return message

    def create(self):
        """Create a test role"""
        role_id = self.id()
        name = self.name()
        user, keypair = helper.user.create()
        message = rbac.role.make(
            role_id=role_id, name=name, owners=[user.user_id], admins=[user.user_id]
        )

        status = rbac.role.new(
            signer_keypair=keypair, signer_user_id=user.user_id, message=message
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        role = rbac.role.get(object_id=message.role_id)

        assert role.role_id == message.role_id
        assert role.name == message.name
        assert rbac.role.owner.exists(object_id=role.role_id, related_id=user.user_id)
        assert rbac.role.admin.exists(object_id=role.role_id, related_id=user.user_id)
        return role, user, keypair
