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
""" Common Transaction Creation
"""
import rethinkdb as r
from rbac.server.api.proposals import PROPOSAL_TRANSACTION
from rbac.server.db.db_utils import create_connection
from rbac.server.db.proposals_query import fetch_open_proposals_by_role
from rbac.common.logs import get_default_logger
from rbac.common.role.delete_role import DeleteRole
from rbac.common.role.delete_role_admin import DeleteRoleAdmin
from rbac.common.role.delete_role_owner import DeleteRoleOwner
from rbac.common.role.delete_role_member import DeleteRoleMember
from rbac.common.sawtooth import batcher

LOGGER = get_default_logger(__name__)


def create_del_role_txns(key_pair, role_id, txn_list):
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
    message = role_delete.make(signer_keypair=key_pair, role_id=role_id)
    payload = role_delete.make_payload(
        message=message, signer_keypair=key_pair, signer_user_id=key_pair.public_key
    )
    transaction = batcher.make_transaction(payload=payload, signer_keypair=key_pair)
    txn_list.extend([transaction])
    return txn_list


async def create_rjct_ppsls_role_txns(key_pair, role_id, txn_user_id, txn_list):
    """Create the reject open proposals transactions for a role that has been
    deleted.
    Args:
        key_pair:
            obj: public and private keys for user
        role_id:
            str: role_id parameter of the targeted role to close proposals for
        txn_list:
            list: transactions for batch submission
    Returns:
        txn_list:
            list: extended list of transactions for batch submission
    """
    conn = await create_connection()
    proposals = await fetch_open_proposals_by_role(conn, role_id)
    conn.close()
    if proposals:
        for proposal in proposals:
            reason = "Target Role was deleted."
            reject_proposal = PROPOSAL_TRANSACTION[proposal["proposal_type"]][
                "REJECTED"
            ]
            reject_proposal_msg = reject_proposal.make(
                signer_keypair=key_pair,
                signer_user_id=txn_user_id,
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
    else:
        LOGGER.warning("No proposals found for role: %s", role_id)
    return txn_list


async def create_del_mmbr_by_role_txns(key_pair, role_id, txn_list):
    """Create the delete transactions for a role. Used when fully deleting a role.
    Args:
        key_pair:
            obj: public and private keys for user
        role_id:
            str: next_id of a role to search for
        txn_list:
            list: transactions for batch submission
    Returns:
        txn_list:
            list: extended list of transactions for batch submission
    """
    conn = await create_connection()
    role_members = (
        await r.table("role_members")
        .filter({"role_id": role_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if role_members:
        member_delete = DeleteRoleMember()
        for member in role_members:
            admin_delete_message = member_delete.make(
                signer_keypair=key_pair,
                related_id=member["related_id"],
                role_id=member["role_id"],
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
    else:
        LOGGER.info("No role_members found for role: %s", role_id)
    return txn_list


async def create_del_mmbr_by_user_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for a member if user is an member of any
    roles.
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
    conn = await create_connection()
    roles = (
        await r.table("role_members")
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
    else:
        LOGGER.info("No role_members found for user: %s", next_id)
    return txn_list


async def create_del_ownr_by_role_txns(key_pair, role_id, txn_list):
    """Create the delete transactions for role_owners. Used when fully deleting
    a role.
    Args:
           key_pair:
               obj: public and private keys for user
           role_id:
               str: next_id of the role to search for
           txn_list:
               list: transactions for batch submission
    Returns:
        txn_list:
            list: extended list of transactions for batch submission
    """
    conn = await create_connection()
    role_owners = (
        await r.table("role_owners")
        .filter({"role_id": role_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if role_owners:
        owner_delete = DeleteRoleOwner()
        for owner in role_owners:
            owner_delete_message = owner_delete.make(
                signer_keypair=key_pair,
                related_id=owner["related_id"],
                role_id=owner["role_id"],
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
    else:
        LOGGER.info("No role_owners found for role: %s", role_id)
    return txn_list


async def create_del_ownr_by_user_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for an owner if ownership of a role(s) exists.
    Args:
           key_pair:
               obj: public and private keys for user
           next_id:
               str: next_id to search for the roles where user is the admin
           txn_list:
               list: transactions for batch submission
    Returns:
        txn_list:
            list: extended list of transactions for batch submission
    """
    conn = await create_connection()
    roles = (
        await r.table("role_owners")
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
    else:
        LOGGER.info("No role_owners found for user: %s", next_id)
    return txn_list


async def create_del_admin_by_role_txns(key_pair, role_id, txn_list):
    """Create the delete transactions for an admin if user is an admin of any roles.
    Args:
           key_pair:
               obj: public and private keys for user
           role_id:
               str: next_id of the role to search for
           txn_list:
               list: transactions for batch submission
    Returns:
        txn_list:
            list: extended list of transactions for batch submission
    """
    conn = await create_connection()
    role_admins = (
        await r.table("role_admins")
        .filter({"role_id": role_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if role_admins:
        admin_delete = DeleteRoleAdmin()
        for admin in role_admins:
            admin_delete_message = admin_delete.make(
                signer_keypair=key_pair,
                related_id=admin["related_id"],
                role_id=admin["role_id"],
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
    else:
        LOGGER.info("No role_admins found for role: %s", role_id)
    return txn_list


async def create_del_admin_by_user_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for an admin if user is an admin of any roles.
    Args:
           key_pair:
               obj: public and private keys for user
           next_id:
               str: next_id to search for the roles where user is the admin
           txn_list:
               list: transactions for batch submission
    Returns:
        txn_list:
            list: extended list of transactions for batch submission
    """
    conn = await create_connection()
    role_admins = (
        await r.table("role_admins")
        .filter({"related_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if role_admins:
        admin_delete = DeleteRoleAdmin()
        for admin in role_admins:
            admin_delete_message = admin_delete.make(
                signer_keypair=key_pair, related_id=next_id, role_id=admin["role_id"]
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
    else:
        LOGGER.info("No role_admins found for user: %s", next_id)
    return txn_list
