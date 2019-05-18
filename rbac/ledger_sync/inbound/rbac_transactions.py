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
# ------------------------------------------------------------------------------
""" LDAP Sawtooth Transaction Creation
"""
import os
from uuid import uuid4

import rethinkdb as r

from rbac.common import addresser
from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import encrypt_private_key
from rbac.common.logs import get_default_logger
from rbac.common.role import Role
from rbac.common.role.delete_role import DeleteRole
from rbac.common.role.delete_role_admin import DeleteRoleAdmin
from rbac.common.role.delete_role_member import DeleteRoleMember
from rbac.common.role.delete_role_owner import DeleteRoleOwner
from rbac.common.user import User
from rbac.common.user.delete_user import DeleteUser
from rbac.common.util import bytes_from_hex
from rbac.common.sawtooth import batcher
from rbac.providers.common.db_queries import connect_to_db
from rbac.server.api.proposals import PROPOSAL_TRANSACTION
from rbac.server.db.proposals_query import (
    fetch_open_proposals_by_opener,
    fetch_open_proposals_by_target,
    get_open_proposals_by_approver,
)

LOGGER = get_default_logger(__name__)

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

AES_KEY = os.getenv("AES_KEY")


def add_transaction(inbound_entry):
    """ Adds transactional entries onto inbound_entry
    """
    try:
        set_metadata_flag = {}
        data = inbound_entry["data"]
        key_pair = Key()
        encrypted_private_key = encrypt_private_key(
            AES_KEY, key_pair.public_key, key_pair.private_key_bytes
        )
        inbound_entry["public_key"] = key_pair.public_key
        inbound_entry["private_key"] = encrypted_private_key
        set_metadata_flag["sync_direction"] = "INBOUND"
        data["metadata"] = set_metadata_flag
        data["provider_id"] = inbound_entry["provider_id"]

        if inbound_entry["data_type"] == "user":
            next_user = get_next_object(
                "user_mapping", data["remote_id"], inbound_entry["provider_id"]
            )
            # Generate Ids
            if next_user:
                next_id = next_user[0]["next_id"]
            else:
                next_id = str(uuid4())
            inbound_entry = add_sawtooth_prereqs(
                entry_id=next_id, inbound_entry=inbound_entry, data_type="user"
            )

            message = User().imports.make(
                signer_keypair=key_pair, next_id=next_id, **data
            )
            batch = User().imports.batch(
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
                message=message,
            )
            inbound_entry["batch"] = batch.SerializeToString()
            add_metadata(inbound_entry, message)

        elif inbound_entry["data_type"] == "group":
            next_role = get_next_object(
                "roles", data["remote_id"], inbound_entry["provider_id"]
            )
            # Generate Ids
            if next_role:
                next_id = next_role[0]["role_id"]
            else:
                next_id = str(uuid4())

            inbound_entry = add_sawtooth_prereqs(
                entry_id=next_id, inbound_entry=inbound_entry, data_type="group"
            )

            message = Role().imports.make(
                signer_keypair=key_pair, role_id=next_id, **data
            )
            batch = Role().imports.batch(
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
                message=message,
            )
            inbound_entry["batch"] = batch.SerializeToString()
            add_metadata(inbound_entry, message)

        elif inbound_entry["data_type"] == "user_deleted":
            LOGGER.info(
                "User deletion detected in inbound_queue: %s", data["remote_id"]
            )

            # Find user to be deleted
            deleted_user = data["remote_id"]
            conn = connect_to_db()
            user_in_db = (
                r.table("users")
                .filter({"remote_id": deleted_user})
                .coerce_to("array")
                .run(conn)
            )
            conn.close()

            # Process if the user exists
            if user_in_db:
                delete_user_transaction(inbound_entry, user_in_db, key_pair)

        elif inbound_entry["data_type"] == "group_deleted":
            LOGGER.info(
                "Group deletion detected in inbound_queue: %s", data["remote_id"]
            )
            deleted_group = data["remote_id"]
            conn = connect_to_db()
            group_in_db = (
                r.table("roles")
                .filter({"remote_id": deleted_group})
                .coerce_to("array")
                .run(conn)
            )
            if group_in_db:
                role_delete = DeleteRole()
                role_id = group_in_db[0]["role_id"]

                role_relationships = fetch_role_relationships(
                    role_id=role_id, conn=conn
                )
                if role_relationships:
                    data = {**data, **role_relationships}

                inbound_entry = add_sawtooth_prereqs(
                    entry_id=role_id, inbound_entry=inbound_entry, data_type="group"
                )
                message = role_delete.make(
                    signer_keypair=key_pair, role_id=role_id, **data
                )
                batch = role_delete.batch(
                    signer_keypair=key_pair,
                    signer_user_id=key_pair.public_key,
                    message=message,
                )
                inbound_entry["batch"] = batch.SerializeToString()
            conn.close()
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
    keys = META_DATA_PROHIBITED & set(metadata.keys())
    if "id" in metadata:
        metadata["remote_idx"] = metadata.pop("id", None)
    for key in keys:
        metadata["remote_" + key] = metadata.pop(key, None)
    inbound_entry["metadata"] = metadata


def get_next_object(table, remote_id, provider_id):
    """Check if object already exists in NEXT and return it."""
    query_filter = {"remote_id": remote_id}
    if table == "user_mapping":
        query_filter["provider_id"] = provider_id
    conn = connect_to_db()
    result = r.table(table).filter(query_filter).coerce_to("array").run(conn)
    conn.close()
    return result


def add_sawtooth_prereqs(entry_id, inbound_entry, data_type):
    """ Adds the following fields to inbound_entry: address, object_id,
    object_type, and next_id if data_type is set as 'user'.

    Args:
        entry_id: A string containing the user's or group's UUID4
            formatted id.
        inbound_entry: A dictionary containing one user/group data that was fetched
            from the integrated provider along with additional information
            like: provider_id, timestamp, and sync_type.
        data_type: A string with the value of either 'user' or 'group'.

    Returns:
        inbound_entry: A dictionary of the original inbound_entry with additional
            fields added as they are required to process the data to Sawtooth
            Blockchain.

    Raises:
        ValueError: If the data_type parameter does not have the value
            of 'user' or 'group'.
    """
    if data_type == "user":
        object_id = User().hash(entry_id)
        address = User().address(object_id=object_id)
        inbound_entry["next_id"] = entry_id
        inbound_entry["object_type"] = addresser.ObjectType.USER.value
    elif data_type == "group":
        object_id = Role().hash(entry_id)
        address = Role().address(object_id=object_id)
        inbound_entry["object_type"] = addresser.ObjectType.ROLE.value
    else:
        raise ValueError(
            "Expecting data_type to be 'user' or 'group, found: " + data_type
        )
    inbound_entry["address"] = bytes_from_hex(address)
    inbound_entry["object_id"] = bytes_from_hex(object_id)
    return inbound_entry


def fetch_role_relationships(role_id, conn):
    """ Fetches all admins, members, owners of role_id from
    RethinkDB tables.

    Args:
        role_id: UUID4 formatted ID of the role.
        conn: A RethinkDB connection

    Returns:
        result: A dict containing a list of all role admins,
            members, and owners if they do exist in RethinkDB.
    """
    result = dict()
    for relationship in ["admins", "members", "owners"]:
        table_name = "role_" + relationship
        relationship_list = list(
            r.table(table_name)
            .filter({"role_id": role_id})
            .get_field("related_id")
            .run(conn)
        )
        result[relationship] = relationship_list
    return result


def delete_role_transaction(inbound_entry, role_in_db, key_pair):
    """Composes transactions for deleting a role. This includes rejecting any
    pending proposals concerning the role, deleting role_owner, role_admin, and
    role_member relationships, and the role object.
    Args:
        inbound_entry:
            dict: transaction entry from the inbound queue containing one
            user/group data that was fetched from the integrated provider
            along with additional information like:
                provider_id, timestamp, and sync_type.
        role_in_db:
            dict: an entry in the roles table in rethinkdb.
                (see /docs/diagrams/out/rethink_db_schemas.svg for table schemas)
        key_pair:
            obj: public and private keys for user.
    """
    next_id = role_in_db[0]["next_id"]
    inbound_entry = add_sawtooth_prereqs(
        entry_id=next_id, inbound_entry=inbound_entry, data_type="role"
    )

    txn_list = []
    # Compile role relationship transactions for removal from blockchain
    txn_list = create_reject_ppsls_role_txns(key_pair, next_id, txn_list)
    txn_list = create_delete_role_owner_txns(key_pair, next_id, txn_list)
    txn_list = create_delete_role_admin_txns(key_pair, next_id, txn_list)
    txn_list = create_delete_role_member_txns(key_pair, next_id, txn_list)
    txn_list = create_delete_role_txns(key_pair, next_id, txn_list)

    if txn_list:
        batch = batcher.make_batch_from_txns(
            transactions=txn_list, signer_keypair=key_pair
        )
        inbound_entry["batch"] = batch.SerializeToString()


def delete_user_transaction(inbound_entry, user_in_db, key_pair):
    """Composes transactions for deleting a user.  This includes deleting role_owner,
    role_admin, and role_member relationships and user object.
    """
    user_delete = DeleteUser()
    next_id = user_in_db[0]["next_id"]
    inbound_entry = add_sawtooth_prereqs(
        entry_id=next_id, inbound_entry=inbound_entry, data_type="user"
    )

    txn_list = []
    # Compile role relationship transactions for removal from blockchain
    txn_list = create_reject_ppsls_user_txns(key_pair, next_id, txn_list)
    txn_list = create_delete_role_owner_txns(key_pair, next_id, txn_list)
    txn_list = create_delete_role_admin_txns(key_pair, next_id, txn_list)
    txn_list = create_delete_role_member_txns(key_pair, next_id, txn_list)

    # Compile user delete transaction for removal from blockchain
    message = user_delete.make(signer_keypair=key_pair, next_id=next_id)
    payload = user_delete.make_payload(
        message=message, signer_keypair=key_pair, signer_user_id=key_pair.public_key
    )
    transaction = batcher.make_transaction(payload=payload, signer_keypair=key_pair)
    txn_list.extend([transaction])

    if txn_list:
        batch = batcher.make_batch_from_txns(
            transactions=txn_list, signer_keypair=key_pair
        )
        inbound_entry["batch"] = batch.SerializeToString()


def create_delete_role_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for a role object.
    Args:
        key_pair:
               obj: public and private keys for user
        next_id: next_
            str: next_id to search for the roles where user is the admin
        txn_list:
            list: transactions for batch submission
    Returns:
        txn_list:
            list: extended list of transactions for batch submission
    """
    role_delete = DeleteRole()
    message = role_delete.make(signer_keypair=key_pair, next_id=next_id)
    payload = role_delete.make_payload(
        message=message, signer_keypair=key_pair, signer_user_id=key_pair.public_key
    )
    transaction = batcher.make_transaction(payload=payload, signer_keypair=key_pair)
    txn_list.extend([transaction])
    return txn_list


def create_delete_role_owner_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for an owner if ownership of a role(s) exists."""
    conn = connect_to_db()
    roles = (
        r.table("role_owners")
        .filter({"related_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if roles:
        owner_delete = DeleteRoleOwner()
        for role in roles:
            owner_delete_message = owner_delete.make(
                signer_keypair=key_pair, related_id=next_id, role_id=role["role_id"]
            )
            payload = owner_delete.make_payload(
                message=owner_delete_message,
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
            )
            transaction = batcher.make_transaction(
                payload=payload, signer_keypair=key_pair
            )
            txn_list.extend([transaction])
    return txn_list


def create_delete_role_admin_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for an admin if user is an admin of any roles."""
    conn = connect_to_db()
    roles = (
        r.table("role_admins")
        .filter({"related_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if roles:
        admin_delete = DeleteRoleAdmin()
        for role in roles:
            admin_delete_message = admin_delete.make(
                signer_keypair=key_pair, related_id=next_id, role_id=role["role_id"]
            )
            payload = admin_delete.make_payload(
                message=admin_delete_message,
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
            )
            transaction = batcher.make_transaction(
                payload=payload, signer_keypair=key_pair
            )
            txn_list.extend([transaction])
    return txn_list


def create_delete_role_member_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for a member if user is an member of any roles."""
    conn = connect_to_db()
    roles = (
        r.table("role_members")
        .filter({"related_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if roles:
        member_delete = DeleteRoleMember()
        for role in roles:
            admin_delete_message = member_delete.make(
                signer_keypair=key_pair, related_id=next_id, role_id=role["role_id"]
            )
            payload = member_delete.make_payload(
                message=admin_delete_message,
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
            )
            transaction = batcher.make_transaction(
                payload=payload, signer_keypair=key_pair
            )
            txn_list.extend([transaction])
    return txn_list


def create_reject_ppsls_role_txns(key_pair, next_id, txn_list):
    """Create the reject open proposals transactions for a role that has been
    deleted.
       Args:
           key_pair:
               obj: public and private keys for user
           next_id: next_
               str: next_id of the targeted role to close proposals for
           txn_list:
               list: transactions for batch submission
    """
    conn = connect_to_db()
    proposals = fetch_open_proposals_by_target(next_id).coerce_to("array").run(conn)
    conn.close()
    if proposals:
        for proposal in proposals:
            reason = "Target Role was deleted."
            reject_proposal = PROPOSAL_TRANSACTION[proposal["proposal_type"]][
                "REJECTED"
            ]
            reject_proposal_msg = reject_proposal.make(
                signer_keypair=key_pair,
                signer_user_id=next_id,
                proposal_id=proposal["proposal_id"],
                object_id=proposal["object_id"],
                related_id=proposal["related_id"],
                reason=reason,
            )
            payload = reject_proposal.make_payload(
                message=reject_proposal_msg,
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
            )
            transaction = batcher.make_transaction(
                payload=payload, signer_keypair=key_pair
            )
            txn_list.extend([transaction])
    return txn_list


def create_reject_ppsls_user_txns(key_pair, next_id, txn_list):
    """Create the reject open proposals transactions for user that has been deleted.
       Args:
           key_pair:
               obj: public and private keys for user
           next_id:
               str: next_id for of the targeted user to close proposals for
           txn_list:
               list: transactions for batch submission

    """
    conn = connect_to_db()
    proposals = (
        fetch_open_proposals_by_opener(next_id)
        .union(get_open_proposals_by_approver(next_id))
        .distinct()
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if proposals:
        for proposal in proposals:
            if proposal["opener"] == next_id:
                reason = "Opener was deleted"
            else:
                reason = "Assigned Appover was deleted."
            reject_proposal = PROPOSAL_TRANSACTION[proposal["proposal_type"]][
                "REJECTED"
            ]
            reject_proposal_msg = reject_proposal.make(
                signer_keypair=key_pair,
                signer_user_id=next_id,
                proposal_id=proposal["proposal_id"],
                object_id=proposal["object_id"],
                related_id=proposal["related_id"],
                reason=reason,
            )
            payload = reject_proposal.make_payload(
                message=reject_proposal_msg,
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
            )
            transaction = batcher.make_transaction(
                payload=payload, signer_keypair=key_pair
            )
            txn_list.extend([transaction])
    return txn_list
