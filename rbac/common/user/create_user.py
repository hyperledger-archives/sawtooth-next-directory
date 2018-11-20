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
"""Implements the CREATE_USER message
usage: rbac.user.create()"""
import logging

from rbac.common import addresser
from rbac.common.base.base_message import BaseMessage
from rbac.common.crypto.keys import Key

LOGGER = logging.getLogger(__name__)


class CreateUser(BaseMessage):
    """Implements the CREATE_USER message
    usage: rbac.user.create()"""

    @property
    def register_message(self):
        """Whether to register this message with the transaction processor"""
        return True  # TODO: remove after TP refactor as default will become True

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.CREATE

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SELF

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES

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

    def validate(self, message, signer=None):
        """Validates the message values"""
        signer = super(CreateUser, self).validate(message=message, signer=signer)
        if len(message.name) < 5:
            raise ValueError("Users must have names longer than 4 characters")
        if message.manager_id is not None:
            if message.user_id == message.manager_id:
                raise ValueError("User cannot be their own manager")
        if signer is not None:
            if signer not in [message.user_id, message.manager_id]:
                raise ValueError("Signer must be the user or their manager")

    def validate_state(self, state, message, signer):
        """Validates the message against state"""
        super(CreateUser, self).validate_state(
            state=state, message=message, signer=signer
        )
        if addresser.user.exists_in_state(state=state, object_id=message.user_id):
            raise ValueError("User with id {} already exists!!".format(message.user_id))
        if message.manager_id and not addresser.user.exists_in_state(
            state=state, object_id=message.manager_id
        ):
            raise ValueError(
                "Manager with id {} does not exist!!".format(message.manager_id)
            )
