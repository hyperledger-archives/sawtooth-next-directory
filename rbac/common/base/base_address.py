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

LOGGER = logging.getLogger(__name__)

PATTERN_ZERO_BYTE = r"00"
PATTERN_12_HEX_BYTES = r"[0-9a-f]{24}"
PATTERN_12_BYTE_HASH = regex.compile(r"^" + PATTERN_12_HEX_BYTES + r"$")


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

    def _address(self, object_id, target_id):
        """Makes an address using the address scheme"""
        address = (
            family.namespace
            + PATTERN_ZERO_BYTE * 2
            + hex(self.object_type.value)[2:].zfill(4)
            + self.hash(object_id)
            + hex(self.related_type.value)[2:].zfill(4)
            + hex(self.relationship_type.value)[2:].zfill(2)
            + self.hash(target_id)
            + PATTERN_ZERO_BYTE
        )
        return address

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

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        return self._address(object_id=object_id, target_id=target_id)

    def get_address_type(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class or a child class, otherewise returns None"""
        return self.address_is(address=address)

    def address_is(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class, otherewise returns None"""
        if self._pattern.match(address):
            return self.address_type
        return None

    def addresses_are(self, addresses):
        """Determines if all addresses given are of the classes' address type"""
        # pylint: disable=unnecessary-lambda
        return all(map(lambda a: self.address_is(a), addresses))
