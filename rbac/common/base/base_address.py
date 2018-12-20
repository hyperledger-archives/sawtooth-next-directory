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
"""The Address Base class is the base for all address classes.
It addresses information on the blockchain using three enumeration
fields: object_type, related_type and relationship_type; combined
with the hash of the object_id and the related_id (if any)."""
import logging
import re as regex
from rbac.common.addresser.family_address import family
from rbac.common.base.base_state import StateBase
from rbac.common.addresser.addressers import register_addresser

LOGGER = logging.getLogger(__name__)

PATTERN_ZERO_BYTE = r"00"
PATTERN_12_HEX_BYTES = r"[0-9a-f]{24}"
PATTERN_12_BYTE_HASH = regex.compile(r"^" + PATTERN_12_HEX_BYTES + r"$")


class Address:
    """The values of a specific address"""

    def __init__(
        self,
        address,
        address_type,
        object_type,
        object_id,
        related_type,
        relationship_type,
        related_id,
    ):
        self._address = address
        self._address_type = address_type
        self._object_type = object_type
        self._object_id = object_id
        self._related_type = related_type
        self._relationship_type = relationship_type
        self._related_id = related_id

    @property
    def address(self):
        """The address"""
        return self._address

    @property
    def address_type(self):
        """The address type of this address"""
        return self._address_type

    @property
    def object_type(self):
        """The object type of this address"""
        return self._object_type

    @property
    def object_id(self):
        """The hash of an object_id (or the object_id itself
        if it is a 12-byte unique identifier)"""
        return self._object_id

    @property
    def related_type(self):
        """The related type of this address"""
        return self._related_type

    @property
    def relationship_type(self):
        """The relationship type of this address"""
        return self._relationship_type

    @property
    def related_id(self):
        """The hash of a related_id (the related_id
        itself if it is a 12-byte unique identifier)
        None if no related_id."""
        return self._related_id

    def __repr__(self):
        """Return a string representation of the object"""
        return str(
            {
                "address": self.address,
                "address_type": self.address_type.name,
                "object_type": self.object_type.name,
                "object_id": self.object_id,
                "related_type": self.related_type.name,
                "relationship_type": self.relationship_type.name,
                "related_id": self.related_id,
            }
        )


class AddressBase(StateBase):
    """Address is a 35-byte (70 character) lowercase hexadecimal string
        in the following format:
            3-bytes (6 characters): Transaction Family Namespace
            2-bytes (4 characters): Reserved (zero bytes)
            2-bytes (4 characters): Hex representation of the object type (enum value)
            12-bytes (24 characters): Hash of the object id
            2-bytes (4 characters): Hex representation of the related object type (enum value)
            1-byte (2 characters): Hex representation of the relationship type (enum value)
            12-bytes (24 characters): Hash of the related object id or zero bytes if None
            1-byte (2 characters): Reserved (zero bytes)
        """

    def __init__(self):
        """The regular expression pattern of addresses matching the address scheme"""
        StateBase.__init__(self)
        self._pattern = regex.compile(
            r"^"
            + family.namespace
            + PATTERN_ZERO_BYTE * 2
            + hex(self.object_type.value)[2:].zfill(4)
            + PATTERN_12_HEX_BYTES
            + hex(self.related_type.value)[2:].zfill(4)
            + hex(self.relationship_type.value)[2:].zfill(2)
            + PATTERN_12_HEX_BYTES
            + PATTERN_ZERO_BYTE
            + r"$"
        )

    def _address(self, object_id, related_id):
        """Makes an address using the address scheme"""
        address = (
            family.namespace
            + PATTERN_ZERO_BYTE * 2
            + hex(self.object_type.value)[2:].zfill(4)
            + self.hash(object_id)
            + hex(self.related_type.value)[2:].zfill(4)
            + hex(self.relationship_type.value)[2:].zfill(2)
            + self.hash(related_id)
            + PATTERN_ZERO_BYTE
        )
        return address

    def parse(self, address):
        """Returns the components of an address if the address if of the address type
        implemented by this class or a child class, otherwise returns None"""
        if self._pattern.match(address):
            return Address(
                address=address,
                address_type=self.address_type,
                object_type=self.object_type,
                object_id=self.get_object_id(address=address),
                related_type=self.related_type,
                relationship_type=self.relationship_type,
                related_id=self.get_related_id(address=address),
            )
        return None

    def _register(self):
        """Registers the class as the authoritative addresser for this address type"""
        register_addresser(self)

    @property
    def _family(self):
        """The transaction family implemented by this class"""
        return family

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
    def address_type_name(self):
        """Returns a unique name for this addresser based on the combination
        of the properties object_type + related_type + relationship_type"""
        return (
            self.object_type.name
            + "_"
            + self.related_type.name
            + "_"
            + self.relationship_type.name
        )

    def address(self, object_id, related_id=None):
        """Makes a blockchain address of this address type"""
        return self._address(object_id=object_id, related_id=related_id)

    def addresses_are(self, addresses):
        """Determines if all addresses given are of the classes' address type"""
        return all([self.get_address_type(a) for a in addresses])

    def get_address_type(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class, otherwise returns None"""
        if self._pattern.match(address):
            return self.address_type
        return None

    def get_addresser(self, address):
        """Returns the self if the address is of the address type
        implemented by this class, otherwise returns None"""
        if self._pattern.match(address):
            return self
        return None

    def get_object_id(self, address):
        """Returns the hash of an object_id (or the object_id itself if it
        is a 12-byte unique identifier), as encoded in a given address"""
        return address[14:38]

    def get_related_id(self, address):
        """Returns the hash of a related_id (or the related_id itself if it
        is a 12-byte unique identifier), as encoded in a given address"""
        value = address[44:68]
        if value == PATTERN_ZERO_BYTE * 12:
            return None
        return value

    def deserialize(self, address, data):
        """Returns the deserialized content if the address is of the address type
        implemented by this class or a child class, otherwise returns None"""
        if self._pattern.match(address):
            return super().deserialize(address=address, data=data)
        return None

    def deserialize_list(self, address, data):
        """Returns the deserialized content if the address is of the address type
        implemented by this class or a child class, otherwise returns None"""
        if self._pattern.match(address):
            return super().deserialize_list(address=address, data=data)
        return None
