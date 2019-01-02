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
"""A base for all proposal creation message types"""
import logging
from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.proposal.proposal_message import ProposalMessage

LOGGER = logging.getLogger(__name__)


class ProposalPropose(ProposalMessage):
    """A base for all proposal rejection message types"""

    @property
    def message_action_type(self):
        """The action type performed by this message"""
        return addresser.MessageActionType.PROPOSE

    def validate_state(self, context, message, payload, input_state, store):
        """Validates that:
        1. the proposal is signed by the user or their manager
        2. there is no open proposal for the same relationship
        """
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        object_id = self._get_object_id(message)
        related_id = self._get_related_id(message)
        # TODO: change signer verification method
        # if hasattr(message, "user_id") and getattr(message, "user_id") != payload.signer.user_id:
        #    user = addresser.user.get_from_input_state(
        #        inputs=payload.inputs, input_state=input_state, object_id=message.user_id
        #    )
        #    if user.manager_id != payload.signer.user_id:
        #        raise ValueError(
        #            "{}: the user or their manager must be the proposal signer, got {}\n{}".format(
        #                self.message_type_name, signer, user
        #            )
        #        )
        last_proposal = addresser.proposal.get_from_input_state(
            inputs=payload.inputs,
            input_state=input_state,
            object_id=object_id,
            related_id=related_id,
        )
        if (
            # pylint: disable=no-member
            last_proposal is not None
            and last_proposal.status == protobuf.proposal_state_pb2.Proposal.OPEN
        ):
            raise ValueError(
                "Existing proposal id {} for {} {} {} {} is still open".format(
                    last_proposal.proposal_id,
                    self._name_id,
                    object_id,
                    self._related_id,
                    related_id,
                )
            )

    def store_message(
        self, object_id, related_id, store, message, payload, output_state
    ):
        """Create the proposal data"""
        store.proposal_id = message.proposal_id
        store.proposal_type = self.proposal_type
        # pylint: disable=no-member
        store.status = protobuf.proposal_state_pb2.Proposal.OPEN
        store.object_id = self._get_object_id(message)
        store.related_id = self._get_related_id(message)
        store.open_reason = message.reason
        store.opener = payload.signer.user_id
        store.created_date = payload.now
        store.metadata = message.metadata
