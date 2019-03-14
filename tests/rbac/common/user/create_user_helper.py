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
"""Create User Test Helper"""
# pylint: disable=no-member,too-few-public-methods,invalid-name

from rbac.common.user import User
from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.logs import get_default_logger
from tests.rbac.testdata.user import UserTestData

LOGGER = get_default_logger(__name__)


class CreateUserTestHelper(UserTestData):
    """Create User Test Helper"""

    def message(self):
        """Get a test data CreateUser message with a new keypair"""
        next_id = self.id()
        name = self.name()
        keypair = self.key()
        user = User().make(next_id=next_id, name=name, key=keypair.public_key)
        assert isinstance(user, protobuf.user_transaction_pb2.CreateUser)
        assert user.next_id == next_id
        assert user.name == name
        assert user.key == keypair.public_key
        return user, keypair

    def imports_message(self):
        """ Get a test data ImportsUser message
        """
        name = self.name()
        user = User().imports.make(name=name)

        assert isinstance(user, protobuf.user_transaction_pb2.ImportsUser)
        assert user.name == name
        return user

    def message_with_manager(self):
        """Get a test data CreateUser message for user and manager"""
        manager, manager_key = self.message()
        next_id = self.id()
        user_key = self.key()
        user = User().make(
            next_id=next_id,
            name=self.name(),
            manager_id=manager.next_id,
            key=user_key.public_key,
        )
        assert manager.next_id == user.manager_id
        return user, user_key, manager, manager_key

    def create(self):
        """Create a test user"""
        message, keypair = self.message()

        status = User().new(
            signer_user_id=message.next_id, signer_keypair=keypair, message=message
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        user = User().get(object_id=message.next_id)

        assert user.next_id == message.next_id
        assert user.name == message.name
        return user, keypair

    def imports(self):
        """ Imports a test user
            Imported user has no key assignment
        """
        signer_keypair = Key()  # TODO: will need to change to a provider key

        message = self.imports_message()

        status = User().imports.new(
            signer_user_id=message.next_id,
            signer_keypair=signer_keypair,
            message=message,
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        user = User().get(object_id=message.next_id)

        assert user.next_id == message.next_id
        assert user.name == message.name
        return user

    def create_with_manager(self):
        """Create a test user with manager"""
        manager, manager_key = self.create()

        message, user_key = self.message()
        message.manager_id = manager.next_id

        status = User().new(
            signer_user_id=message.manager_id,
            signer_keypair=manager_key,
            message=message,
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        user = User().get(object_id=message.next_id)

        assert user.next_id == message.next_id
        assert user.name == message.name
        assert user.manager_id == manager.next_id
        return user, user_key, manager, manager_key

    def create_with_grand_manager(self):
        """Create a test user with manager and their manager"""
        grandmgr, grandmgr_key = self.create()

        message, manager_key = self.message()
        message.manager_id = grandmgr.next_id

        status = User().new(
            signer_user_id=grandmgr.next_id,
            signer_keypair=grandmgr_key,
            message=message,
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        manager = User().get(object_id=message.next_id)
        assert manager.next_id == message.next_id
        assert manager.name == message.name
        assert manager.manager_id == grandmgr.next_id

        message, user_key = self.message()
        message.manager_id = manager.next_id

        status = User().new(
            signer_user_id=manager.next_id, signer_keypair=manager_key, message=message
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        user = User().get(object_id=message.next_id)

        assert user.next_id == message.next_id
        assert user.name == message.name
        assert user.manager_id == manager.next_id
        return user, user_key, manager, manager_key, grandmgr, grandmgr_key
