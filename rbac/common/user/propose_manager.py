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
from rbac.common.proposal.proposal_message import ProposalMessage

LOGGER = logging.getLogger(__name__)


class ProposeUpdateUserManager(ProposalMessage):
    """Implements the PROPOSE_UPDATE_USER_MANAGER message
    usage: rbac.user.manager.propose.create()"""

    @property
    def message_action_type(self):
        """The action type performed by this message"""
        return addresser.MessageActionType.PROPOSE

    @property
    def message_subaction_type(self):
        """The subsequent action performed or proposed by this message"""
        return addresser.MessageActionType.UPDATE

    @property
    def message_object_type(self):
        """The object type this message acts upon"""
        return addresser.ObjectType.USER

    @property
    def message_relationship_type(self):
        """The relationship type this message acts upon"""
        return addresser.RelationshipType.MANAGER

    def make_addresses(self, message, signer_keypair=None):
        """Makes the appropriate inputs & output addresses for the message"""
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))

        user_address = addresser.user.address(message.user_id)
        manager_address = addresser.user.address(message.new_manager_id)
        proposal_address = addresser.proposal.address(
            object_id=message.user_id, target_id=message.new_manager_id
        )

        inputs = [user_address, manager_address, proposal_address]
        outputs = [proposal_address]

        return inputs, outputs

    def new_state(self, state, message, object_id, target_id=None):
        """Creates a new address in the blockchain state"""
        address = self.address(object_id=object_id, target_id=target_id)
        # pylint: disable=not-callable
        container = self._state_container()
        item = self._state_object(
            user_id=message.user_id,
            name=message.name,
            manager_id=message.manager_id,
            metadata=message.metadata,
        )
        # pylint: disable=no-member
        container.users.extend([item])
        self.state.set_address(state=state, address=address, container=container)
