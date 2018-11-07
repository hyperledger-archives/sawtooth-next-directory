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

import logging
import inspect

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from rbac.common.role.role_manager import RoleManager
from rbac.common.task.task_manager import TaskManager

LOGGER = logging.getLogger(__name__)


def _only_rbac_common_(value):
    """Get only objects that are of type rbac.common.*"""
    return str(type(value)).startswith("<class 'rbac.common.")


def getattr_or_none(value, attrib):
    """getattr except returns None instead of throwing KeyError"""
    if hasattr(value, attrib):
        return getattr(value, attrib)
    return None


def message_type_name(message_type):
    """returns the protobuf enum name from the value"""
    # pylint: disable=no-member
    items = RBACPayload.MessageType.DESCRIPTOR.values_by_name.items()
    # return items[message_type][0] # breaks on OSX and/or Python 3.7
    for (key, value) in items:
        if value == message_type:
            return key
    return None


class RBACManager:
    def __init__(self):
        self.user = UserManager()
        self.role = RoleManager()
        self.task = TaskManager()
        self.handlers = {}
        self._walk_handlers(self, "rbac")

    def _walk_handlers(self, node, path):
        """Walk the rbac library to find all apply methods to register in the
        handlers collection for the transaction processor"""
        props = [
            name
            for (name, value) in inspect.getmembers(node, _only_rbac_common_)
            if not name.startswith("__")
        ]
        for prop in props:
            new_path = path + "." + prop
            value = getattr(node, prop)
            message_type = getattr_or_none(value, "message_type")
            apply = getattr_or_none(value, "apply")
            if message_type is not None:
                self.register_handler(new_path, message_type, apply)
            self._walk_handlers(value, new_path)

    def register_handler(self, path, message_type, apply):
        """Register a transaction processor handler for a given message type"""
        if message_type in self.handlers:
            raise KeyError(
                "{} tried to register message {} that was already registered".format(
                    path, message_type_name(message_type)
                )
            )

        if apply is None:
            return

        self.handlers[message_type] = apply

    def has_handler(self, message_type):
        """Whether a handler is registered for the given message type"""
        return bool(message_type in self.handlers)

    def can_handle(self, payload):
        """Whether we know how to handle a given payload"""
        return self.has_handler(payload.message_type)

    def get_handler(self, message_type):
        """Get the handler for the given message type"""
        if message_type in self.handlers:
            return self.handlers[message_type]
        return None

    def apply(self, header, payload, state):
        """Main entry point for the transaction processor"""
        if not self.can_handle(payload=payload):
            raise InvalidTransaction(
                "No handler registered for {}".format(
                    message_type_name(payload.message_type)
                )
            )

        self.handlers[payload.message_type](header=header, payload=payload, state=state)
