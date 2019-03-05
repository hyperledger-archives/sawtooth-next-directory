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
"""Implementation of the Role-Admin relationship
Usage: rbac.role.admin.exists(role_id, user_id)
"""

from rbac.common import addresser
from rbac.common.base.base_relationship import BaseRelationship
from rbac.common.role.propose_admin import ProposeAddRoleAdmin
from rbac.common.role.confirm_admin import ConfirmAddRoleAdmin
from rbac.common.role.reject_admin import RejectAddRoleAdmin
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class AdminRelationship(BaseRelationship):
    """Implementation of the Role-Admin relationship
    Usage: rbac.role.admin.exists(role_id, user_id)
    """

    def __init__(self):
        super().__init__()
        self.propose = ProposeAddRoleAdmin()
        self.confirm = ConfirmAddRoleAdmin()
        self.reject = RejectAddRoleAdmin()

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.ROLES_ADMINS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ADMIN
