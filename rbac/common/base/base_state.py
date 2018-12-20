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
"""Base State handles accessing blockchain state information.
It is a common base class for both Base Address and Base Message classes.

From the object_type name, it is able to infer information about how
the object is stored on the blockchain: the state and container protubufs,
and the unique identifier name"""
# pylint: disable=too-many-public-methods

import logging

from rbac.common import protobuf
from rbac.common.crypto.hash import unique_id, hash_id
from rbac.common.sawtooth import batcher
from rbac.common.sawtooth import state_client

LOGGER = logging.getLogger(__name__)


class StateBase:
    """Base class for both the address and message base classes
    This handles common blockchain state access and manipulation"""

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        raise NotImplementedError("Class must implement this property")

    @property
    def _is_plural(self):
        """Whether the name is already plural
        Default to False, override to True when plural"""
        return False

    @property
    def _name_upper(self):
        """The lowercase name of the object type
        Example: ObjectType.USER -> 'USER'
        """
        return self.object_type.name.upper()

    @property
    def _name_lower(self):
        """The lowercase name of the object type
        Example: ObjectType.USER -> 'user'
        """
        return self.object_type.name.lower()

    @property
    def _name_title(self):
        """The title case name of the object type
        Example: ObjectType.USER -> 'User'
        Example: ObjectType.ROLE_ATTRIBUTE -> 'Role_Attribute'
        """
        return self.object_type.name.title()

    def _camel_case(self, value):
        """Make a string camel case
        Example: ROLE_ATTRIBUTE -> RoleAttribute"""
        return value.title().replace(" ", "").replace("_", "")

    @property
    def _name_camel(self):
        """The camel case name of the object type
        Example: ObjectType.USER -> 'User'
        Example: ObjectType.ROLE_ATTRIBUTE -> 'RoleAttribute'
        """
        return self._camel_case(self.object_type.name)

    @property
    def _name_id(self):
        """The attribute name for the object type
        Example: ObjectType.USER -> 'user_id'
        Override where behavior deviates from this norm"""
        return self._name_lower + "_id"

    @property
    def _related_id(self):
        """The attribute name for the related_id if not related_id"""
        return "related_id"

    @property
    def _name_upper_plural(self):
        """The uppercase plural name of the object type
        Example: ObjectType.USER -> 'USERS'
        Override for irregular grammar"""
        if self._is_plural:
            return self._name_upper
        return self._name_upper + "s"

    @property
    def _name_lower_plural(self):
        """The lowercase plural name of the object type
        Example: ObjectType.USER -> 'users'
        Override for irregular grammar"""
        if self._is_plural:
            return self._name_lower
        return self._name_lower + "s"

    @property
    def _name_title_plural(self):
        """The uppercase plural name of the object type
        Example: ObjectType.USER -> 'Users'
        Override for irregular grammar"""
        if self._is_plural:
            return self._name_title
        return self._name_title + "s"

    @property
    def _name_camel_plural(self):
        """The lowercase plural name of the object type
        Example: ObjectType.ROLE_ATTRIBUTE -> 'RoleAttributes'
        Override for irregular grammar"""
        if self._is_plural:
            return self._name_camel
        return self._name_camel + "s"

    @property
    def _state_object_name(self):
        """The name of the state object on the state protobuf
        The 'User' in protobuf.user_state_pb2.User
        Defaults to self._name_camel, override where differs from this norm"""
        return self._name_camel

    @property
    def _state_container_prefix(self):
        """The 'User' in protobuf.user_state_pb2.UserContainer
        Defaults to self._state_object_name, override where differs from this norm"""
        return self._state_object_name

    @property
    def _state_container_list_name(self):
        """The name of the state collection on the state container protobuf
        The 'users' in protobuf.user_state_pb2.UserContainer.users
        Defaults to self._name_lower_plural, override where differs from this norm"""
        return self._name_lower_plural

    @property
    def _state_object(self):
        """The state object (protobuf) used by this object type
        Derives name of the protobuf class from the object type name
        Example: ObjectType.USER -> protobuf.user_state_pb2.User
        Override where behavior differs from this norm"""
        if not hasattr(protobuf, self._name_lower + "_state_pb2"):
            raise AttributeError(
                "Could not find protobuf.{}_state_pb2".format(self._name_lower)
            )
        if not hasattr(
            getattr(protobuf, self._name_lower + "_state_pb2"), self._state_object_name
        ):
            raise AttributeError(
                "Could not find protobuf.{}_state_pb2.{}".format(
                    self._name_lower, self._state_object_name
                )
            )
        return getattr(
            getattr(protobuf, self._name_lower + "_state_pb2"), self._state_object_name
        )

    @property
    def _state_container(self):
        """The state container (protobuf) used by this object type
        Derives name of the protobuf class from the object type name
        Example: ObjectType.USER -> protobuf.user_state_pb2.UserContainer
        Override where behavior differs from this norm"""
        if not hasattr(protobuf, self._name_lower + "_state_pb2"):
            raise AttributeError(
                "Could not find protobuf.{}_state_pb2".format(self._name_lower)
            )
        if not hasattr(
            getattr(protobuf, self._name_lower + "_state_pb2"),
            self._state_container_prefix + "Container",
        ):
            raise AttributeError(
                "Could not find protobuf.{}_state_pb2.{}Container".format(
                    self._name_lower, self._state_container_prefix
                )
            )
        return getattr(
            getattr(protobuf, self._name_lower + "_state_pb2"),
            self._state_container_prefix + "Container",
        )

    def unique_id(self):
        """Generates a random 12-byte hexadecimal string
        Override where desired behavior differs"""
        return unique_id()

    def hash(self, value):
        """Returns a 12-byte hash of a given string lowercased, unless it is already a
        12-byte hexadecimal string (e.g. as returned by the unique_id function).
        Returns zero bytes if the value is None or falsey
        Override where desired behavior differs"""
        return hash_id(value)

    def address(self, object_id, related_id):
        """Makes an address for the given state object"""
        raise NotImplementedError("Class must implement this method")

    def parse(self, address):
        """Returns the components of an address if the address if of the address type
        implemented by this class or a child class, otherwise returns None"""
        raise NotImplementedError("Class must implement this method")

    def _get_object_id(self, item):
        """Find the object_id attribute value on an object
        Prefers object_id over specific IDs like user_id"""
        if hasattr(item, "object_id"):
            return getattr(item, "object_id")
        if hasattr(item, self._name_id):
            return getattr(item, self._name_id)
        return None

    def _get_related_id(self, item):
        """Find the related_id attribute value on an object
        Prefers related_id over specific IDs like user_id"""
        if hasattr(item, "related_id"):
            return getattr(item, "related_id")
        if self._related_id != "related_id" and hasattr(item, self._related_id):
            return getattr(item, self._related_id)
        return None

    def _find_in_state_container(self, container, address, object_id, related_id=None):
        """Finds the state_object within a given state_container for the
        object type implemented by this class; returns None if not found"""
        items = list(getattr(container, self._state_container_list_name))
        if not items:
            return None
        if len(items) > 1:
            LOGGER.warning(
                "%s container for %s target %s has more than one record at address %s",
                self._name_title,
                object_id,
                related_id,
                address,
            )
        for item in items:
            if (
                object_id == self._get_object_id(item)
                and related_id == self._get_related_id(item)
            ) or (object_id == self._get_object_id(item) and related_id is None):
                return item
        LOGGER.warning(
            "%s not found in container for %s target %s at address %s\n%s",
            self._name_title,
            object_id,
            related_id,
            address,
            container,
        )
        return None

    def deserialize(self, address, data):
        """Deserialize the data of a blockchain address"""
        # pylint: disable=not-callable
        try:
            container = self._state_container()
            container.ParseFromString(data)
            return container
        except Exception:  # pylint: disable=broad-except
            LOGGER.warning(
                "%s data at address %s could not be deserialized \n%s",
                self._name_title,
                address,
                data,
            )
            return None

    def deserialize_list(self, address, data):
        """Deserialize the data of a blockchain address and return the store list"""
        # pylint: disable=not-callable
        try:
            container = self._state_container()
            container.ParseFromString(data)
            return list(getattr(container, self._state_container_list_name))
        except Exception:  # pylint: disable=broad-except
            LOGGER.warning(
                "%s data at address %s could not be deserialized \n%s",
                self._name_title,
                address,
                data,
            )
            return None

    def get_address(self, context, address):
        """Get the deserialized data of a blockchain address"""
        data = state_client.get_address(context=context, address=address)
        if data:
            return self.deserialize(address=address, data=data)
        return None

    def get_addresses(self, context, addresses):
        """Get the list of blockchain addresses"""
        return state_client.get_addresses(context=context, addresses=addresses)

    def get_from_state_context(self, context, object_id, related_id=None):
        """Gets an address from the blockchain state"""
        address = self.address(object_id=object_id, related_id=related_id)
        container = self.get_address(context=context, address=address)
        if container:
            return self._find_in_state_container(
                container=container,
                address=address,
                object_id=object_id,
                related_id=related_id,
            )
        return None

    def _get_new_state(self):
        """Returns a new state container (protobuf) with a single store object"""
        # pylint: disable=not-callable
        container = self._state_container()
        getattr(container, self._state_container_list_name).extend(
            [self._state_object()]
        )
        store = getattr(container, self._state_container_list_name)[0]
        return container, store

    def get_from_input_state(self, inputs, input_state, object_id, related_id=None):
        """Get an address from the transaction input state"""
        address = self.address(object_id=object_id, related_id=related_id)
        if address not in inputs:
            raise ValueError(
                "{} address {} for {} {} target {} was not sent as an input address".format(
                    self.parse(address).address_type,
                    address,
                    self._name_id,
                    object_id,
                    related_id,
                )
            )
        if address not in input_state:
            return None
        container = input_state[address]
        if container:
            return self._find_in_state_container(
                container=container,
                address=address,
                object_id=object_id,
                related_id=related_id,
            )
        return None

    def get_from_output_state(self, outputs, output_state, object_id, related_id=None):
        """Get an address from the transaction output state"""
        address = self.address(object_id=object_id, related_id=related_id)
        if address not in outputs:
            raise ValueError(
                "{} address {} for {} {} target {} was not sent as an output address".format(
                    self._name_title, address, self._name_id, object_id, related_id
                )
            )
        if address not in output_state:
            raise ValueError(
                "{} address {} for {} {} target {} was not in output state".format(
                    self._name_title, address, self._name_id, object_id, related_id
                )
            )
        container = output_state[address]
        if not container:
            raise ValueError(
                "{} address {} for {} {} target {} had no container in output state".format(
                    self._name_title, address, self._name_id, object_id, related_id
                )
            )
        return self._find_in_state_container(
            container=container,
            address=address,
            object_id=object_id,
            related_id=related_id,
        )

    def store(self, message, outputs, output_state, object_id, related_id=None):
        """Copies a dictionary or message to the state object of this address"""
        address = self.address(object_id=object_id, related_id=related_id)
        if address not in outputs:
            raise ValueError(
                "{} address {} for {} {} target {} was not sent as an output address".format(
                    self._name_title, address, self._name_id, object_id, related_id
                )
            )
        if address in output_state:
            container = output_state[address]
            store = self._find_in_state_container(
                container=container,
                address=address,
                object_id=object_id,
                related_id=related_id,
            )
            if not store:
                raise ValueError(
                    "{} store for {} {} target {} was not found in container".format(
                        self._name_title, self._name_id, object_id, related_id
                    )
                )
        else:
            container, store = self._get_new_state()
            output_state[address] = container

        batcher.message_to_message(
            message_to=store, message_from=message, message_name=self._name_camel
        )
        output_state["changed"].add(address)

    def set_output_state_attribute(
        self, name, value, outputs, output_state, object_id, related_id=None
    ):
        """Sets an attribute in the state store object"""
        address = self.address(object_id=object_id, related_id=related_id)
        store = self.get_from_output_state(
            outputs=outputs,
            output_state=output_state,
            object_id=object_id,
            related_id=related_id,
        )
        if not store:
            raise ValueError(
                "set_output_state_attribute error: {} address {} for {} {} target {} had no store object in output state".format(
                    self._name_title, address, self._name_id, object_id, related_id
                )
            )
        if not hasattr(store, name):
            raise KeyError(
                "{} address {} for {} {} target {} store has no attribute '{}'".format(
                    self._name_title,
                    address,
                    self._name_id,
                    object_id,
                    related_id,
                    name,
                )
            )
        setattr(store, name, value)
        output_state["changed"].add(address)

    def address_exists(self, context, object_id, related_id=None):
        """Checks to see if an address already exists on the blockchain
        for a given object or object relationship"""
        address = self.address(object_id=object_id, related_id=related_id)
        content = state_client.get_address(context=context, address=address)
        if content is None:
            return False
        return True

    def exists_in_state(self, context, object_id, related_id=None, fast_check=False):
        """Checks an object exists in the blockchain
        fast_check False will see if the object really exists and isn't a hash collision
        fast_check True will only check to see the address exists (generally sufficient)"""
        if fast_check:  # check address exists only, not contents of address
            return self.address_exists(
                context=context, object_id=object_id, related_id=related_id
            )

        result = self.get_from_state_context(
            context=context, object_id=object_id, related_id=related_id
        )
        return bool(result is not None)

    def exists_in_inputs(self, inputs, object_id, related_id=None):
        """Check an address exists in transaction inputs"""
        address = self.address(object_id=object_id, related_id=related_id)
        return bool(address in inputs)

    def exists_in_outputs(self, outputs, object_id, related_id=None):
        """Check an address exists in transaction outputs"""
        address = self.address(object_id=object_id, related_id=related_id)
        return bool(address in outputs)

    def exists_in_state_inputs(
        self,
        inputs,
        input_state,
        object_id,
        related_id=None,
        skip_if_not_in_inputs=False,
    ):
        """Check an object exists in the blockchain via inputs and input_state
        input_state is the result of a state query on addresses=inputs"""
        address = self.address(object_id=object_id, related_id=related_id)
        if address not in inputs:
            if skip_if_not_in_inputs:
                return True
            raise ValueError(
                "{} address {} for {} {} target {} was not sent as an input address".format(
                    self.parse(address).address_type,
                    address,
                    self._name_id,
                    object_id,
                    related_id,
                )
            )
        return bool(address in input_state)

    def exist_in_state(self, context, object_ids, related_id=None, fast_check=False):
        """Checks that all the object ids passed in object_list exist in the blockchain
        fast_check False will see if the object really exists and isn't a hash collission
        fast_check True will only check to see the address exists (generally sufficient)"""
        exists = [
            self.exists_in_state(
                context=context,
                object_id=object_id,
                related_id=related_id,
                fast_check=fast_check,
            )
            for object_id in object_ids
        ]
        all_exist = all(exists)
        not_found = []
        if not all_exist:
            not_found = [
                object_id for object_id, found in zip(object_ids, exists) if not found
            ]
        return all_exist, not_found

    def create_relationship(self, object_id, related_id, outputs, output_state):
        """Creates a relationship record in the output state for a transaction
        (Legacy relationship format)"""
        address = self.address(object_id=object_id, related_id=related_id)
        if address not in outputs:
            raise ValueError(
                "address {} for was not included in outputs".format(
                    self.parse(address=address)
                )
            )
        # pylint: disable=not-callable
        container = self._state_container()
        store = self._state_object()
        if hasattr(store, "object_id"):
            store.object_id = object_id
        if hasattr(store, "related_id"):
            store.related_id = related_id
        if self._name_id != "object_id" and hasattr(store, self._name_id):
            setattr(store, self._name_id, object_id)
        if hasattr(store, "identifiers"):
            store.identifiers.append(related_id)
        container = self._state_container()
        getattr(container, self._state_container_list_name).extend([store])
        output_state[address] = container
        output_state["changed"].add(address)
