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
from base64 import b64decode
import pytest

from rbac.common.crypto.keys import Key
from rbac.addressing import addresser
from rbac.addressing.addresser import AddressSpace
from rbac.addressing.addresser import make_user_address
from rbac.common.sawtooth.client_sync import ClientSync
from tests.rbac.common.sawtooth.batch_assertions import BatchAssertions
from tests.rbac.common.sawtooth.test_data import TestData
from rbac.transaction_creation.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.transaction_creation.protobuf import user_transaction_pb2
from rbac.processor.protobuf import proposal_state_pb2
from rbac.processor.protobuf import role_state_pb2
from rbac.processor.protobuf import task_state_pb2
from rbac.processor.protobuf import user_state_pb2

LOGGER = logging.getLogger(__name__)


@pytest.mark.integration
@pytest.mark.client_sync
class TestRestClient(BatchAssertions, ClientSync, TestData):
    def __init__(self, *args, **kwargs):
        BatchAssertions.__init__(self, *args, **kwargs)
        ClientSync.__init__(self)

    @pytest.mark.skip("skip me")
    def test_send_batches_get_status(self):
        self.assertTrue(callable(self.send_batches_get_status))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        batch_list = self.batch_to_list(
            batch=self.make_batch(
                transaction=self.make_transaction(
                    message=message,
                    message_type=message_type,
                    inputs=inputs,
                    outputs=outputs,
                    signer_keypair=signer,
                )
            )
        )
        status = self.send_batches_get_status(batch_list=batch_list)
        LOGGER.debug("status %s", status)

    @pytest.mark.skip("skip me")
    def test_create_user_no_user_id(self):
        self.assertTrue(callable(self.send_batches_get_status))

        signer = Key()
        message_type = RBACPayload.CREATE_USER
        message = user_transaction_pb2.CreateUser(name="foobar")
        # message.user_id = signer.public_key
        inputs = [make_user_address(signer.public_key)]
        outputs = inputs

        batch_list = self.batch_to_list(
            batch=self.make_batch(
                transaction=self.make_transaction(
                    message=message,
                    message_type=message_type,
                    inputs=inputs,
                    outputs=outputs,
                    signer_keypair=signer,
                    batcher_public_key=signer.public_key,
                ),
                batcher_keypair=signer,
            )
        )
        status = self.send_batches_get_status(batch_list=batch_list)
        LOGGER.debug("status %s", status)

    @pytest.mark.state
    @pytest.mark.skip("too expensive if large chain, refactor elsewhere")
    def test_state(self):
        subtree = addresser.NS
        for item in self._client.list_state(subtree=subtree)["data"]:
            address_type = item["address_type"] = addresser.address_is(item["address"])
            if address_type == AddressSpace.USER:
                content = user_state_pb2.UserContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.PROPOSALS:
                content = proposal_state_pb2.ProposalsContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.SYSADMIN_ATTRIBUTES:
                content = "SYSADMIN_ATTRIBUTES"
            elif address_type == AddressSpace.SYSADMIN_MEMBERS:
                content = "SYSADMIN_MEMBERS"
            elif address_type == AddressSpace.SYSADMIN_OWNERS:
                content = "SYSADMIN_OWNERS"
            elif address_type == AddressSpace.SYSADMIN_ADMINS:
                content = "SYSADMIN_ADMINS"
            elif address_type == AddressSpace.ROLES_ATTRIBUTES:
                content = role_state_pb2.RoleAttributesContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.ROLES_MEMBERS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.ROLES_OWNERS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.ROLES_ADMINS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.ROLES_TASKS:
                content = role_state_pb2.RoleRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.TASKS_ATTRIBUTES:
                content = task_state_pb2.TaskAttributesContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.TASKS_OWNERS:
                content = task_state_pb2.TaskRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            elif address_type == AddressSpace.TASKS_ADMINS:
                content = task_state_pb2.TaskRelationshipContainer()
                content.ParseFromString(b64decode(item["data"]))
            else:
                content = "ERROR: unknown type: {}".format(address_type)

            LOGGER.debug("%-80s%-30s%s", item["address"], address_type, content)
