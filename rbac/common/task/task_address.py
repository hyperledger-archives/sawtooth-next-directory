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
"""Addresses and accesses task objects on the blockchain"""
from rbac.common import addresser
from rbac.common.base.base_address import AddressBase


class TaskOwnerAddress(AddressBase):
    """Addresses and accesses the role owner relationship"""

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.TASKS_OWNERS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.TASK

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.OWNER


class TaskAdminAddress(AddressBase):
    """Addresses and accesses the role admin relationship"""

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.TASKS_ADMINS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.TASK

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ADMIN


class TaskAddress(AddressBase):
    """Addresses and accesses task objects on the blockchain"""

    def __init__(self):
        AddressBase.__init__(self)
        self.owner = TaskOwnerAddress()
        self.admin = TaskAdminAddress()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.TASKS_ATTRIBUTES

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.TASK

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SELF

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES

    @property
    def _state_container_prefix(self):
        """Tasks state container name contains Attributes (TaskAttributesContainer)"""
        return self._name_camel + "Attributes"

    def get_address_type(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class or a child class, otherewise returns None"""
        return (
            self.address_is(address=address)
            or self.owner.get_address_type(address=address)
            or self.admin.get_address_type(address=address)
        )


TASK_ADDRESS = TaskAddress()

__all__ = ["TASK_ADDRESS"]
