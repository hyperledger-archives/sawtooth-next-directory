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
"""Implements the Task library: rbac.task.*"""
# pylint: disable=too-few-public-methods

from rbac.common.task.create_task import CreateTask

from rbac.common.task.relationship_owner import OwnerRelationship
from rbac.common.task.relationship_admin import AdminRelationship
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class Task(CreateTask):
    """Implements the Task library: rbac.task.*"""

    def __init__(self):
        CreateTask.__init__(self)
        self.owner = OwnerRelationship()
        self.admin = AdminRelationship()


TASK = Task()

__all__ = ["TASK"]
