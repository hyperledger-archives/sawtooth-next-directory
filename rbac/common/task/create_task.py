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
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class CreateTask(BaseMessage):
    def __init__(self):
        BaseMessage.__init__(self)

    @property
    def name(self):
        return "task"

    @property
    def names(self):
        return self.name + "_attributes"

    @property
    def message_type(self):
        # pylint: disable=no-member
        return RBACPayload.CREATE_TASK

    @property
    def message_proto(self):
        return protobuf.task_transaction_pb2.CreateTask

    @property
    def container_proto(self):
        return protobuf.task_state_pb2.TaskAttributesContainer

    @property
    def state_proto(self):
        # pylint: disable=no-member
        return protobuf.task_state_pb2.Task

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on the state object"""
        return ["owners", "admins"]

    def address(self, object_id, target_id=None):
        """Make an address for the given task_id"""
        return addresser.task.address(object_id)

    # pylint: disable=arguments-differ, not-callable
    def make(self, task_id, name, metadata=None, owners=None, admins=None):
        """Make a message"""
        return self.message_proto(
            task_id=task_id, name=name, metadata=metadata, owners=owners, admins=admins
        )

    def make_addresses(self, message, signer_keypair=None):
        """Makes the appropriate inputs & output addresses for the message type"""
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))

        inputs = [
            # addresser.sysadmin.member.address(signer_public_key),
            addresser.task.address(message.task_id)
        ]
        inputs.extend([addresser.user.address(u) for u in message.admins])
        inputs.extend([addresser.user.address(u) for u in message.owners])
        inputs.extend(
            [addresser.task.admin.address(message.task_id, a) for a in message.admins]
        )
        inputs.extend(
            [addresser.task.owner.address(message.task_id, o) for o in message.owners]
        )
        outputs = inputs
        return inputs, outputs
