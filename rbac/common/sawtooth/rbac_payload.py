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
"""RBAC Payload is a protobuf that is used to encapsulate all messages
sent to the RBAC Sawtooth validator / transaction processor
"""

# pylint: disable=no-member
import time
import logging
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf.rbac_payload_pb2 import Signer

LOGGER = logging.getLogger(__name__)
MESSAGE_NAMES = RBACPayload.MessageType.DESCRIPTOR.values_by_name.items()


class MessagePayload:
    """ The decoded message payload wrapper information
    """

    def __init__(self, message_type, inputs, outputs, signer, now):
        self._message_type = message_type
        self._message_type_name = get_message_type_name(message_type)
        self._inputs = inputs
        self._outputs = outputs
        self._signer = signer
        self._now = now

    @property
    def message_type(self):
        """ The type of the message (enum from the payload protobuf) """
        return self._message_type

    @property
    def message_type_name(self):
        """ The text name of the message type """
        return self._message_type_name

    @property
    def inputs(self):
        """ The input addresses sent with the message """
        return self._inputs

    @property
    def outputs(self):
        """ The output addresses sent with the message """
        return self._outputs

    @property
    def signer(self):
        """ The signer of the message (user_id, public_key) """
        return self._signer

    @property
    def now(self):
        """ The time the message was created, approximately now
            This is passed to message methods can access the current time,
            which is otherwise can't be safely accessed (not deterministic)
        """
        return self._now


def get_message_type_name(message_type):
    """returns the protobuf enum name from the value
    """
    for (key, descriptor) in MESSAGE_NAMES:
        if descriptor.index == message_type:
            return key
    return None


def make_signer(user_id, public_key):
    """Make a signer object
    """
    return Signer(user_id=user_id, public_key=public_key)


def make_payload(message, message_type, inputs, outputs, signer):
    """Make a payload from a message and its attributes
    """
    return RBACPayload(
        content=message.SerializeToString(),
        message_type=message_type,
        inputs=inputs,
        outputs=outputs,
        signer=signer,
        now=int(time.time()),
    )


def get_proto(message_type):
    """Attempts to get the protobuf associated with a message type
    given the message type name. Can find most protobufs via
    this method. Used only for testing purposes by unmake.
    """
    name = get_message_type_name(message_type)
    name_parts = name.split("_")
    try:
        if len(name_parts) >= 4:
            # e.g. PROPOSE_REMOVE_ROLE_ADMIN -> role
            object_type = name_parts[2].lower()
        else:
            # e.g. CREATE_USER -> user
            object_type = name_parts[1].lower()

        proto = getattr(
            getattr(protobuf, object_type + "_transaction_pb2"),
            name.title().replace("_", ""),  # camel case the message type name
        )
        return proto()
    except Exception:
        raise Exception(
            "get_proto couldn't discover the protobuf for message type {}".format(name)
        )
    return None


def unmake_payload(payload):
    """Turn a payload back into a message given it's message type
    Use only for testing purposes.
    """
    if isinstance(payload, bytes):
        decoded = RBACPayload()
        decoded.ParseFromString(payload)
        payload = decoded
    if not isinstance(payload, RBACPayload):
        raise Exception("Expected RBACPayload")
    if not isinstance(payload.content, bytes):
        raise Exception("Expected RBACPayload, no content found")

    message_type = payload.message_type
    message = get_proto(message_type)
    message.ParseFromString(payload.content)

    message_payload = MessagePayload(
        message_type=message_type,
        inputs=set(list(payload.inputs)),
        outputs=set(list(payload.outputs)),
        signer=payload.signer,
        now=payload.now,
    )

    return message, message_payload
