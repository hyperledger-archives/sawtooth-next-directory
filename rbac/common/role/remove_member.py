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
""" Implements the REMOVE_ROLE_MEMBER message
    usage: rbac.role.member.remove.new()
"""
from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.proposal.proposal_message import ProposalMessage
from rbac.common.protobuf import proposal_transaction_pb2
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


class RemoveRoleMember(ProposalMessage):
    """ Implements the REMOVE_ROLE_MEMBER message
        usage: rbac.role.member.remove.new()
    """

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type performed by this message"""
        return addresser.MessageActionType.PROPOSE

    @property
    def message_subaction_type(self):
        """The sub action type performed by this message"""
        return addresser.MessageActionType.REMOVE

    @property
    def message_object_type(self):
        """The object type this message acts upon"""
        return addresser.ObjectType.ROLE

    @property
    def message_related_type(self):
        """the object type of the related object this message acts upon"""
        return addresser.ObjectType.USER

    @property
    def message_relationship_type(self):
        """The relationship type this message acts upon"""
        return addresser.RelationshipType.MEMBER

    @property
    def message_proto(self):
        return proposal_transaction_pb2.RemovalProposal

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message"""
        inputs, outputs = super().make_addresses(message, signer_user_id)

        proposal_address = self.address(
            object_id=message.object_id, related_id=message.related_id
        )
        inputs.add(proposal_address)
        outputs.add(proposal_address)

        signer_owner_address = addresser.role.owner.address(
            message.object_id, signer_user_id
        )
        inputs.add(signer_owner_address)

        relationship_address = addresser.role.member.address(
            message.object_id, message.related_id
        )
        inputs.add(relationship_address)
        outputs.add(relationship_address)

        return inputs, outputs

    def validate_state(self, context, message, payload, input_state, store):
        """ Validates that:
            1. the user to be removed is a member of the role
            2. the signer is an owner of the role
        """
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        if not addresser.role.member.exists_in_state_inputs(
            inputs=payload.inputs,
            input_state=input_state,
            object_id=message.object_id,
            related_id=message.related_id,
        ):
            raise ValueError(
                "User {} is not a member of role {}".format(
                    message.user_id, message.role_id
                )
            )
        if not addresser.role.owner.exists_in_state_inputs(
            inputs=payload.inputs,
            input_state=input_state,
            object_id=message.object_id,
            related_id=payload.signer.user_id,
        ):
            raise ValueError(
                "Signer {} must be an owner of the role {}".format(
                    message.signer_user_id, message.object_id
                )
            )

    def store_message(
        self, object_id, related_id, store, message, payload, output_state
    ):
        """Create the proposal data"""
        store.proposal_id = message.proposal_id
        store.proposal_type = self.proposal_type
        # pylint: disable=no-member
        store.status = protobuf.proposal_state_pb2.Proposal.REMOVED
        store.object_id = self._get_object_id(message)
        store.related_id = self._get_related_id(message)
        store.open_reason = message.reason
        store.close_reason = ""
        store.opener = payload.signer.user_id
        store.closer = payload.signer.user_id
        store.created_date = payload.now
        store.closed_date = payload.now

    def apply_update(self, message, payload, object_id, related_id, output_state):
        """Remove member address"""
        addresser.role.member.remove_relationship(
            object_id=object_id,
            related_id=related_id,
            outputs=payload.outputs,
            output_state=output_state,
        )
