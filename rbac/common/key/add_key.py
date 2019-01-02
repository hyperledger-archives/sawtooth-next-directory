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
""" Registers a new public key for a user
    usage: rbac.key.add()
"""
import logging

from rbac.common import addresser
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class AddKey(BaseMessage):
    """ Implements the ADD_KEY message
    """

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message
        """
        return addresser.MessageActionType.ADD

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class
        """
        return addresser.AddressSpace.KEY

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class
        """
        return addresser.ObjectType.KEY

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class
        """
        return addresser.ObjectType.NONE

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class
        """
        return addresser.RelationshipType.NONE

    def make_addresses(self, message, signer_user_id):
        """ Makes the appropriate inputs & output addresses for the message type
        """
        inputs, _ = super().make_addresses(message, signer_user_id)

        key_address = self.address(object_id=message.key_id)
        inputs.add(key_address)

        user_address = addresser.user.address(object_id=message.user_id)
        inputs.add(user_address)

        user_key_address = addresser.user.key.address(
            object_id=message.user_id, related_id=message.key_id
        )
        inputs.add(user_key_address)

        outputs = inputs
        return inputs, outputs

    @property
    def allow_signer_not_in_state(self):
        """ Whether the signer of the message is allowed to
            not be in state.
        """
        return True

    def validate_state(self, context, message, payload, input_state, store):
        """ Validates the message against state
        """
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        if not addresser.user.exists_in_state_inputs(
            inputs=payload.inputs, input_state=input_state, object_id=message.user_id
        ):
            raise ValueError(
                "User with id {} does not exists in state".format(message.user_id)
            )

    def apply_update(self, message, payload, object_id, related_id, output_state):
        """ Stores additional data and relationships
        """
        addresser.user.key.create_relationship(
            object_id=message.user_id,
            related_id=message.key_id,
            outputs=payload.outputs,
            output_state=output_state,
            created_date=payload.now,
        )
