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
"""Implements the DELETE_USER message"""

from rbac.common import addresser
from rbac.common.base.base_message import BaseMessage
from rbac.common.logs import get_default_logger
from rbac.common.protobuf import user_transaction_pb2  # pylint: disable=unused-import

LOGGER = get_default_logger(__name__)


class DeleteUser(BaseMessage):
    """Implements the DELETE_USER message"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.DELETE

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.NONE

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message type"""
        inputs = set({})

        user_address = self.address(object_id=message.next_id)
        inputs.add(user_address)

        outputs = inputs
        return inputs, outputs

    @property
    def allow_signer_not_in_state(self):
        """Whether the signer of the message is allowed to not be
        in state. Used only for when the transaction also creates the
        signer of the message (e.g. IMPORT_USER)"""
        return True

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
            raise ValueError(
                "User with id {} currently does not exist in state".format(
                    message.next_id
                )
            )

    def apply_update(self, message, payload, object_id, related_id, output_state):
        """ Adds deleted user's address to the removed field in output_state. This
        will inform the blockcahin to remove this address from state.

        Args:
            payload: A RBACPayload protobuf formatted variable containing fields:
                message_type, content, inputs, outputs, signer, now
            object_id: A 12-byte hexadecimal hash of the next_id
            output_state: A dictionary with two fields, changed and
                removed. The fields contains addresses that will be
                changed on the blockchain or will be removed from
                the blockchain.
        """
        addresser.user.remove_state_object(
            object_id=object_id,
            related_id=None,
            outputs=payload.outputs,
            output_state=output_state,
        )
