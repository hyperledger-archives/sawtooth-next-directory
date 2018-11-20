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
import logging

from rbac.common import protobuf
from rbac.common.crypto.hash import unique_id, hash_id
from rbac.common.sawtooth import state_client
from rbac.common.util import get_attribute

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
        """The identifier field name for the object type
        Example: ObjectType.USER -> 'user_id'
        Override where behavior deviates from this norm"""
        return self._name_lower + "_id"

    @property
    def _name_upper_plural(self):
        """The upppercase plural name of the object type
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
        """The upppercase plural name of the object type
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
            getattr(protobuf, self._name_lower + "_state_pb2"), self._name_camel
        ):
            raise AttributeError(
                "Could not find protobuf.{}_state_pb2.{}".format(
                    self._name_lower, self._name_camel
                )
            )
        return getattr(
            getattr(protobuf, self._name_lower + "_state_pb2"), self._name_camel
        )

    @property
    def _state_container_name_plural(self):
        """Whether the state container name is plural
        Default False, override where differs"""
        return False

    @property
    def _state_container_prefix(self):
        """The 'User' in protobuf.user_state_pb2.UserContainer
        Defaults to self._name_camel, override where differs from this norm"""
        return self._name_camel

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

    @property
    def _state_container_list_name(self):
        """The state container (protobuf) used by this object type
        Derives name of the protobuf class from the object type name
        Example: if protobuf.user_state_pb2.UserContainer.users
            ObjectType.USER -> users
        Override where behavior differs from this norm"""
        return self._name_lower_plural

    def unique_id(self):
        """Generates a random 12-byte hexidecimal string
        Override where desired behavior differs"""
        return unique_id()

    def hash(self, value):
        """Returns a 12-byte hash of a given string, unless it is already a
        12-byte hexadecimal string (e.g. as returned by the unique_id function).
        Returns zero bytes if the value is None or falsey
        Override where desired behavior differs"""
        return hash_id(value)

    def address(self, object_id, target_id):
        """Makes an address for the given state object"""
        raise NotImplementedError("Class must implement this method")

    def _get_object_id(self, item):
        """Find the object_id attribute value on an object
        Prefers object_id over specific IDs like user_id"""
        if hasattr(item, "object_id"):
            return getattr(item, "object_id")
        if hasattr(item, self._name_id):
            return getattr(item, self._name_id)
        return None

    def _get_target_id(self, item):
        """Find the target_id attribute value on an object"""
        return get_attribute(item, "target_id")

    def _find_in_state_container(self, container, address, object_id, target_id=None):
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
                target_id,
                address,
            )
        for item in items:
            if (
                object_id == self._get_object_id(item)
                and target_id == self._get_target_id(item)
            ) or (object_id == self._get_object_id(item) and target_id is None):
                return item
        LOGGER.warning(
            "%s not found in container for %s target %s at address %s\n%s",
            self._name_title,
            object_id,
            target_id,
            address,
            container,
        )
        return None

    def get_from_state(self, state, object_id, target_id=None):
        """Gets an address from the blockchain state
        (state object is available when message is handled by transaction processor)"""
        address = self.address(object_id=object_id, target_id=target_id)
        # pylint: disable=not-callable
        container = self._state_container()

        results = state_client.get_address(state=state, address=address)
        if not list(results):
            return None

        container.ParseFromString(results[0].data)
        return self._find_in_state_container(
            container=container,
            address=address,
            object_id=object_id,
            target_id=target_id,
        )

    def address_exists(self, state, object_id, target_id=None):
        """Checks to see if an address already exists on the blockchain
        for a given object or object relationship
        (state object is available when message is handled by transaction processor)"""
        address = self.address(object_id=object_id, target_id=target_id)
        results = state_client.get_address(state=state, address=address)
        if not list(results):
            return False
        return True

    def exists_in_state(self, state, object_id, target_id=None, fast_check=False):
        """Checks an object exists in the blockchain
        fast_check False will see if the object really exists and isn't a hash collission
        fast_check True will only check to see the address exists (generally sufficient)
        (state object is available when message is handled by transaction processor)"""
        if fast_check:  # check address exists only, not contents of address
            return self.address_exists(
                state=state, object_id=object_id, target_id=target_id
            )

        result = self.get_from_state(
            state=state, object_id=object_id, target_id=target_id
        )
        return bool(result is not None)
