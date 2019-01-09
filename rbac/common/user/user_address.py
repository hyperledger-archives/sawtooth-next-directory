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
from rbac.common.base.base_relationship import BaseRelationship
from rbac.common.protobuf import user_state_pb2
from rbac.common.protobuf import user_transaction_pb2


class UserEmailAddress(BaseRelationship):
    """Addresses user email objects on the blockchain"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER_EMAIL

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.EMAIL

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.OWNER


class UserKeyAddress(BaseRelationship):
    """Addresses user key objects on the blockchain"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER_KEY

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.KEY

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.OWNER


class UserManagerAddress(BaseRelationship):
    """Addresses user manager relationships on the blockchain"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER_MANAGER

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.MANAGER


class UserDirectReportAddress(BaseRelationship):
    """Addresses user direct report relationships on the blockchain"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER_DIRECT_REPORT

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.DIRECT_REPORT


class UserAddress(AddressBase):
    """Addresses user objects on the blockchain"""

    def __init__(self):
        super().__init__()
        self._register()
        self.email = UserEmailAddress()
        self.key = UserKeyAddress()
        self.manager = UserManagerAddress()
        self.direct_report = UserDirectReportAddress()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.NONE

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES


USER_ADDRESS = UserAddress()

__all__ = ["USER_ADDRESS"]
