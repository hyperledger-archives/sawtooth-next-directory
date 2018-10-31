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

import logging

from rbac.addressing import addresser
from rbac.common import protobuf
from rbac.common.manager.base_relationship import BaseRelationship
from rbac.common.role.propose_task import ProposeAddRoleTask
from rbac.common.role.confirm_task import ConfirmAddRoleTask
from rbac.common.role.reject_task import RejectAddRoleTask

LOGGER = logging.getLogger(__name__)


class TaskRelationship(BaseRelationship):
    def __init__(self):
        BaseRelationship.__init__(self)
        self.propose = ProposeAddRoleTask()
        self.confirm = ConfirmAddRoleTask()
        self.reject = RejectAddRoleTask()

    @property
    def name(self):
        return "role"

    @property
    def container_proto(self):
        return protobuf.role_state_pb2.RoleRelationshipContainer

    def address(self, object_id, target_id):
        return addresser.make_role_tasks_address(object_id, target_id)
