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
from rbac.common import protobuf
from rbac.common.manager.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class CreateUser(BaseMessage):
    def __init__(self):
        BaseMessage.__init__(self)

    @property
    def name(self):
        return "user"

    @property
    def message_type(self):
        return protobuf.rbac_payload_pb2.RBACPayload.CREATE_USER

    @property
    def message_proto(self):
        return protobuf.user_transaction_pb2.CreateUser

    @property
    def container_proto(self):
        return protobuf.user_state_pb2.UserContainer

    @property
    def state_proto(self):
        return protobuf.user_state_pb2.User

    def address(self, object_id, target_id=None):
        """Make an address for the given user_id"""
        return make_user_address(object_id)

    # pylint: disable=arguments-differ, not-callable
    def make(
        self, user_id, name, user_name=None, email=None, metadata=None, manager_id=None
    ):
        """Makes a CreateUser message"""
        message = self.message_proto(
            user_id=user_id, name=name, metadata=metadata, manager_id=manager_id
        )
        self.validate(message=message)
        return message

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

    def make_addresses(self, message, signer_keypair=None):
        """Makes the appropriate inputs & output addresses for the message type"""
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))

        user_address = self.address(object_id=message.user_id)
        if message.manager_id:
            manager_address = self.address(object_id=message.manager_id)

        if message.manager_id:
            inputs = [user_address, manager_address]
        else:
            inputs = [user_address]

        outputs = inputs
        return inputs, outputs

    def validate(self, message, signer=None, state=None):
        """Validates the message values"""
        signer = self.base_validate(message=message, signer=signer)
        if len(message.name) < 5:
            raise ValueError("Users must have names longer than 4 characters")
        if message.manager_id is not None:
            if message.user_id == message.manager_id:
                raise ValueError("User cannot be their own manager")
        if signer is not None:
            if signer not in [message.user_id, message.manager_id]:
                raise ValueError("Signer must be the user or their manager")
        if state is not None:
            self.validate_state(state=state, message=message, signer=signer)

    def validate_state(self, state, message, signer):
        """Validates the message against state"""
        self.base_validate_state(state=state, message=message, signer=signer)
        if self.exists_state(state=state, object_id=message.user_id):
            raise ValueError("User already exists")
        if message.manager_id and not self.exists_state(
            state=state, object_id=message.manager_id
        ):
            raise ValueError("Manager does not exist")

    def set_state(self, state, message, object_id, target_id=None):
        """Creates a new address in the blockchain state"""
        address = self.address(object_id=object_id, target_id=target_id)
        container = self.container_proto()
        item = self.state_proto(
            user_id=message.user_id,
            name=message.name,
            manager_id=message.manager_id,
            metadata=message.metadata,
        )
        container.users.extend([item])
        self.state.set_address(state=state, address=address, container=container)

    def apply(self, header, payload, state):
        """Handles a message in the transaction processor"""
        message = self.message_proto()
        message.ParseFromString(payload.content)

        self.validate(message=message, signer=header.signer_public_key, state=state)
        self.set_state(state=state, message=message, object_id=message.user_id)
