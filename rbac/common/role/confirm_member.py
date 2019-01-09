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

    def make_addresses(self, message, signer_user_id):
        """Makes the appropriate inputs & output addresses for the message"""
        inputs, outputs = super().make_addresses(message, signer_user_id)

        user_address = addresser.user.address(message.related_id)
        inputs.add(user_address)

        # should be owner not admin
        signer_admin_address = addresser.role.admin.address(
            message.object_id, signer_user_id
        )
        inputs.add(signer_admin_address)

        signer_owner_address = addresser.role.owner.address(
            message.object_id, signer_user_id
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

    def validate_state(self, context, message, payload, input_state, store):
        """Validates that:
        1. the signer is an owner of the role"""
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        # TODO: change to verify proposal assignment and hierarchy

    #          if not addresser.role.owner.exists_in_state_inputs(
    #              inputs=inputs,
    #            input_state=input_state,
    #            object_id=message.object_id,
    #            related_id=payload.signer.user_id,
    #        ):
    #            raise ValueError(
    #                "Signer {} must be an owner of the role {}".format(
    #                    payload.signer.user_id, message.object_id
    #                )
    #            )

    def apply_update(self, message, payload, object_id, related_id, output_state):
        """Create admin address"""
        # set membership expiration 6 months from now
        expiration_date = int(payload.now + 2628000 * 6)

        addresser.role.member.create_relationship(
            object_id=object_id,
            related_id=related_id,
            outputs=payload.outputs,
            output_state=output_state,
            created_date=payload.now,
            expiration_date=expiration_date,
        )
