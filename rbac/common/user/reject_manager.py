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
"""Implements the REJECT_UPDATE_USER_MANAGER message
usage: rbac.user.manager.reject.create()"""
from rbac.common import addresser
from rbac.common.proposal.proposal_reject import ProposalReject
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class RejectUpdateUserManager(ProposalReject):
    """Implements the REJECT_UPDATE_USER_MANAGER message
    usage: rbac.user.manager.reject.create()"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type performed by this message"""
        return addresser.MessageActionType.REJECT

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

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message"""
        inputs, outputs = super().make_addresses(message, signer_user_id)

        proposal_address = addresser.proposal.address(
            object_id=message.object_id, related_id=message.related_id
        )
        inputs.add(proposal_address)
        outputs.add(proposal_address)

        return inputs, outputs

    def validate_state(self, context, message, payload, input_state, store):
        """Validates that:
        1. The proposed new manager is the signer of the transaction"""
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        # TODO: change to verify proposal assignment and hierarchy


#        if message.related_id != payload.signer.user_id:
#            raise ValueError(
#                "Proposed manager {} is not the transaction signer {}".format(
#                    message.related_id, payload.signer.user_id
#                )
#            )
