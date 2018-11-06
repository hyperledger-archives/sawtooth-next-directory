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

from rbac.legacy import addresser as legacy
from rbac.common.addresser.address_base import AddressBase
from rbac.common.addresser.address_space import AddressSpace


class RoleOwnerAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_OWNERS

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        return legacy.make_role_owners_address(role_id=object_id, user_id=target_id)


class RoleAdminAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_ADMINS

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        return legacy.make_role_admins_address(role_id=object_id, user_id=target_id)


class RoleMemberAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_MEMBERS

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        return legacy.make_role_members_address(role_id=object_id, user_id=target_id)


class RoleTaskAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_TASKS

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        return legacy.make_role_tasks_address(role_id=object_id, task_id=target_id)


class RoleAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)
        self.owner = RoleOwnerAddress()
        self.admin = RoleAdminAddress()
        self.member = RoleMemberAddress()
        self.task = RoleTaskAddress()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_ATTRIBUTES

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        return legacy.make_role_attributes_address(role_id=object_id)

    def address_is(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class or a child class, otherewise returns None"""
        return (
            self._address_is(address=address)
            or self.owner.address_is(address=address)
            or self.admin.address_is(address=address)
            or self.member.address_is(address=address)
            or self.task.address_is(address=address)
        )


role = RoleAddress()

__all__ = ["role"]
