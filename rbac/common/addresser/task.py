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
from rbac.common.addresser.family import family


class TaskOwnerAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.TASKS_OWNERS

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_task_owners_address(task_id=object_id, user_id=target_id)

        return legacy.make_task_owners_address(task_id=object_id, user_id=target_id)


class TaskAdminAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.TASKS_ADMINS

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_task_admins_address(task_id=object_id, user_id=target_id)

        return legacy.make_task_admins_address(task_id=object_id, user_id=target_id)


class TaskAddress(AddressBase):
    def __init__(self):
        AddressBase.__init__(self)
        self.owner = TaskOwnerAddress()
        self.admin = TaskAdminAddress()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.TASKS_ATTRIBUTES

    def address(self, object_id, target_id=None):
        """Makes a blockchain address of this address type"""
        if family.version == "1.0":
            return legacy.make_task_attributes_address(task_id=object_id)

        return legacy.make_task_attributes_address(task_id=object_id)

    def address_is(self, address):
        """Returns the address type if the address is of the address type
        implemented by this class or a child class, otherewise returns None"""
        return (
            self._address_is(address=address)
            or self.owner.address_is(address=address)
            or self.admin.address_is(address=address)
        )


# pylint: disable=invalid-name
task = TaskAddress()

__all__ = ["task"]
