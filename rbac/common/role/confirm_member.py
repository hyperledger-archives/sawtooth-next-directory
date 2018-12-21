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
"""Implements the CONFIRM_ADD_ROLE_MEMBER message
usage: rbac.role.member.confirm.create()"""
import logging
from rbac.common import addresser
from rbac.common.proposal.proposal_confirm import ProposalConfirm

LOGGER = logging.getLogger(__name__)


class ConfirmAddRoleMember(ProposalConfirm):
    """Implements the CONFIRM_ADD_ROLE_MEMBER message
    usage: rbac.role.member.confirm.create()"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_subaction_type(self):
        """The subsequent action performed or proposed by this message"""
        return addresser.MessageActionType.ADD

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

    def make_addresses(self, message, signer_keypair):
        """Makes the appropriate inputs & output addresses for the message"""
        inputs, outputs = super().make_addresses(message, signer_keypair)

        user_address = addresser.user.address(message.related_id)
        inputs.add(user_address)

        # should be owner not admin
        signer_admin_address = addresser.role.admin.address(
            message.object_id, signer_keypair.public_key
        )
        inputs.add(signer_admin_address)

        signer_owner_address = addresser.role.owner.address(
            message.object_id, signer_keypair.public_key
        )
        inputs.add(signer_owner_address)

        relationship_address = addresser.role.member.address(
            message.object_id, message.related_id
        )
        inputs.add(relationship_address)
        outputs.add(relationship_address)

        proposal_address = self.address(
            object_id=message.object_id, related_id=message.related_id
        )
        inputs.add(proposal_address)
        outputs.add(proposal_address)

        return inputs, outputs

    def validate_state(self, context, message, inputs, input_state, store, signer):
        """Validates that:
        1. the signer is an owner of the role"""
        super().validate_state(
            context=context,
            message=message,
            inputs=inputs,
            input_state=input_state,
            store=store,
            signer=signer,
        )
        # TODO: change to verify proposal assignment and hierarchy

    #          if not addresser.role.owner.exists_in_state_inputs(
    #              inputs=inputs,
    #            input_state=input_state,
    #            object_id=message.object_id,
    #            related_id=signer,
    #        ):
    #            raise ValueError(
    #                "Signer {} must be an owner of the role {}".format(
    #                    signer, message.object_id
    #                )
    #            )

    def apply_update(
        self, message, object_id, related_id, outputs, output_state, signer
    ):
        """Create admin address"""
        addresser.role.member.create_relationship(
            object_id=object_id,
            related_id=related_id,
            outputs=outputs,
            output_state=output_state,
        )
