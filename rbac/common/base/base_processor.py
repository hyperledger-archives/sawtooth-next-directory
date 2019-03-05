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
"""A Base Sawtooth Transaction Processor"""

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.sawtooth.batcher import get_message_type_name
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)

message_handlers = {}  # pylint: disable=invalid-name


def register_message_handler(message):
    """Register a transaction message handler for a given message class"""
    message_handlers[message.message_type] = message


def unregister_message_handler(message):
    """Unregister a transaction message handler for a given message class"""
    if message.message_type in message_handlers:
        del message_handlers[message.message_type]


def has_message_handler(message_type):
    """Whether a handler is registered for the given message type"""
    return bool(message_type in message_handlers)


def can_handle_message(payload):
    """Whether we know how to handle a given payload"""
    return has_message_handler(payload.message_type)


def get_message_handler(message_type):
    """Get the handler for the given message type"""
    if message_type in message_handlers:
        return message_handlers[message_type]
    return None


def handle_message(header, payload, context):
    """Handle the messages submitted to the transaction processor"""
    if not can_handle_message(payload=payload):
        raise InvalidTransaction(
            "No handler registered for {}".format(
                get_message_type_name(payload.message_type)
            )
        )
    message_handlers[payload.message_type].apply(
        header=header, payload=payload, context=context
    )


# pylint: disable=useless-object-inheritance
class BaseTransactionProcessor(object):
    """A Base Sawtooth Transaction Processor"""

    def __init__(self, family):
        object.__init__(self)
        self._family = family

    @property
    def family_name(self):
        """The transaction family name handled by this processor"""
        return self._family.name

    @property
    def family_versions(self):
        """Family versions handled by this transaction processor"""
        return self._family.versions

    @property
    def encodings(self):
        """The expected message encoding"""
        return self._family.encodings

    @property
    def namespaces(self):
        """Namespaces handled by this transaction processor"""
        return self._family.namespaces

    def register_message_handler(self, message):
        """Register a transaction processor handler for a given message class"""
        return register_message_handler(message)

    def has_message_handler(self, message_type):
        """Whether a handler is registered for the given message type"""
        return has_message_handler(message_type)

    def can_handle_message(self, payload):
        """Whether we know how to handle a given payload"""
        return can_handle_message(payload)

    def get_message_handler(self, message_type):
        """Get the handler for the given message type"""
        return get_message_handler(message_type)

    def handle_message(self, header, payload, context):
        """Handle the messages submitted to the transaction processor"""
        return handle_message(header, payload, context)

    def apply(self, transaction, context):
        """Main entry point for the Sawtooth Transaction Processor
        Transactions get submitted to this required interface method"""
        try:
            payload = RBACPayload()
            payload.ParseFromString(transaction.payload)
            return handle_message(
                header=transaction.header, payload=payload, context=context
            )
        except ValueError as err:
            raise InvalidTransaction(err)
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.exception("Unexpected processor error %s", err)
            raise InvalidTransaction(err)
