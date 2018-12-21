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
from rbac.common import addresser
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
        super().__init__()
        self._message_type_name = batcher.get_message_type_name(self.message_type)

    def _register(self):
        """Registers the class as the authoritative message handler for this message type"""
        processor.register_message_handler(self)

    def _unregister(self):
        """Unregisters the class as the authoritative message handler for this message type"""
        processor.unregister_message_handler(self)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        raise NotImplementedError("Class must implement this property")

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        raise NotImplementedError("Class must implement this property")

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class,
        if it is an address type that stores relationships"""
        raise NotImplementedError("Class must implement this property")

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class,
        if it is an address type that stores relationships"""
        raise NotImplementedError("Class must implement this property")

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
    def _name_id(self):
        """The attribute name for the object type
        Example: ObjectType.USER -> 'user_id'
        Override where behavior deviates from this norm"""
        if self.message_object_type == self.object_type:
            return self._name_lower + "_id"
        return self.message_object_type.name.lower() + "_id"

    @property
    def _related_id(self):
        """The attribute name for the related_id if not related_id
        e.g. RelatedType.TASK -> 'task_id'
        RelationshipType.MANAGER -> 'manager_id
        Override where behavior deviates from this norm"""
        if self.message_related_type == self.related_type:
            return "related_id"
        if self.message_related_type == self.message_object_type:
            return self.message_relationship_type.name.lower() + "_id"
        return self.message_related_type.name.lower() + "_id"

    @property
    def message_type_name(self):
        """The name of the message type, derives from the message properties
        Example: ObjectType.USER  MessageActionType.CREATE -> CREATE_USER
        -or- ActionType.PROPOSE, SubActionType.UPDATE, MessageObjectType.USER,
        RelationshipType.MANAGER -> PROPOSE_UPDATE_USER_MANAGER
        Override where behavior differs"""
        if (
            self.message_action_type
            and self.message_subaction_type
            and self.message_relationship_type
        ):
            if (
                self.message_related_type
                and self.message_related_type != addresser.address_space.ObjectType.USER
            ):
                return (
                    self.message_action_type.name
                    + "_"
                    + self.message_subaction_type.name
                    + "_"
                    + self.message_object_type.name
                    + "_"
                    + self.message_related_type.name
                )
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
    def message_subtype_name(self):
        """The name of the message sub type, derives from the message properties
        Example: SubActionType.UPDATE, MessageObjectType.USER,
        RelationshipType.MANAGER -> UPDATE_USER_MANAGER
        Override where behavior differs"""
        if (
            self.message_subaction_type
            and self.message_object_type
            and self.message_relationship_type
        ):
            if (
                self.message_related_type
                and self.message_related_type != addresser.address_space.ObjectType.USER
            ):
                return (
                    self.message_subaction_type.name
                    + "_"
                    + self.message_object_type.name
                    + "_"
                    + self.message_related_type.name
                )
            return (
                self.message_subaction_type.name
                + "_"
                + self.message_object_type.name
                + "_"
                + self.message_relationship_type.name
            )
        return None

    @property
    def message_type(self):
        """The message type of this message, an attribute enum of RBACPayload
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
        if not hasattr(
            protobuf, self.message_object_type.name.lower() + "_transaction_pb2"
        ):
            raise AttributeError(
                "Could not find protobuf.{}_transaction_pb2".format(
                    self.message_object_type.name.lower()
                )
            )
        if not hasattr(
            getattr(
                protobuf, self.message_object_type.name.lower() + "_transaction_pb2"
            ),
            self._camel_case(self.message_type_name),
        ):
            raise AttributeError(
                "Could not find protobuf.{}_transaction_pb2.{}".format(
                    self.message_object_type.name.lower(),
                    self._camel_case(self.message_type_name),
                )
            )
        return getattr(
            getattr(
                protobuf, self.message_object_type.name.lower() + "_transaction_pb2"
            ),
            self._camel_case(self.message_type_name),
        )

    @property
    def proposal_type(self):
        """The type of the proposal (if any) implemented by this message"""
        if not hasattr(protobuf.proposal_state_pb2.Proposal, self.message_subtype_name):
            raise AttributeError(
                "Could not find protobuf.proposal_state_pb2.Proposal.{}".format(
                    self.message_subtype_name
                )
            )
        return getattr(protobuf.proposal_state_pb2.Proposal, self.message_subtype_name)

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on its state object"""
        return []

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
        and store the resulting data of a successful or failed execution.
        Messages will override this method and add all the input/output
        addresses they require to read and write to."""
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))
        if not isinstance(signer_keypair, Key):
            raise TypeError(
                "Expected signer_keypair to be a key, not {}".format(
                    type(signer_keypair)
                )
            )

        user_key_address = addresser.user.address(object_id=signer_keypair.public_key)
        key_address = addresser.key.address(object_id=signer_keypair.public_key)
        inputs = {user_key_address, key_address}
        outputs = set({})
        return inputs, outputs

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

    # pylint: disable=unused-argument
    def validate_state(self, context, message, inputs, input_state, store, signer):
        """Common state validation for all messages"""
        if signer is None:
            raise ValueError("Signer is required")
        if message is None:
            raise ValueError("Message is required")
        if not isinstance(inputs, list) and not isinstance(inputs, set):
            raise ValueError("Inputs is required and expected to be a list or a set")
        if not isinstance(input_state, dict):
            raise ValueError("Input state was expected to be a dictionary")
        if not isinstance(signer, str) and PUBLIC_KEY_PATTERN.match(signer):
            raise TypeError("Expected signer to be a public key")
        if context is None:
            raise ValueError("State context is required")

    def validate_signer(self, message, inputs, input_state, signer):
        """Validates the transaction signer has a valid key"""
        key_address = addresser.key.address(object_id=signer)
        if key_address not in inputs:
            LOGGER.warning("Signer key address was not included in inputs")
        if (
            key_address in inputs
            and key_address not in input_state
            and not self.allow_signer_not_in_state
        ):
            raise ValueError("Signer key not found in state")

    def make_payload(self, message, signer_keypair):
        """Make a payload for the given message type"""
        self.validate(message=message, signer=signer_keypair)

        message_type = self.message_type
        inputs, outputs = self.make_addresses(
            message=message, signer_keypair=signer_keypair
        )
        inputs = set(inputs)
        outputs = set(outputs)

        if signer_keypair:
            inputs.add(addresser.user.address(object_id=signer_keypair.public_key))

        if not outputs.issubset(inputs):
            raise ValueError(
                "{} output addresses {} not contained in inputs".format(
                    self.message_type_name,
                    addresser.parse_addresses(outputs.difference(inputs)),
                )
            )

        return batcher.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )

    def batch(self, signer_keypair, batch=None, **kwargs):
        """Adds a new message to an existing or new batch"""
        message = kwargs.get("message")
        if not message:
            message = self.make(**kwargs)
        else:
            self.validate(message=message, signer=signer_keypair)
        payload = self.make_payload(message=message, signer_keypair=signer_keypair)
        transaction, new_batch, _, _ = batcher.make(
            payload=payload, signer_keypair=signer_keypair
        )
        if batch:
            batch.transactions.extend([transaction])
            return batch
        return new_batch

    def batch_list(self, signer_keypair, batch_list=None, **kwargs):
        """Adds a new message to an existing or new batch list"""
        message = kwargs.get("message")
        if not message:
            message = self.make(**kwargs)
        else:
            self.validate(message=message, signer=signer_keypair)
        payload = self.make_payload(message=message, signer_keypair=signer_keypair)
        _, new_batch, new_batch_list, _ = batcher.make(
            payload=payload, signer_keypair=signer_keypair
        )
        if batch_list:
            batch_list.batches.extend([new_batch])
            return batch_list
        return new_batch_list

    def unmake_payload(self, payload):
        """Unmake the payload for the given message type"""
        message_type = self.message_type
        # pylint: disable=not-callable
        message = self.message_proto()
        message.ParseFromString(payload.content)
        inputs = set(list(payload.inputs))
        outputs = set(list(payload.outputs))
        return message, message_type, inputs, outputs

    def new(self, signer_keypair, **kwargs):
        """Creates and send a message to the blockchain"""
        message = kwargs.get("message")
        if not message:
            message = self.make(**kwargs)
        else:
            self.validate(message=message, signer=signer_keypair)
        return self.send(
            signer_keypair=signer_keypair,
            payload=self.make_payload(message=message, signer_keypair=signer_keypair),
        )

    def send(self, signer_keypair, payload):
        """Sends a payload to the validator API"""
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")
        if not isinstance(payload, protobuf.rbac_payload_pb2.RBACPayload):
            raise TypeError("Expected payload to be an RBACPayload")

        _, _, batch_list, _ = batcher.make(
            payload=payload, signer_keypair=signer_keypair
        )
        status = client.send_batches_get_status(batch_list=batch_list)
        return status

    def get(self, object_id, related_id=None):
        """Gets an address from the blockchain from the validator API"""
        address = self.address(object_id=object_id, related_id=related_id)
        # pylint: disable=not-callable
        container = self._state_container()
        container.ParseFromString(client.get_address(address=address))
        return self._find_in_state_container(
            container=container,
            address=address,
            object_id=object_id,
            related_id=related_id,
        )

    def get_addresses(self, context, addresses):
        """Get the deserialized state entries given a list of blockchain addresses"""
        state_entries = {}
        records = state_client.get_addresses(context=context, addresses=addresses)
        if not records:
            return state_entries
        for record in records:
            state_entries[record.address] = addresser.deserialize(
                address=record.address, data=record.data
            )
        return state_entries

    def _make_output_state(self, input_state, outputs):
        """Makes the output state entries from the input state and
        adds the addresses that were not in state"""
        output_state = {"changed": set()}
        inputs_to_outputs = [address for address in outputs if address in input_state]
        for address in inputs_to_outputs:
            output_state[address] = input_state[address]
        return output_state

    def message_to_storage(self, message):
        """Transforms the message into the state (storage) object"""
        return batcher.message_to_message(
            # pylint: disable=not-callable
            message_to=self._state_object(),
            message_from=message,
            message_name=self._name_camel,
            exclude_fields=self.message_fields_not_in_state,
        )

    def set_state(self, context, message, outputs, object_id, related_id=None):
        """Creates a new address in the blockchain state"""
        store = self.message_to_storage(message=message)
        # pylint: disable=no-member,not-callable
        container = self._state_container()
        getattr(container, self._state_container_list_name).extend([store])
        address = self.address(object_id=object_id, related_id=related_id)
        if address not in outputs:
            raise ValueError(
                "Address {} not in listed outputs".format(addresser.parse(address))
            )
        state_client.set_address(context=context, address=address, container=container)

    def _get_store(self, object_id, related_id, outputs, output_state):
        """Gets the store object to store data for this message"""
        address = self.address(object_id=object_id, related_id=related_id)
        container = None
        if address not in outputs and address in output_state:
            raise ValueError(
                "Address {} not in listed outputs".format(addresser.parse(address))
            )
        if address in output_state:
            container = output_state[address]
            # TODO: is getting the first item in the container... may not be correct!
            store = getattr(container, self._state_container_list_name)[0]
        if not container:
            container, store = self._get_new_state()
            output_state[address] = container
        return store

    def _update_store(
        self, object_id, related_id, message, store, outputs, output_state, signer
    ):
        """Update the output state entries for the given address using
        the data the given message"""
        address = self.address(object_id=object_id, related_id=related_id)
        self.store_message(
            object_id=object_id,
            related_id=related_id,
            store=store,
            message=message,
            outputs=outputs,
            output_state=output_state,
            signer=signer,
        )
        output_state["changed"].add(address)

    # pylint: disable=unused-argument
    def store_message(
        self, object_id, related_id, store, message, outputs, output_state, signer
    ):
        """Copies a message to the state object, excluding properties
        listed in message_fields_not_in_state property. This provides
        a simple default behavior for cases where this is appropriate;
        commonly override this method in message classes"""
        batcher.message_to_message(
            message_to=store,
            message_from=message,
            message_name=self._name_camel,
            exclude_fields=self.message_fields_not_in_state,
        )

    def save_state(self, context, output_state):
        """Save the output state to the blockchain"""
        changed = [
            address
            for address in output_state.keys()
            if address in output_state["changed"]
        ]
        entries = {}
        for address in changed:
            entries[address] = output_state[address].SerializeToString()
        state_client.set_state(context=context, entries=entries)

    def apply_update(
        self, message, object_id, related_id, outputs, output_state, signer
    ):
        """Apply additional state changes (if any)
        Message implementation will override this method if there
        is data to be stored in any other address"""
        pass

    @property
    def allow_signer_not_in_state(self):
        """Whether the signer of the message is allowed to not be
        in state. Used only for when the transaction also creates the
        signer of the message (e.g. CREATE_USER)"""
        return False

    def authenticate_state(self, message, inputs, input_state, signer):
        """Check to see if the signer of the transaction is
        eligible to perform the action"""
        signer_address = addresser.user.address(object_id=signer)
        key_address = addresser.key.address(object_id=signer)
        if signer_address not in inputs:
            raise ValueError(
                "{}: address {} for signer's public key {} was not sent as an input address".format(
                    self._name_title, signer_address, signer
                )
            )
        if not self.allow_signer_not_in_state and signer_address not in input_state:
            raise ValueError(
                "{}: address {} for signer's public key {} was not found in state".format(
                    self._name_title, signer_address, signer
                )
            )

    def apply(self, header, payload, context):
        """Handles a message in the transaction processor"""
        # pylint: disable=not-callable
        message, _, inputs, outputs = self.unmake_payload(payload=payload)
        signer = header.signer_public_key
        object_id = self._get_object_id(item=message)
        related_id = self._get_related_id(item=message)

        self.validate(message=message, signer=signer)
        input_state = self.get_addresses(context=context, addresses=inputs)
        output_state = self._make_output_state(input_state=input_state, outputs=outputs)

        self.authenticate_state(
            message=message, inputs=inputs, input_state=input_state, signer=signer
        )
        store = self._get_store(
            object_id=object_id,
            related_id=related_id,
            outputs=outputs,
            output_state=output_state,
        )
        self.validate_state(
            context=context,
            message=message,
            inputs=inputs,
            input_state=input_state,
            store=store,
            signer=signer,
        )
        self._update_store(
            object_id=object_id,
            related_id=related_id,
            message=message,
            store=store,
            outputs=outputs,
            output_state=output_state,
            signer=signer,
        )
        self.apply_update(
            message=message,
            object_id=object_id,
            related_id=related_id,
            outputs=outputs,
            output_state=output_state,
            signer=signer,
        )
        self.save_state(context=context, output_state=output_state)
