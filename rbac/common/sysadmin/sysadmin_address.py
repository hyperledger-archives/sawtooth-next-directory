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
"""Addresses and accesses sysadmin objects on the blockchain"""
# pylint: disable=unused-import

from rbac.common import addresser
from rbac.common.base.base_address import AddressBase


class SysAdminOwnerAddress(AddressBase):
    """Addresses and accesses the sysadmin owner relationship"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.SYSADMIN_OWNERS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SYSADMIN

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.OWNER


class SysAdminAdminAddress(AddressBase):
    """Addresses and accesses the sysadmin admin relationship"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.SYSADMIN_ADMINS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SYSADMIN

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ADMIN


class SysAdminMemberAddress(AddressBase):
    """Addresses and accesses the sysadmin member relationship"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.SYSADMIN_MEMBERS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SYSADMIN

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.MEMBER


class SysAdminAddress(AddressBase):
    """Addresses and accesses sysadmin objects on the blockchain"""

    def __init__(self):
        super().__init__()
        self._register()
        self.owner = SysAdminOwnerAddress()
        self.admin = SysAdminAdminAddress()
        self.member = SysAdminMemberAddress()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.SYSADMIN_ATTRIBUTES

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SYSADMIN

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.NONE

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES

    def address(self, object_id=None, related_id=None):
        """Makes a blockchain address of this address type
        (sysadmin has no object_id, there is only one sysadmin role)"""
        return self._address(object_id=object_id, related_id=related_id)


SYSADMIN_ADDRESS = SysAdminAddress()

__all__ = ["SYSADMIN_ADDRESS"]
