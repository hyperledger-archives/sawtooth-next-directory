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
""" Implements the CREATE_ROLE message
    usage: rbac.role.new()
"""
import logging

from rbac.common import addresser
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.address_space import ObjectType
from rbac.common.addresser.address_space import RelationshipType
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class CreateRole(BaseMessage):
    """ Implements the CREATE_ROLE message
        usage: rbac.role.new()
    """

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.CREATE

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
        return ["owners", "admins"]

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message type"""
        inputs, _ = super().make_addresses(message, signer_user_id)

        inputs.update(
            {addresser.role.address(message.role_id)}
            | {addresser.role.admin.address(message.role_id, a) for a in message.admins}
            | {addresser.role.owner.address(message.role_id, o) for o in message.owners}
            | {
                addresser.user.address(u)
                for u in set(message.owners) | set(message.admins)
            }
        )
        outputs = inputs
        return inputs, outputs

    def validate(self, message, signer=None):
        """Validates the message values"""
        super().validate(message=message, signer=signer)
        if not message.admins:
            raise ValueError("New roles must have administrators.")
        if not message.owners:
            raise ValueError("New roles must have owners.")

    def validate_state(self, context, message, payload, input_state, store):
        """Validates the message against state"""
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        if addresser.role.exists_in_state_inputs(
            inputs=payload.inputs, input_state=input_state, object_id=message.role_id
        ):
            raise ValueError("Role with id {} already exists".format(message.role_id))
        users = list(set(list(message.admins) + list(message.owners)))
        all_users_exist, users_not_found = addresser.user.exist_in_state(
            context=context, object_ids=users
        )
        if not all_users_exist:
            raise ValueError("The users {} were not found".format(users_not_found))

    def apply_update(self, message, payload, object_id, related_id, output_state):
        """Create admin and owner addresses"""
        for admin in message.admins:
            addresser.role.admin.create_relationship(
                object_id=object_id,
                related_id=admin,
                outputs=payload.outputs,
                output_state=output_state,
                created_date=payload.now,
            )
        for admin in message.owners:
            addresser.role.owner.create_relationship(
                object_id=object_id,
                related_id=admin,
                outputs=payload.outputs,
                output_state=output_state,
                created_date=payload.now,
            )
