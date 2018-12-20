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
"""Implements the User library: rbac.user.*"""
# pylint: disable=too-few-public-methods

import logging
from rbac.common.user.create_user import CreateUser
from rbac.common.user.propose_manager import ProposeUpdateUserManager
from rbac.common.user.confirm_manager import ConfirmUpdateUserManager
from rbac.common.user.reject_manager import RejectUpdateUserManager
from rbac.common.user.imports_user import ImportsUser
from rbac.common.user.user_address import UserManagerAddress
from rbac.common.user.user_address import UserDirectReportAddress
from rbac.common.user.user_address import UserEmailAddress
from rbac.common.user.user_address import UserKeyAddress

LOGGER = logging.getLogger(__name__)


class Manager(UserManagerAddress):
    """Implements the User Manager library: rbac.user.manager.*"""

    def __init__(self):
        super().__init__()
        self.propose = ProposeUpdateUserManager()
        self.confirm = ConfirmUpdateUserManager()
        self.reject = RejectUpdateUserManager()


class User(CreateUser):
    """Implements the User library: rbac.user.*"""

    def __init__(self):
        CreateUser.__init__(self)
        self.manager = Manager()
        self.imports = ImportsUser()
        self.email = UserEmailAddress()
        self.key = UserKeyAddress()
        self.direct_report = UserDirectReportAddress()


USER = User()

__all__ = ["USER"]
