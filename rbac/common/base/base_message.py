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
# pylint: disable=too-many-public-methods,cyclic-import
"""Base class for all message classes, abstracting out
common functionality and facilitating differences via
property and method overrides"""
import logging
from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.crypto.keys import PUBLIC_KEY_PATTERN
from rbac.common.sawtooth import batcher
from rbac.common.sawtooth import client
from rbac.common.sawtooth import state_client
from rbac.common.base import base_processor as processor
from rbac.common.base.base_address import AddressBase

LOGGER = logging.getLogger(__name__)


class BaseMessage(AddressBase):
    """Base class for all message classes, abstracting out
    common functionality and facilitating differences via
    property and method overrides"""

    def __init__(self):
        AddressBase.__init__(self)
        self._message_type_name = batcher.get_message_type_name(self.message_type)
        if self.register_message:
            processor.register_message_handler(self)
        else:
            processor.unregister_message_handler(self)

    @property
    def message_action_type(self):
        """The action type performed by this message"""
        return None
        # raise NotImplementedError("Class must implement this property")

    @property
    def message_subaction_type(self):
        """The subsequent action performed or proposed by this message"""
        return None

    @property
    def message_object_type(self):
        """The object type this message acts upon"""
        return self.object_type

    @property
    def message_related_type(self):
        """The related object type this message acts upon"""
        return self.related_type

    @property
    def message_relationship_type(self):
        """The relationship type this message acts upon"""
        return self.relationship_type

    @property
    def message_type_name(self):
        """The name of the message type, derives from the message properties
        Example: ObjectType.USER  MessageActionType.CREATE -> CREATE_USER
        -or- ActionType.PROPOSE, SubActionType.ADD, MessageObjectType.USER,
        RelationshipType.MANAGER -> PROPOSE_ADD_USER_MANAGER
        Override where behavior differs"""
        if (
            self.message_action_type
            and self.message_subaction_type
            and self.message_relationship_type
        ):
            return (
                self.message_action_type.name
                + "_"
                + self.message_subaction_type.name
                + "_"
                + self.message_object_type.name
                + "_"
                + self.message_relationship_type.name
            )
        if self.message_action_type.name:
            return self.message_action_type.name + "_" + self.message_object_type.name
        return self._message_type_name

    @property
    def message_type(self):
        """The message type of this message, an atrribute enum of RBACPayload
        Defaults to protobuf.rbac_payload_pb2.{message_type_name}
        (see message_type_name) Override message_type_name where behavior differs"""
        if not self.message_action_type:
            raise NotImplementedError("Class must implement this property")
        return getattr(protobuf.rbac_payload_pb2.RBACPayload, self.message_type_name)

    @property
    def message_proto(self):
        """The protobuf used to serialize this message type
        Derives name form the object type and message action type names.
        Example: ObjectType.USER  MessageActionType.CREATE
        -> protobuf.user_transaction_pb2.CreateUser
        (see message_type_name) Override where behavior differs"""
        if not self.message_action_type:
            raise NotImplementedError("Class must implement this property")
        return getattr(
            getattr(
                protobuf, self.message_object_type.name.lower() + "_transaction_pb2"
            ),
            self._camel_case(self.message_type_name),
        )

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on its state object"""
        return []

    @property
    def register_message(self):
        """Whether to register this message handler with the transaction processor"""
        return False  # TODO: default will flip to True after TP refactor

    def make(self, **kwargs):
        """Makes the message (protobuf) from the named arguments passed to make"""
        # pylint: disable=not-callable
        message = self.message_proto()
        batcher.make_message(message, self.message_type, **kwargs)
        if hasattr(message, self._name_id) and getattr(message, self._name_id) == "":
            # sets the unique identifier field of the message to a unique_id if no identifier is provided
            setattr(message, self._name_id, self.unique_id())
        self.validate(message=message)
        return message

    def make_addresses(self, message, signer_keypair):
        """Make addresses returns the inputs (read) and output (write)
        addresses that may be required in order to validate the message
        and store the resulting data of a successful or failed execution"""
        raise NotImplementedError("Class must implement this method")

    def validate(self, message, signer=None):
        """Commmon validation for all messages"""
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))
        if (
            signer is not None
            and not isinstance(signer, Key)
            and not (isinstance(signer, str) and PUBLIC_KEY_PATTERN.match(signer))
        ):
            raise TypeError("Expected signer to be a keypair or a public key")
        if isinstance(signer, Key):
            signer = signer.public_key
        return signer

    def validate_state(self, state, message, signer):
        """Common state validation for all messages"""
        if signer is None:
            raise ValueError("Signer is required")
        if message is None:
            raise ValueError("Message is required")
        if not isinstance(signer, str) and PUBLIC_KEY_PATTERN.match(signer):
            raise TypeError("Expected signer to be a public key")
        if state is None:
            raise ValueError("State is required")

    def make_payload(self, message, signer_keypair=None):
        """Make a payload for the given message type"""
        self.validate(message=message, signer=signer_keypair)

        message_type = self.message_type
        inputs, outputs = self.make_addresses(
            message=message, signer_keypair=signer_keypair
        )
        return batcher.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )

    def create(self, signer_keypair, message, object_id=None, target_id=None):
        """Send a message to the blockchain"""
        self.validate(message=message, signer=signer_keypair)

        return self.send(
            signer_keypair=signer_keypair,
            payload=self.make_payload(message=message, signer_keypair=signer_keypair),
            object_id=object_id,
            target_id=target_id,
        )

    def send(self, signer_keypair, payload, object_id=None, target_id=None):
        """Sends a payload to the validator API"""
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")
        if not isinstance(payload, protobuf.rbac_payload_pb2.RBACPayload):
            raise TypeError("Expected payload to be an RBACPayload")

        _, _, batch_list, _ = batcher.make(
            payload=payload, signer_keypair=signer_keypair
        )
        got = None

        status = client.send_batches_get_status(batch_list=batch_list)

        if object_id is not None:
            got = self.get(object_id=object_id, target_id=target_id)

        return got, status

    def get(self, object_id, target_id=None):
        """Gets an address from the blockchain from the validator API"""
        address = self.address(object_id=object_id, target_id=target_id)
        # pylint: disable=not-callable
        container = self._state_container()
        container.ParseFromString(client.get_address(address=address))
        return self._find_in_state_container(
            container=container,
            address=address,
            object_id=object_id,
            target_id=target_id,
        )

    def message_to_storage(self, message):
        """Transforms the message into the state (storage) object"""
        # pylint: disable=not-callable
        return batcher.message_to_message(
            self._state_object(), self._name_camel, message
        )

    def set_state(self, state, message, object_id, target_id=None):
        """Creates a new address in the blockchain state"""
        store = self.message_to_storage(message=message)
        # pylint: disable=no-member,not-callable
        container = self._state_container()
        container.users.extend([store])
        address = self.address(object_id=object_id, target_id=target_id)
        state_client.set_address(state=state, address=address, container=container)

    def apply(self, header, payload, state):
        """Handles a message in the transaction processor"""
        # pylint: disable=not-callable
        message = self.message_proto()
        message.ParseFromString(payload.content)
        signer = header.signer_public_key
        self.validate(message=message, signer=signer)
        self.validate_state(state=state, message=message, signer=signer)
        self.set_state(state=state, message=message, object_id=message.user_id)
