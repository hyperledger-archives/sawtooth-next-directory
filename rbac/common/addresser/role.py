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
from rbac.common.base.base_address import AddressBase
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.address_space import ObjectType
from rbac.common.addresser.address_space import RelationshipType
from rbac.common.addresser.family import family


class RoleOwnerAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self, family=family)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_OWNERS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.OWNER

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_role_owners_address(role_id=object_id, user_id=target_id)

        return self._address(object_id=object_id, target_id=target_id)


class RoleAdminAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self, family=family)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_ADMINS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.ADMIN

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_role_admins_address(role_id=object_id, user_id=target_id)

        return self._address(object_id=object_id, target_id=target_id)


class RoleMemberAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self, family=family)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_MEMBERS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.MEMBER

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_role_members_address(
                role_id=object_id, user_id=target_id
            )

        return self._address(object_id=object_id, target_id=target_id)


class RoleTaskAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self, family=family)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_TASKS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.TASK

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.MEMBER

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_role_tasks_address(role_id=object_id, task_id=target_id)

        return self._address(object_id=object_id, target_id=target_id)


class RoleAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self, family=family)
        self.owner = RoleOwnerAddress()
        self.admin = RoleAdminAddress()
        self.member = RoleMemberAddress()
        self.task = RoleTaskAddress()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_ATTRIBUTES

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.SELF

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.ATTRIBUTES

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_role_attributes_address(role_id=object_id)

        return self._address(object_id=object_id, target_id=target_id)

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


# pylint: disable=invalid-name
role = RoleAddress()

__all__ = ["role"]
