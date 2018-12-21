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
"""Implements the CONFIRM_UPDATE_USER_MANAGER message
usage: rbac.user.manager.confirm.create()"""
import logging
from rbac.common import addresser
from rbac.common.proposal.proposal_confirm import ProposalConfirm

LOGGER = logging.getLogger(__name__)


class ConfirmUpdateUserManager(ProposalConfirm):
    """Implements the CONFIRM_UPDATE_USER_MANAGER message
    usage: rbac.user.manager.confirm.create()"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_subaction_type(self):
        """The subsequent action performed or proposed by this message"""
        return addresser.MessageActionType.UPDATE

    @property
    def message_object_type(self):
        """The object type this message acts upon"""
        return addresser.ObjectType.USER

    @property
    def message_related_type(self):
        """the object type of the related object this message acts upon"""
        return addresser.ObjectType.USER

    @property
    def message_relationship_type(self):
        """The relationship type this message acts upon"""
        return addresser.RelationshipType.MANAGER

    def make_addresses(self, message, signer_keypair):
        """Makes the appropriate inputs & output addresses for the message"""
        inputs, outputs = super().make_addresses(message, signer_keypair)

        proposal_address = addresser.proposal.address(
            object_id=message.object_id, related_id=message.related_id
        )
        inputs.add(proposal_address)
        outputs.add(proposal_address)

        user_address = addresser.user.address(message.object_id)
        inputs.add(user_address)
        outputs.add(user_address)

        return inputs, outputs

    def validate_state(self, context, message, inputs, input_state, store, signer):
        """Validates that:
        1. the proposed manager is a User that exists in state
        2. The proposed manager is the signer of the transaction"""
        super().validate_state(
            context=context,
            message=message,
            inputs=inputs,
            input_state=input_state,
            store=store,
            signer=signer,
        )
        if message.related_id and not addresser.user.exists_in_state_inputs(
            inputs=inputs, input_state=input_state, object_id=message.related_id
        ):
            raise ValueError(
                "Manager with id {} does not exist in state".format(message.related_id)
            )
        user = addresser.user.get_from_input_state(
            inputs=inputs, input_state=input_state, object_id=message.object_id
        )
        if message.related_id != signer:
            raise ValueError(
                "Proposed manager {} is not the transaction signer".format(
                    message.related_id
                )
            )

    def store_message(
        self, object_id, related_id, store, message, outputs, output_state, signer
    ):
        super().store_message(
            object_id, related_id, store, message, outputs, output_state, signer
        )
        addresser.user.set_output_state_attribute(
            name="manager_id",
            value=message.related_id,
            outputs=outputs,
            output_state=output_state,
            object_id=message.object_id,
            related_id=None,
        )
