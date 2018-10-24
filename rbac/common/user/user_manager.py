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
from rbac.common.crypto.keys import Key
from rbac.common.user.user_address import make_user_address
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import user_transaction_pb2
from rbac.common.protobuf import user_state_pb2
from rbac.common.manager.base_manager import BaseManager

LOGGER = logging.getLogger(__name__)


class UserManager(BaseManager):
    def __init__(self):
        BaseManager.__init__(self)

    def address(self, user_id):
        """Make an address for the given user_id"""
        return make_user_address(user_id=user_id)

    def make(
        self, user_id, name, user_name=None, email=None, metadata=None, manager_id=None
    ):
        """Makes a CreateUser message"""
        return user_transaction_pb2.CreateUser(
            user_id=user_id, name=name, metadata=metadata, manager_id=manager_id
        )

    def make_with_key(
        self,
        name,
        user_id=None,
        user_name=None,
        email=None,
        metadata=None,
        manager_id=None,
    ):
        """Makes a CreateUser message with a new keypair"""
        keypair = Key()
        if user_id is None:
            user_id = keypair.public_key
        message = self.make(
            user_id=user_id,
            name=name,
            user_name=user_name,
            email=email,
            metadata=metadata,
            manager_id=manager_id,
        )
        return message, keypair

    def make_payload(self, message):
        """Make a payload for the given message type"""
        if isinstance(message, user_transaction_pb2.CreateUser):
            message_type = RBACPayload.CREATE_USER
            inputs, outputs = self.make_addresses(message=message)
        else:
            raise TypeError(
                "Expected message to be a user_transaction_pb2.CreateUser, use make first"
            )

        return self.batch.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )

    def make_addresses(self, message):
        """Makes the approporiate inputs & output addresses for the message type"""
        if isinstance(message, user_transaction_pb2.CreateUser):
            inputs = [self.address(user_id=message.user_id)]
            if message.manager_id:
                inputs.append(self.address(user_id=message.manager_id))
            outputs = inputs
        else:
            raise TypeError("Expected message to be a user_transaction_pb2.CreateUser")
        return inputs, outputs

    def create(self, signer_keypair, message, do_send=True, do_get=False):
        """Create a user object in the blockchain"""
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")

        return self.send(
            signer_keypair=signer_keypair,
            object_id=message.user_id,
            payload=self.make_payload(message=message),
            do_send=do_send,
            do_get=do_get,
        )

    def get(self, object_id):
        """Gets a user object from the blockchain"""
        address = self.address(user_id=object_id)
        user_container = user_state_pb2.UserContainer()
        user_container.ParseFromString(self.client.get_address(address=address))
        users = list(user_container.users)
        if len(users) == 0:
            return None
        elif len(users) > 1:
            LOGGER.warning(
                "user container at address %s has more than one record, looking for %s",
                address,
                object_id,
            )
        for user in users:
            if user.user_id == object_id:
                return user
        LOGGER.warning("user %s not found in container address %s", object_id, address)
        return None
