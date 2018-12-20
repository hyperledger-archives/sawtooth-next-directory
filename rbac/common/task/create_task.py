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
"""Implements the CREATE_TASK message
usage: rbac.task.create()"""
import logging
from rbac.common import addresser
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class CreateTask(BaseMessage):
    """Implements the CREATE_TASK message
    usage: rbac.task.create()"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.CREATE

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.TASKS_ATTRIBUTES

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.TASK

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.NONE

    @property
    def relationship_type(self):
        """The relationship type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES

    @property
    def _state_object_name(self):
        """Task state object name ends with Attributes (TaskAttributes)"""
        return self._name_camel + "Attributes"

    @property
    def _state_container_list_name(self):
        """Task state container collection name contains _attributes (task_attributes)"""
        return self._name_lower + "_attributes"

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on the state object"""
        return ["owners", "admins"]

    def make_addresses(self, message, signer_keypair):
        """Makes the appropriate inputs & output addresses for the message type"""
        inputs, _ = super().make_addresses(message, signer_keypair)

        inputs.update(
            {addresser.task.address(message.task_id)}
            | {addresser.task.admin.address(message.task_id, a) for a in message.admins}
            | {addresser.task.owner.address(message.task_id, o) for o in message.owners}
            | {
                addresser.user.address(u)
                for u in set(message.owners) | set(message.admins)
            }
        )

        outputs = inputs
        return inputs, outputs

    def validate(self, message, signer=None):
        """Validates the message values"""
        super().validate(message=message, signer=signer)
        if not message.admins:
            raise ValueError("New tasks must have administrators.")
        if not message.owners:
            raise ValueError("New tasks must have owners.")

    def validate_state(self, context, message, inputs, input_state, store, signer):
        """Validates the message against state"""
        super().validate_state(
            context=context,
            message=message,
            inputs=inputs,
            input_state=input_state,
            store=store,
            signer=signer,
        )
        if addresser.task.exists_in_state_inputs(
            inputs=inputs, input_state=input_state, object_id=message.task_id
        ):
            raise ValueError("Task with id {} already exists".format(message.task_id))
        users = list(set(list(message.admins) + list(message.owners)))
        all_users_exist, users_not_found = addresser.user.exist_in_state(
            context=context, object_ids=users
        )
        if not all_users_exist:
            raise ValueError("The users {} were not found".format(users_not_found))

    def apply_update(
        self, message, object_id, related_id, outputs, output_state, signer
    ):
        """Create admin and owner addresses"""
        for admin in message.admins:
            addresser.task.admin.create_relationship(
                object_id=object_id,
                related_id=admin,
                outputs=outputs,
                output_state=output_state,
            )
        for admin in message.owners:
            addresser.task.owner.create_relationship(
                object_id=object_id,
                related_id=admin,
                outputs=outputs,
                output_state=output_state,
            )
