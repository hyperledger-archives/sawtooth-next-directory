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


class UserAssertions(BatchAssertions):
    def __init__(self, *args, **kwargs):
        BatchAssertions.__init__(self, *args, **kwargs)

    def assertValidPayload(self, payload, message, message_type):
        """Test a payload is valid given a user related message type"""
        check_message_type, check_message, check_inputs, check_outputs = unmake_payload(
            payload
        )
        self.assertEqual(check_message_type, message_type)
        if message_type == RBACPayload.CREATE_USER:
            self.assertIsInstance(
                check_message, protobuf.user_transaction_pb2.CreateUser
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
