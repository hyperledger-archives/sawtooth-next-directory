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
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common import protobuf

LOGGER = logging.getLogger(__name__)


def make_payload(message, message_type, inputs, outputs):
    """Make a payload from a message and its attributes"""
    return RBACPayload(
        content=message.SerializeToString(),
        message_type=message_type,
        inputs=inputs,
        outputs=outputs,
    )


def unmake_payload(payload):
    """Turn a payload back into a message given it's message type"""
    if isinstance(payload, bytes):
        decoded = RBACPayload()
        decoded.ParseFromString(payload)
        payload = decoded
    if not isinstance(payload, RBACPayload):
        raise Exception("Expected RBACPayload")
    if not isinstance(payload.content, bytes):
        raise Exception("Expected RBACPayload, no content found")
    message_type = payload.message_type
    message = None
    inputs = list(payload.inputs)
    outputs = list(payload.outputs)
    if message_type == RBACPayload.CREATE_USER:
        message = protobuf.user_transaction_pb2.CreateUser()
    elif message_type == RBACPayload.CREATE_ROLE:
        message = protobuf.role_transaction_pb2.CreateRole()
    elif message_type == RBACPayload.PROPOSE_ADD_ROLE_MEMBERS:
        message = protobuf.role_transaction_pb2.ProposeAddRoleMember()
    elif message_type == RBACPayload.PROPOSE_ADD_ROLE_OWNERS:
        message = protobuf.role_transaction_pb2.ProposeAddRoleOwner()
    elif message_type == RBACPayload.PROPOSE_ADD_ROLE_ADMINS:
        message = protobuf.role_transaction_pb2.ProposeAddRoleAdmin()
    else:
        raise Exception(
            "unmake_payload doesn't support message type {}".format(message_type)
        )
    message.ParseFromString(payload.content)
    return message_type, message, inputs, outputs
