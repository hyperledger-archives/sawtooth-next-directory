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
"""A base for all proposal message types"""
import logging
from rbac.common import addresser
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class ProposalMessage(BaseMessage):
    """A base for all proposal message types"""

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.PROPOSALS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.PROPOSAL

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.NONE

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES

    @property
    def _state_container_prefix(self):
        """Proposal state container name is plural (ProposalsContainer)"""
        return self._name_camel_plural

    def validate_state(self, context, message, payload, input_state, store):
        """Validates that:
        1. the proposed user is a User that exists in state (if proposal involves a user)
        2. the proposed role is a Role that exists in state (if a role proposal)
        3. the proposed task is a Task that exists in state (if a task proposal)
        """
        super().validate_state(
            context=context,
            message=message,
            payload=payload,
            input_state=input_state,
            store=store,
        )
        if hasattr(message, "user_id") and not addresser.user.exists_in_state_inputs(
            inputs=payload.inputs,
            input_state=input_state,
            object_id=getattr(message, "user_id"),
            skip_if_not_in_inputs=True,
        ):
            raise ValueError(
                "User with id {} does not exist in state".format(
                    getattr(message, "user_id")
                )
            )
        if hasattr(message, "role_id") and not addresser.role.exists_in_state_inputs(
            inputs=payload.inputs,
            input_state=input_state,
            object_id=getattr(message, "role_id"),
            skip_if_not_in_inputs=True,
        ):
            raise ValueError(
                "Role with id {} does not exist in state".format(
                    getattr(message, "role_id")
                )
            )
        if hasattr(message, "task_id") and not addresser.task.exists_in_state_inputs(
            inputs=payload.inputs,
            input_state=input_state,
            object_id=getattr(message, "task_id"),
            skip_if_not_in_inputs=True,
        ):
            raise ValueError(
                "Task with id {} does not exist in state".format(
                    getattr(message, "task_id")
                )
            )
