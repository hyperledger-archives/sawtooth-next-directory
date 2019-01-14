# Copyright 2019 Contributors to Hyperledger Sawtooth
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
""" Implements the UPDATE_ROLE message
    usage: rbac.role.new()
"""
import logging

from rbac.common import addresser
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.address_space import ObjectType
from rbac.common.addresser.address_space import RelationshipType
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class UpdateRole(BaseMessage):
    """ Implements the UPDATE_ROLE message
        usage: rbac.role.new()
    """

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.UPDATE

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

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message type"""
        inputs, _ = super().make_addresses(message, signer_user_id)

        inputs.update({addresser.role.address(message.role_id)})

        outputs = inputs
        return inputs, outputs

    def validate(self, message, signer=None):
        """Validates the message values"""
        super().validate(message=message, signer=signer)
        if message.description is None:
            raise ValueError("To update a role, a description must be provided.")

    def validate_state(self, context, message, payload, input_state, store):
        """Validates the message against state"""
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        if not addresser.role.exists_in_state_inputs(
            inputs=payload.inputs, input_state=input_state, object_id=message.role_id
        ):
            raise ValueError("Role with id {} does not exist".format(message.role_id))
