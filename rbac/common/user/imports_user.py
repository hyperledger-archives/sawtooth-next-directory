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
"""Implements the IMPORTS_USER message
usage: rbac.user.imports.create()"""
import logging

from rbac.common import addresser
from rbac.common.protobuf import user_transaction_pb2  # pylint: disable=unused-import
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class ImportsUser(BaseMessage):
    """Implements the IMPORTS_USER message
    usage: rbac.user.imports.create()"""

    def __init__(self):
        super().__init__()
        self._register()

    @property
    def message_action_type(self):
        """The action type from AddressSpace performed by this message"""
        return addresser.MessageActionType.IMPORTS

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.USER

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.USER

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SELF

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES

    def make_addresses(self, message, signer_keypair):
        """Makes the appropriate inputs & output addresses for the message type"""
        if not isinstance(message, self.message_proto):
            raise TypeError(
                "Expected message to be {}, got {}".format(
                    self.message_proto, type(message).__name__
                )
            )

        user_address = self.address(object_id=message.user_id)
        if message.manager_id:
            manager_address = self.address(object_id=message.manager_id)

        if message.manager_id:
            inputs = {user_address, manager_address}
        else:
            inputs = {user_address}

        outputs = inputs
        return inputs, outputs

    @property
    def allow_signer_not_in_state(self):
        """Whether the signer of the message is allowed to not be
        in state. Used only for when the transaction also creates the
        signer of the message (e.g. IMPORT_USER)"""
        return True

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
        if addresser.user.exists_in_state_inputs(
            inputs=inputs, input_state=input_state, object_id=message.user_id
        ):
            LOGGER.warning(
                # import is replayable, we'll verify information is up-to-date instead
                "User with id %s already exists in state",
                message.user_id,
            )
