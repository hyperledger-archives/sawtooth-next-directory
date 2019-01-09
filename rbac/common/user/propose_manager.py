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
"""Implements the PROPOSE_UPDATE_USER_MANAGER message
usage: rbac.user.manager.propose.create()"""
import logging
from rbac.common import addresser
from rbac.common.proposal.proposal_propose import ProposalPropose

LOGGER = logging.getLogger(__name__)


class ProposeUpdateUserManager(ProposalPropose):
    """Implements the PROPOSE_UPDATE_USER_MANAGER message
    usage: rbac.user.manager.propose.create()"""

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

    @property
    def _related_id(self):
        """The attribute name for related_id"""
        return "new_manager_id"

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message"""
        inputs, outputs = super().make_addresses(message, signer_user_id)

        user_address = addresser.user.address(message.user_id)
        inputs.add(user_address)

        manager_address = addresser.user.address(message.new_manager_id)
        inputs.add(manager_address)

        proposal_address = addresser.proposal.address(
            object_id=message.user_id, related_id=message.new_manager_id
        )
        inputs.add(proposal_address)
        outputs.add(proposal_address)

        return inputs, outputs

    def validate_state(self, context, message, payload, input_state, store):
        """Validates that:
        1. the proposed manager is a User that exists in state
        2. The existing manager (if any) is the signer of the transaction"""
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        if message.new_manager_id and not addresser.user.exists_in_state_inputs(
            inputs=payload.inputs,
            input_state=input_state,
            object_id=message.new_manager_id,
        ):
            raise ValueError(
                "Manager with id {} does not exist in state".format(
                    message.new_manager_id
                )
            )
        user = addresser.user.get_from_input_state(
            inputs=payload.inputs, input_state=input_state, object_id=message.user_id
        )


# TODO: change to verify proposal assignment and hierarchy
#        if user.manager_id and user.manager_id != payload.signer.user_id:
#            raise ValueError(
#                "Existing manager {} is not the transaction signer {}".format(
#                    user.manager_id, payload.signer.user_id
#                )
#            )
