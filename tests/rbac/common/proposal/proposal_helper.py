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
"""Proposal test helper"""
# pylint: disable=no-member,too-few-public-methods,invalid-name

import random

from rbac.common import rbac
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class ProposalTestHelper:
    """Proposal test helper"""

    def id(self):
        """Get a test proposal_id (not created)"""
        return rbac.addresser.proposal.unique_id()

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))
