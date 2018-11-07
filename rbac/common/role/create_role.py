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


class CreateRole(BaseMessage):
    def __init__(self):
        BaseMessage.__init__(self)

    @property
    def name(self):
        return "role"

    @property
    def names(self):
        return self.name + "_attributes"

    @property
    def message_type(self):
        # pylint: disable=no-member
        return RBACPayload.CREATE_ROLE

    @property
    def message_proto(self):
        return protobuf.role_transaction_pb2.CreateRole

    @property
    def container_proto(self):
        return protobuf.role_state_pb2.RoleAttributesContainer

    @property
    def state_proto(self):
        # pylint: disable=no-member
        return protobuf.role_state_pb2.Role

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on the state object"""
        return ["owners", "admins"]

    def address(self, object_id, target_id=None):
        """Make an address for the given role_id"""
        return addresser.role.address(object_id)

    # pylint: disable=arguments-differ, not-callable
    def make(self, role_id, name, metadata=None, owners=None, admins=None):
        """Make a message"""
        return self.message_proto(
            role_id=role_id, name=name, metadata=metadata, owners=owners, admins=admins
        )

    def make_addresses(self, message, signer_keypair=None):
        """Makes the appropriate inputs & output addresses for the message type"""
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))

        inputs = [
            # addresser.sysadmin.member.address(signer_public_key),
            addresser.role.address(message.role_id)
        ]
        inputs.extend([addresser.user.address(u) for u in message.admins])
        inputs.extend([addresser.user.address(u) for u in message.owners])
        inputs.extend(
            [addresser.role.admin.address(message.role_id, a) for a in message.admins]
        )
        inputs.extend(
            [addresser.role.owner.address(message.role_id, o) for o in message.owners]
        )
        outputs = inputs
        return inputs, outputs
