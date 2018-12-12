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
# ------------------------------------------------------------------------------
""" LDAP Sawtooth Transaction Creation
"""
import logging

from rbac.common import rbac
from rbac.common.crypto.keys import Key
from rbac.common.util import bytes_from_hex

SIGNER_KEYPAIR = Key()
LOGGER = logging.getLogger(__name__)


def add_transaction(inbound_entry):
    """ Adds transactional entries onto inbound_entry
    """
    try:
        if inbound_entry["data_type"] == "user":
            data = inbound_entry["data"]
            if not data or "user_id" not in data:
                raise KeyError("user_id not found")

            object_id = rbac.user.hash(data["user_id"])
            address = rbac.user.address(object_id=object_id)

            inbound_entry["address"] = bytes_from_hex(address)
            inbound_entry["object_id"] = bytes_from_hex(object_id)
            inbound_entry["object_type"] = rbac.addresser.ObjectType.USER.value

            message = rbac.user.imports.make(signer_keypair=SIGNER_KEYPAIR, **data)
            batch = rbac.user.imports.batch(
                signer_keypair=SIGNER_KEYPAIR, message=message
            )
            inbound_entry["batch"] = batch.SerializeToString()
            add_metadata(inbound_entry, message)

        elif inbound_entry["data_type"] == "group":
            data = inbound_entry["data"]
            if not data or "role_id" not in data:
                raise KeyError("role_id not found")

            object_id = rbac.role.hash(data["role_id"])
            address = rbac.role.address(object_id=object_id)

            inbound_entry["address"] = bytes_from_hex(address)
            inbound_entry["object_id"] = bytes_from_hex(object_id)
            inbound_entry["object_type"] = rbac.addresser.ObjectType.ROLE.value

            message = rbac.role.imports.make(signer_keypair=SIGNER_KEYPAIR, **data)
            batch = rbac.role.imports.batch(
                signer_keypair=SIGNER_KEYPAIR, message=message
            )
            inbound_entry["batch"] = batch.SerializeToString()
            add_metadata(inbound_entry, message)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(
            "Unable to create transaction for inbound data:\n%s", inbound_entry
        )
        LOGGER.exception(err)


def add_metadata(inbound_entry, message):
    """ Any fields in data that are not sent to the blockchain state
        via the message are stored in a metadata dictionary to be put
        in the metadata table in RethinkDB. This creates the metadata
        dictionary from data and removes fields that are in the message.
    """
    message_keys = [f[0].name for f in message.ListFields()]
    metadata = dict(inbound_entry["data"])
    for key in message_keys:
        metadata.pop(key, None)
    inbound_entry["metadata"] = metadata
