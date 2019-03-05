# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Implementation of the Role-Task relationship
Usage: rbac.role.task.exists(role_id, task_id)
"""

from rbac.common import addresser
from rbac.common.base.base_relationship import BaseRelationship
from rbac.common.role.propose_task import ProposeAddRoleTask
from rbac.common.role.confirm_task import ConfirmAddRoleTask
from rbac.common.role.reject_task import RejectAddRoleTask
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class TaskRelationship(BaseRelationship):
    """Implementation of the Role-Task relationship
    Usage: rbac.role.task.exists(role_id, task_id)
    """

    def __init__(self):
        super().__init__()
        self.propose = ProposeAddRoleTask()
        self.confirm = ConfirmAddRoleTask()
        self.reject = RejectAddRoleTask()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.ROLES_TASKS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.TASK

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.MEMBER
