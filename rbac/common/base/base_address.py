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

import os
from hashlib import sha512
from rbac.legacy import addresser as legacy
from rbac.common.addresser.address_space import AddressSpace


class AddressBase:
    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        raise NotImplementedError("Class must implement this method")

    def address(self, object_id, target_id):
        """Makes a blockchain address of this address type"""
        raise NotImplementedError("Class must implement this method")

    def address_is(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class or a child class, otherewise returns None"""
        return self._address_is(address)

    def _address_is(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class, otherwise returns None"""
        address_type = AddressSpace[legacy.address_is(address=address).name]
        if address_type == self.address_type:
            return self.address_type
        return None

    def unique_id(self, length=16):
        """Generates cryptographically strong random hexidecimal string"""
        return os.urandom(length).hex()

    def hash(self, value, length=60):
        """Returns a variable length hash of the given string"""
        return sha512(value.encode()).hexdigest()[:length]
