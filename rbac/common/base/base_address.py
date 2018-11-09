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
import os
import re as regex
from hashlib import sha512
from rbac.legacy import addresser as legacy
from rbac.common.addresser.address_space import AddressSpace

LOGGER = logging.getLogger(__name__)

PATTERN_ZERO_BYTE = r"00"
PATTERN_12_HEX_BYTES = r"[0-9a-f]{24}"
PATTERN_12_BYTE_HASH = regex.compile(r"^" + PATTERN_12_HEX_BYTES + r"$")


class AddressBase:
    def __init__(self, family):
        """The Role Based Access Control (RBAC) Transaction Family"""
        self._family = family
        self._pattern = regex.compile(
            r"^"
            + self._family.namespace
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
        address = (
            self._family.namespace
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
    def pattern(self):
        """A regular expression that matches only addresses of this address type"""
        return self._pattern

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        return self._address(object_id=object_id, target_id=target_id)

    def address_is(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class or a child class, otherewise returns None"""
        return self._address_is(address=address)

    def _address_is(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class, otherewise returns None"""
        if self._family.version == "1.0":
            return self._legacy_address_is(address=address)

        if self._pattern.match(address):
            return self.address_type
        return None

    def _legacy_address_is(self, address):
        """Temporary support for legacy (version 1.0) addressing scheme"""
        address_type = AddressSpace[legacy.address_is(address=address).name]
        if address_type == self.address_type:
            return self.address_type
        return None

    def unique_id(self):
        """Generates a random 12-byte hexidecimal string"""
        return os.urandom(12).hex()

    def hash(self, value):
        """Returns a 12-byte hash of a given string, unless it is already a
        12-byte hexadecimal string (e.g. as returned by the unique_id function).
        Returns zero bytes if the value is None or falsey"""
        if not value:
            return PATTERN_ZERO_BYTE * 12
        if PATTERN_12_BYTE_HASH.match(value):
            return value
        return sha512(value.encode()).hexdigest()[:24]
