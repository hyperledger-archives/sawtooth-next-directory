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
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac.common import addresser
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.base.base_processor import BaseTransactionProcessor


LOGGER = logging.getLogger(__name__)


class RBACTransactionHandler(object):
    def __init__(self):
        object.__init__(self)
        self._processor = BaseTransactionProcessor(addresser.family)

    @property
    def family_name(self):
        return addresser.family.name

    @property
    def family_versions(self):
        return addresser.family.versions

    @property
    def encodings(self):
        return addresser.family.encodings

    @property
    def namespaces(self):
        return addresser.family.namespaces

    def apply(self, transaction, state):
        try:
            if transaction.payload == "ping".encode("utf-8"):
                LOGGER.info("Got a ping!")
                return
            payload = RBACPayload()
            payload.ParseFromString(transaction.payload)

            if self._processor.has_message_handler(message_type=payload.message_type):
                return self._processor.handle_message(
                    header=transaction.header, payload=payload, context=state
                )
            raise InvalidTransaction(
                "Transaction processor has no registered handler for message type {}".format(
                    payload.message_type
                )
            )
        except (ValueError, KeyError) as err:
            raise InvalidTransaction(err)
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.exception("Unexpected processor %s exception", type(err))
            LOGGER.exception(err)
            raise InvalidTransaction(err)
