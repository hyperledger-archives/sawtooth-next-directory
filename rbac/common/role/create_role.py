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
"""Implements the CREATE_ROLE message
usage: rbac.role.create()"""

import logging
from rbac.common import addresser
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.address_space import ObjectType
from rbac.common.addresser.address_space import RelationshipType
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class CreateRole(BaseMessage):
    """Implements the CREATE_ROLE message
    usage: rbac.role.create()"""

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.CREATE

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLE

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.SELF

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.ATTRIBUTES

    @property
    def _state_container_prefix(self):
        """Roles state container name contains Attributes (RoleAttributesContainer)"""
        return self._name_camel + "Attributes"

    @property
    def _state_container_list_name(self):
        """Roles state container collection name contains _attributes (role_attributes)"""
        return self._name_lower + "_attributes"

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on the state object"""
        return ["owners", "admins"]

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
