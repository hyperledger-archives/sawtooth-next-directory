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

from rbac.common.crypto.keys import Key
from rbac.addressing.addresser import make_user_address
from rbac.transaction_creation.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.transaction_creation.protobuf import user_transaction_pb2

LOGGER = logging.getLogger(__name__)


class TestData:
    def get_test_inputs(self, message_type=RBACPayload.CREATE_USER):
        if message_type == RBACPayload.CREATE_USER:
            signer = Key()
            message = user_transaction_pb2.CreateUser(name="foobar")
            message.user_id = signer.public_key
            inputs = [make_user_address(signer.public_key)]
            outputs = inputs
            return message, message_type, inputs, outputs, signer
        else:
            raise Exception(
                "get_test_payload doesn't yet support {}".format(message_type)
            )
