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
"""Test the Sawtooth REST client"""

# pylint: disable=too-many-branches

import logging
from base64 import b64decode
import pytest

from rbac.common import addresser
from rbac.common.sawtooth import client
from rbac.common.protobuf import proposal_state_pb2
from rbac.common.protobuf import role_state_pb2
from rbac.common.protobuf import task_state_pb2
from rbac.common.protobuf import user_state_pb2
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.integration
@pytest.mark.client_sync
class TestRestClient(TestAssertions):
    """Test the Sawtooth REST client"""

    @pytest.mark.state
    @pytest.mark.skip("too expensive if large chain, refactor elsewhere")
    def test_state(self):
        """Grab the entire blockchain state and deserialize it"""
        subtree = addresser.family.namespace
        for item in client.list_state(subtree=subtree)["data"]:
            address_type = item["address_type"] = addresser.get_address_type(
                item["address"]
            )
            if address_type == addresser.AddressSpace.USER:
                content = user_state_pb2.UserContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.PROPOSALS:
                content = proposal_state_pb2.ProposalsContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.SYSADMIN_ATTRIBUTES:
                content = "SYSADMIN_ATTRIBUTES"
            elif address_type == addresser.AddressSpace.SYSADMIN_MEMBERS:
                content = "SYSADMIN_MEMBERS"
            elif address_type == addresser.AddressSpace.SYSADMIN_OWNERS:
                content = "SYSADMIN_OWNERS"
            elif address_type == addresser.AddressSpace.SYSADMIN_ADMINS:
                content = "SYSADMIN_ADMINS"
            elif address_type == addresser.AddressSpace.ROLES_ATTRIBUTES:
                content = role_state_pb2.RoleAttributesContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.ROLES_MEMBERS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.ROLES_OWNERS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.ROLES_ADMINS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.ROLES_TASKS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.TASKS_ATTRIBUTES:
                content = task_state_pb2.TaskAttributesContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.TASKS_OWNERS:
                content = task_state_pb2.TaskRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == addresser.AddressSpace.TASKS_ADMINS:
                content = task_state_pb2.TaskRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            else:
                content = "ERROR: unknown type: {}".format(address_type)

            LOGGER.debug("%-80s%-30s%s", item["address"], address_type, content)
