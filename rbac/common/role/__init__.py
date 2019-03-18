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
"""Implements the Role library: rbac.role.*"""

# pylint: disable=too-few-public-methods

from rbac.common.role.create_role import CreateRole
from rbac.common.role.relationship_member import MemberRelationship

from rbac.common.role.relationship_owner import OwnerRelationship
from rbac.common.role.relationship_admin import AdminRelationship
from rbac.common.role.relationship_task import TaskRelationship
from rbac.common.role.imports_role import ImportsRole
from rbac.common.role.update_role import UpdateRole
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class Role(CreateRole):
    """Implements the Role library: rbac.role.*"""

    def __init__(self):
        CreateRole.__init__(self)
        self.member = MemberRelationship()
        self.owner = OwnerRelationship()
        self.admin = AdminRelationship()
        self.task = TaskRelationship()
        self.imports = ImportsRole()
        self.update = UpdateRole()


ROLE = Role()

__all__ = ["ROLE"]
