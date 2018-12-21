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
"""Create User Test Helper"""
# pylint: disable=no-member,too-few-public-methods,invalid-name

import logging

from rbac.common import rbac
from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from tests.rbac.testdata.user import UserTestData

LOGGER = logging.getLogger(__name__)


class CreateUserTestHelper(UserTestData):
    """Create User Test Helper"""

    def message(self):
        """Get a test data CreateUser message with a new keypair"""
        name = self.name()
        user, keypair = rbac.user.make_with_key(name=name)
        assert isinstance(user, protobuf.user_transaction_pb2.CreateUser)
        assert isinstance(keypair, Key)
        assert user.user_id == keypair.public_key
        assert user.name == name
        return user, keypair

    def message_with_manager(self):
        """Get a test data CreateUser message for user and manager"""
        manager, manager_key = self.message()
        user, user_key = rbac.user.make_with_key(
            name=self.name(), manager_id=manager.user_id
        )
        assert manager.user_id == user.manager_id
        return user, user_key, manager, manager_key

    def create(self):
        """Create a test user"""
        message, keypair = self.message()

        status = rbac.user.new(signer_keypair=keypair, message=message)

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        user = rbac.user.get(object_id=message.user_id)

        assert user.user_id == message.user_id
        assert user.name == message.name
        return user, keypair

    def create_with_manager(self):
        """Create a test user with manager"""
        manager, manager_key = self.create()

        message, user_key = self.message()
        message.manager_id = manager.user_id

        status = rbac.user.new(signer_keypair=manager_key, message=message)

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        user = rbac.user.get(object_id=message.user_id)

        assert user.user_id == message.user_id
        assert user.name == message.name
        assert user.manager_id == manager.user_id
        return user, user_key, manager, manager_key

    def create_with_grand_manager(self):
        """Create a test user with manager and their manager"""
        grandmgr, grandmgr_key = self.create()

        message, manager_key = self.message()
        message.manager_id = grandmgr.user_id

        status = rbac.user.new(signer_keypair=grandmgr_key, message=message)

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        manager = rbac.user.get(object_id=message.user_id)
        assert manager.user_id == message.user_id
        assert manager.name == message.name
        assert manager.manager_id == grandmgr.user_id

        message, user_key = self.message()
        message.manager_id = manager.user_id

        status = rbac.user.new(signer_keypair=manager_key, message=message)

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        user = rbac.user.get(object_id=message.user_id)

        assert user.user_id == message.user_id
        assert user.name == message.name
        assert user.manager_id == manager.user_id
        return user, user_key, manager, manager_key, grandmgr, grandmgr_key
