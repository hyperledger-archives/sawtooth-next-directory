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
"""Base Relationship acts as a common base class for all
relationship classes. It is able to access state relationship
information."""
import logging

from rbac.common import protobuf
from rbac.common.sawtooth import client
from rbac.common.base.base_address import AddressBase

LOGGER = logging.getLogger(__name__)


class BaseRelationship(AddressBase):
    """Base class for object relationship classes
    This handles common blockchain state access and manipulation"""

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
            self._name_camel + "RelationshipContainer",
        ):
            raise AttributeError(
                "Could not find protobuf.{}_state_pb2.{}Container".format(
                    self._name_lower, self._state_container_prefix
                )
            )
        return getattr(
            getattr(protobuf, self._name_lower + "_state_pb2"),
            self._name_camel + "RelationshipContainer",
        )

    def exists(self, object_id, target_id):
        """Check the existence of a relationship record"""
        # pylint: disable=not-callable
        container = self._state_container()
        address = self.address(object_id=object_id, target_id=target_id)
        container.ParseFromString(client.get_address(address=address))
        items = list(container.relationships)
        if not items:
            return False
        if len(items) > 1:
            LOGGER.warning(
                "%s %s relationship container for %s %s at address %s has more than one record",
                self.object_type.name.title(),
                object_id,
                self.related_type.name.lower(),
                target_id,
                address,
            )
        item = items[0]
        identifiers = list(item.identifiers)
        if not identifiers:
            LOGGER.warning(
                "%s %s relationship container for user %s %s at address %s has no identifiers",
                self.object_type.name.title(),
                object_id,
                self.related_type.name.lower(),
                target_id,
                address,
            )
            return False
        if len(identifiers) > 1:
            LOGGER.warning(
                "%s %s relationship container for user %s %s at address %s has more than one identifier",
                self.object_type.name.title(),
                object_id,
                self.related_type.name.lower(),
                target_id,
                address,
            )
        return bool(target_id in item.identifiers)
