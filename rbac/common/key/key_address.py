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
"""Addresses and accesses user objects on the blockchain"""
# pylint: disable=unused-import

from rbac.common import addresser
from rbac.common.base.base_address import AddressBase
from rbac.common.protobuf import key_state_pb2
from rbac.common.protobuf import key_transaction_pb2


class KeyAddress(AddressBase):
    """Addresses public key objects on the blockchain"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.KEY

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.KEY

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.NONE

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.NONE


KEY_ADDRESS = KeyAddress()

__all__ = ["KEY_ADDRESS"]
