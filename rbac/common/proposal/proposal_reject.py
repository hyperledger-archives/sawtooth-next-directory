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
"""A base for all proposal rejection message types"""

from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.proposal.proposal_action import ProposalAction
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class ProposalReject(ProposalAction):
    """A base for all proposal rejection message types"""

    @property
    def message_action_type(self):
        """The action type performed by this message"""
        return addresser.MessageActionType.REJECT

    def store_message(
        self, object_id, related_id, store, message, payload, output_state
    ):
        """Update the proposal data"""
        # pylint: disable=no-member
        store.status = protobuf.proposal_state_pb2.Proposal.REJECTED
        store.close_reason = message.reason
        store.closer = payload.signer.next_id
        store.closed_date = payload.now
