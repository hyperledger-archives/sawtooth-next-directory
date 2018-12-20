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
"""A base for all proposal action message types (e.g. confirm, reject)"""
import logging
from rbac.common import protobuf
from rbac.common.proposal.proposal_message import ProposalMessage

LOGGER = logging.getLogger(__name__)


class ProposalAction(ProposalMessage):
    """A base for all proposal rejection message types"""

    def validate_state(self, context, message, inputs, input_state, store, signer):
        """Validates that:
        1. the proposal id sent is the current proposal
        2. the proposed is open
        """
        super().validate_state(
            context=context,
            message=message,
            inputs=inputs,
            input_state=input_state,
            store=store,
            signer=signer,
        )
        if not store:
            raise ValueError(
                "{}: no proposal was found for proposal id {}".format(
                    self.message_type_name, message.proposal_id
                )
            )
        if store.proposal_id != message.proposal_id:
            raise ValueError(
                "{}: message proposal id {} does not match current proposal id {}".format(
                    self.message_type_name, message.proposal_id, store.proposal_id
                )
            )
        if store.proposal_type != self.proposal_type:
            raise ValueError(
                "{}: message class proposal type {} does not match current proposal type {}".format(
                    self.message_type_name, self.proposal_type, store.proposal_type
                )
            )
        # pylint: disable=no-member
        if store.status != protobuf.proposal_state_pb2.Proposal.OPEN:
            raise ValueError(
                "{}: proposal id {} is not open".format(
                    self.message_type_name, message.proposal_id
                )
            )
