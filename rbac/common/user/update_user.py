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
""" Implements the UPDATE_USER message
    usage: rbac.user.update()
"""

from rbac.common import addresser
from rbac.common.addresser.address_space import (
    AddressSpace,
    ObjectType,
    RelationshipType,
)
from rbac.common.base.base_message import BaseMessage
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class UpdateUser(BaseMessage):
    """ Implements the UPDATE_USER message
        usage: rbac.user.update()
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
        return AddressSpace.USER_ATTRIBUTES

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.NONE

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return RelationshipType.ATTRIBUTES

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message type"""
        inputs, _ = super().make_addresses(message, signer_user_id)

        user_address = self.address(object_id=message.next_id)
        inputs.add(user_address)

        if message.manager_id:
            manager_address = self.address(object_id=message.manager_id)
            inputs.add(manager_address)

        outputs = inputs
        return inputs, outputs

    @property
    def allow_signer_not_in_state(self):
        """Whether the signer of the message is allowed to not be
        in state. Used only for when the transaction also creates the
        signer of the message (e.g. CREATE_USER)"""
        return False

    def validate(self, message, signer=None):
        """Validates the message values"""
        super().validate(message=message, signer=signer)
        if len(message.name) < 5:
            raise ValueError("Users must have names longer than 4 characters")
        if message.manager_id is not None:
            if message.next_id == message.manager_id:
                raise ValueError("User cannot be their own manager")

    def validate_state(self, context, message, payload, input_state, store):
        """Validates the message against state"""
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        if not addresser.user.exists_in_state_inputs(
            inputs=payload.inputs, input_state=input_state, object_id=message.next_id
        ):
            raise ValueError("User with id {} does not exist".format(message.next_id))
        if message.manager_id and not addresser.user.exists_in_state_inputs(
            inputs=payload.inputs, input_state=input_state, object_id=message.manager_id
        ):
            raise ValueError(
                "Manager with id {} does not exist in state".format(message.manager_id)
            )
