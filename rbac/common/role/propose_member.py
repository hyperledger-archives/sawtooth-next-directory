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
"""Implements the PROPOSE_ADD_ROLE_MEMBER message
usage: rbac.role.member.propose.create()"""
import logging
from rbac.common import addresser
from rbac.common.proposal.proposal_message import ProposalMessage

LOGGER = logging.getLogger(__name__)


class ProposeAddRoleMember(ProposalMessage):
    """Implements the PROPOSE_ADD_ROLE_MEMBER message
    usage: rbac.role.member.propose.create()"""

    @property
    def message_action_type(self):
        """The action type performed by this message"""
        return addresser.MessageActionType.PROPOSE

    @property
    def message_subaction_type(self):
        """The subsequent action performed or proposed by this message"""
        return addresser.MessageActionType.ADD

    @property
    def message_object_type(self):
        """The object type this message acts upon"""
        return addresser.ObjectType.ROLE

    @property
    def message_relationship_type(self):
        """The relationship type this message acts upon"""
        return addresser.RelationshipType.MEMBER

    def make_addresses(self, message, signer_keypair=None):
        """Makes the appropriate inputs & output addresses for the message"""
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))

        relationship_address = addresser.role.member.address(
            message.role_id, message.user_id
        )
        user_address = addresser.user.address(message.user_id)
        role_address = addresser.role.address(message.role_id)
        proposal_address = self.address(
            object_id=message.role_id, target_id=message.user_id
        )

        inputs = [relationship_address, role_address, user_address, proposal_address]
        outputs = [proposal_address]

        return inputs, outputs
