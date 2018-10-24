# Copyright contributors to Hyperledger Sawtooth
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
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.sawtooth.rbac_payload import unmake_payload
from tests.rbac.common.sawtooth.batch_assertions import BatchAssertions

LOGGER = logging.getLogger(__name__)


class RoleAssertions(BatchAssertions):
    def __init__(self, *args, **kwargs):
        BatchAssertions.__init__(self, *args, **kwargs)

    def assertValidPayload(self, payload, message, message_type):
        """Check that a payload is valid given its message type"""
        check_message_type, check_message, check_inputs, check_outputs = unmake_payload(
            payload
        )
        self.assertEqual(check_message_type, message_type)
        if message_type == RBACPayload.CREATE_ROLE:
            self.assertIsInstance(
                check_message, protobuf.role_transaction_pb2.CreateRole
            )
        elif message_type == RBACPayload.PROPOSE_ADD_ROLE_MEMBERS:
            self.assertIsInstance(
                check_message, protobuf.role_transaction_pb2.ProposeAddRoleMember
            )
        elif message_type == RBACPayload.PROPOSE_ADD_ROLE_OWNERS:
            self.assertIsInstance(
                check_message, protobuf.role_transaction_pb2.ProposeAddRoleOwner
            )
        elif message_type == RBACPayload.PROPOSE_ADD_ROLE_ADMINS:
            self.assertIsInstance(
                check_message, protobuf.role_transaction_pb2.ProposeAddRoleAdmin
            )
        else:
            raise Exception(
                "UserAssertions.assertValidPayload doesn't support message type {}".format(
                    message_type
                )
            )
        self.assertEqualMessage(check_message, message)
        self.assertIsInstance(check_inputs, list)
        self.assertIsInstance(check_outputs, list)
        inputs, outputs = self.make_addresses(message=message)
        self.assertEqual(check_inputs, inputs)
        self.assertEqual(check_outputs, outputs)

    def assertCreateRoleResult(self, message, result):
        """Check the result of a Create Role matches the message"""
        self.assertIsInstance(result.role_id, str)
        self.assertIsInstance(result.name, str)
        self.assertEqual(message.role_id, result.role_id)
        self.assertEqual(message.name, result.name)
