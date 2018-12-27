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
from rbac.common.logs import get_logger
from rbac.common import rbac
from rbac.common.crypto.keys import Key
from rbac.common.util import bytes_from_hex
from rbac.providers.common.rbac_uuid_mapper import get_uuid
from rbac.providers.common.rbac_uuid_mapper import map_uuid_identifiers

SIGNER_KEYPAIR = Key()
LOGGER = get_logger(__name__)

# These field names may not be contained in metadata, as they conflict with official field names.
# If they appear, they will be prefixed with "remote_"
META_DATA_PROHIBITED = {
    "address",
    "block_created",
    "block_updated",
    "created_at",
    "updated_at",
    "object_type",
    "object_id",
    "related_type",
    "relationship_type",
    "related_id",
}


def add_transaction(inbound_entry):
    """ Adds transactional entries onto inbound_entry
    """
    try:
        data = inbound_entry.get("data")
        if not data:
            raise KeyError("data not found on inbound entry")
        data_type = inbound_entry.get("data_type")
        if data_type not in ("user", "group"):
            raise KeyError("unhandled inbound data type {}".format(data_type))
        relationship_id = data.get("relationship_id")
        if not relationship_id:
            raise KeyError("relationship_id not found in inbound data")
        else:
            del data["relationship_id"]
        remote_id = data.get("remote_id")
        if not remote_id:
            raise KeyError("remote_id not found in inbound data")

        object_id = get_uuid(relationship_id)

        if "uuid" in data:
            uuid = data["uuid"]
            if uuid:
                uuid.remove(relationship_id)
                uuid.remove(remote_id)
            del data["uuid"]

        if inbound_entry["data_type"] == "user":

            user_id = object_id
            address = rbac.user.address(object_id=object_id)

            inbound_entry["address"] = bytes_from_hex(address)
            inbound_entry["object_id"] = bytes_from_hex(object_id)
            inbound_entry["object_type"] = rbac.addresser.ObjectType.USER.value

            if "manager_id" in data:
                data["manager_id"] = map_uuid_identifiers(data["manager_id"])
            if "member_of" in data:
                data["member_of"] = map_uuid_identifiers(data["member_of"])

            message = rbac.user.imports.make(
                signer_keypair=SIGNER_KEYPAIR, user_id=user_id, **data
            )
            batch = rbac.user.imports.batch(
                signer_keypair=SIGNER_KEYPAIR, message=message
            )
            inbound_entry["batch"] = batch.SerializeToString()
            add_metadata(inbound_entry, message)

        elif inbound_entry["data_type"] == "group":

            role_id = object_id
            address = rbac.role.address(object_id=object_id)

            inbound_entry["address"] = bytes_from_hex(address)
            inbound_entry["object_id"] = bytes_from_hex(object_id)
            inbound_entry["object_type"] = rbac.addresser.ObjectType.ROLE.value

            if "members" in data:
                data["members"] = map_uuid_identifiers(data["members"])
            if "owners" in data:
                data["owners"] = map_uuid_identifiers(data["owners"])

            message = rbac.role.imports.make(
                signer_keypair=SIGNER_KEYPAIR, role_id=role_id, **data
            )
            batch = rbac.role.imports.batch(
                signer_keypair=SIGNER_KEYPAIR, message=message
            )
            inbound_entry["batch"] = batch.SerializeToString()
            add_metadata(inbound_entry, message)

    except KeyError as err:
        LOGGER.exception(
            "Unable to create transaction for inbound data:\n%s\n%s",
            str(err),
            inbound_entry,
        )
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
    metadata.pop("relationship_id", None)
    keys = META_DATA_PROHIBITED & set(metadata.keys())
    if "id" in metadata:
        metadata["remote_idx"] = metadata.pop("id", None)
    for key in keys:
        metadata["remote_" + key] = metadata.pop(key, None)
    inbound_entry["metadata"] = metadata
