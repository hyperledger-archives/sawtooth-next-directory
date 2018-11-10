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

from rbac.common import addresser

from rbac.common.user.user_manager import UserManager
from rbac.common.role.role_manager import RoleManager
from rbac.common.task.task_manager import TaskManager

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class RBACManager:
    def __init__(self):
        self.addresser = addresser
        self.user = UserManager()
        self.role = RoleManager()
        self.task = TaskManager()
