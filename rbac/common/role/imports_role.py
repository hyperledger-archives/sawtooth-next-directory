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
"""Implements the IMPORTS_ROLE message
usage: rbac.role.import.create()"""

import logging
from rbac.common import addresser
from rbac.common.protobuf import role_transaction_pb2  # pylint: disable=unused-import
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.address_space import ObjectType
from rbac.common.addresser.address_space import RelationshipType
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class ImportsRole(BaseMessage):
    """Implements the IMPORTS_ROLE message
    usage: rbac.role.imports.create()"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.IMPORTS

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.ROLES_ATTRIBUTES

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.ROLE

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.NONE

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.ATTRIBUTES

    @property
    def _state_object_name(self):
        """Role state object name ends with Attributes (RoleAttributes)"""
        return self._name_camel + "Attributes"

    @property
    def _state_container_list_name(self):
        """Role state container collection name contains _attributes (role_attributes)"""
        return self._name_lower + "_attributes"

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on the state object"""
        return ["owners", "admins", "members"]

    def make_addresses(self, message, signer_keypair):
        """Makes the appropriate inputs & output addresses for the message type"""
        inputs, _ = super().make_addresses(message, signer_keypair)

        inputs.update(
            {addresser.role.address(message.role_id)}
            | {addresser.role.admin.address(message.role_id, a) for a in message.admins}
            | {addresser.role.owner.address(message.role_id, o) for o in message.owners}
            | {
                addresser.role.member.address(message.role_id, o)
                for o in message.members
            }
            | {
                addresser.user.address(u)
                for u in set(message.admins) | set(message.owners)
            }
        )

        outputs = inputs
        return inputs, outputs

    @property
    def allow_signer_not_in_state(self):
        """Whether the signer of the message is allowed to not be
        in state. (TODO: temporary, add provider keys to state)"""
        return True

    def validate_state(self, context, message, inputs, input_state, store, signer):
        """Validates the message against state"""
        super().validate_state(
            context=context,
            message=message,
            inputs=inputs,
            input_state=input_state,
            store=store,
            signer=signer,
        )
        if addresser.role.exists_in_state_inputs(
            inputs=inputs, input_state=input_state, object_id=message.role_id
        ):
            LOGGER.warning(
                # import is replayable, we'll verify information is up-to-date instead
                "Role with id %s already exists in state",
                message.role_id,
            )

    def apply_update(
        self, message, object_id, related_id, outputs, output_state, signer
    ):
        """Create admin, owner and member addresses"""
        for admin in message.admins:
            addresser.role.admin.create_relationship(
                object_id=object_id,
                related_id=admin,
                outputs=outputs,
                output_state=output_state,
            )
        for admin in message.owners:
            addresser.role.owner.create_relationship(
                object_id=object_id,
                related_id=admin,
                outputs=outputs,
                output_state=output_state,
            )
        for member in message.members:
            addresser.role.member.create_relationship(
                object_id=object_id,
                related_id=member,
                outputs=outputs,
                output_state=output_state,
            )
