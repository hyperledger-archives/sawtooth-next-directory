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
from rbac.common.task.create_task import CreateTask

from rbac.common.task.relationship_owner import OwnerRelationship
from rbac.common.task.relationship_admin import AdminRelationship

LOGGER = logging.getLogger(__name__)


class TaskManager(CreateTask):
    def __init__(self):
        CreateTask.__init__(self)
        self.owner = OwnerRelationship()
        self.admin = AdminRelationship()
