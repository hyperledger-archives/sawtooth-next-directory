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
"""Roles APIs."""
import os
from uuid import uuid4

from environs import Env
import rethinkdb as r
from sanic import Blueprint
from sanic.response import json

from rbac.common.logs import get_default_logger
from rbac.common.role import Role
from rbac.server.api import utils, proposals
from rbac.server.api.errors import (
    ApiTargetConflict,
    ApiNotFound,
    ApiForbidden,
    ApiInternalError,
    handle_not_found,
    handle_errors,
)
from rbac.server.api.auth import authorized
from rbac.server.api.proposals import PROPOSAL_TRANSACTION
from rbac.server.db import proposals_query
from rbac.server.db import roles_query
from rbac.server.db.relationships_query import fetch_relationships

from rbac.common.sawtooth import batcher
from rbac.server.blockchain_transactions.role_transaction import (
    create_del_role_txns,
    create_del_ownr_by_role_txns,
    create_del_admin_by_role_txns,
    create_del_mmbr_by_role_txns,
    create_rjct_ppsls_role_txns,
)
from rbac.server.api.utils import check_admin_status, check_role_owner_status
from rbac.server.db.db_utils import wait_for_resource_in_db

LDAP_DC = os.getenv("LDAP_DC")
GROUP_BASE_DN = os.getenv("GROUP_BASE_DN")
LOGGER = get_default_logger(__name__)

ROLES_BP = Blueprint("roles")


@ROLES_BP.get("api/roles")
@authorized()
async def get_all_roles(request):
    """Get all roles."""
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    role_resources = await roles_query.fetch_all_role_resources(
        request.app.config.DB_CONN, start, limit
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        role_resources,
        head_block,
        start=start,
        limit=limit,
    )


@ROLES_BP.post("api/roles")
@authorized()
async def create_new_role(request):
    """Create a new role."""
    required_fields = ["name", "administrators", "owners"]
    utils.validate_fields(required_fields, request.json)
    role_title = " ".join(request.json.get("name").split())
    response = await roles_query.roles_search_duplicate(
        request.app.config.DB_CONN, role_title
    )
    if request.json.get("metadata") is None or request.json.get("metadata") == {}:
        set_metadata = {}
    else:
        set_metadata = request.json.get("metadata")
    set_metadata["sync_direction"] = "OUTBOUND"
    if not response:
        txn_key, txn_user_id = await utils.get_transactor_key(request)
        role_id = str(uuid4())
        batch_list = Role().batch_list(
            signer_keypair=txn_key,
            signer_user_id=txn_user_id,
            name=role_title,
            role_id=role_id,
            metadata=set_metadata,
            admins=request.json.get("administrators"),
            owners=request.json.get("owners"),
            description=request.json.get("description"),
        )
        sawtooth_response = await utils.send(
            request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
        )

        if not sawtooth_response:
            LOGGER.warning("There was an error submitting the sawtooth transaction.")
            return await handle_errors(
                request,
                ApiInternalError(
                    "There was an error submitting the sawtooth transaction"
                ),
            )

        if role_title != "NextAdmins":
            distinguished_name_formatted = "CN=" + role_title + "," + GROUP_BASE_DN
            data_formatted = {
                "created_date": r.now(),
                "distinguished_name": distinguished_name_formatted,
                "group_nickname": role_title,
                "group_types": -2147483646,
                "name": role_title,
                "remote_id": distinguished_name_formatted,
            }

            env = Env()
            if env.int("ENABLE_LDAP_SYNC", 0):
                provider = env("LDAP_DC")
            elif env.int("ENABLE_AZURE_SYNC", 0):
                provider = env("TENANT_ID")
            else:
                provider = "NEXT-created"

            outbound_entry = {
                "data": data_formatted,
                "data_type": "group",
                "timestamp": r.now(),
                "provider_id": provider,
                "status": "UNCONFIRMED",
            }
            # Insert to outbound_queue and close
            await roles_query.insert_to_outboundqueue(
                request.app.config.DB_CONN, outbound_entry
            )
        else:
            LOGGER.info(
                "The role being created is NextAdmins, which is local to NEXT and will not be inserted into the outbound_queue."
            )
        return create_role_response(request, role_id)
    return await handle_errors(
        request,
        ApiTargetConflict(
            "Error: Could not create this role because the role name already exists."
        ),
    )


@ROLES_BP.get("api/roles/<role_id>")
@authorized()
async def get_role(request, role_id):
    """Get a specific role by role_id."""
    head_block = await utils.get_request_block(request)
    role_resource = await roles_query.fetch_role_resource(
        request.app.config.DB_CONN, role_id
    )
    return await utils.create_response(
        request.app.config.DB_CONN, request.url, role_resource, head_block
    )


@ROLES_BP.get("api/roles/check")
@authorized()
async def check_role_name(request):
    """Check if a role exists with provided name."""
    response = await roles_query.roles_search_duplicate(
        request.app.config.DB_CONN, request.args.get("name")
    )
    return json({"exists": bool(response)})


@ROLES_BP.patch("api/roles/<role_id>")
@authorized()
async def update_role(request, role_id):
    """Update a role."""
    required_fields = ["description"]
    utils.validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await utils.get_transactor_key(request)
    role_description = request.json.get("description")
    batch_list = Role().update.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        role_id=role_id,
        description=role_description,
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"id": role_id, "description": role_description})


@ROLES_BP.delete("api/roles/<role_id>")
@authorized()
async def delete_role(request, role_id):
    """Delete a role by it's next_id.
    Args:
        role_id:
            str: the role_id field of the targeted role
    Returns:
        json:
            dict: {
                message:
                    str: the status of the role delete operation
                deleted:
                    int: count of the number of roles that were deleted
            }
    Raises:
        ApiForbidden:
            The user is not a system admin or owner of the targeted
            role.
        ApiNotFound:
            The role does not exist in RethinkDB.
        ApiInternalError:
            There was an error compiling blockchain transactions.
    """
    txn_key, txn_user_id = await utils.get_transactor_key(request)

    # does the role exist?
    if not await roles_query.does_role_exist(request.app.config.DB_CONN, role_id):
        LOGGER.warning(
            "Nonexistent Role – User %s is attempting to delete the nonexistent role %s",
            txn_user_id,
            role_id,
        )
        return await handle_not_found(
            request, ApiNotFound("The targeted role does not exist.")
        )

    is_role_owner = await check_role_owner_status(txn_user_id, role_id)
    if not is_role_owner:
        is_admin = await check_admin_status(txn_user_id)
        if not is_admin:
            LOGGER.warning(
                "Permission Denied – User %s does not have sufficient privilege to delete role %s.",
                txn_user_id,
                role_id,
            )
            return await handle_errors(
                request, ApiForbidden("You do not have permission to delete this role.")
            )

    txn_list = []
    txn_list = await create_rjct_ppsls_role_txns(
        txn_key, role_id, txn_user_id, txn_list
    )
    txn_list = await create_del_admin_by_role_txns(txn_key, role_id, txn_list)
    txn_list = await create_del_mmbr_by_role_txns(txn_key, role_id, txn_list)
    txn_list = await create_del_ownr_by_role_txns(txn_key, role_id, txn_list)
    txn_list = create_del_role_txns(txn_key, role_id, txn_list)

    # validate transaction list
    if not txn_list:
        LOGGER.warning(
            "txn_list is empty. There was an error processing the delete role transactions. Transaction list: %s",
            txn_list,
        )
        return await handle_errors(
            request,
            ApiInternalError(
                "An error occurred while creating the blockchain transactions to delete the role."
            ),
        )

    batch = batcher.make_batch_from_txns(transactions=txn_list, signer_keypair=txn_key)
    batch_list = batcher.batch_to_list(batch=batch)
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json(
        {"message": "Role {} successfully deleted".format(role_id), "deleted": 1}
    )


@ROLES_BP.post("api/roles/<role_id>/admins")
@authorized()
async def add_role_admin(request, role_id):
    """Add an admin to role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    approver = await fetch_relationships("role_admins", "role_id", role_id).run(
        request.app.config.DB_CONN
    )
    batch_list = Role().admin.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        next_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
        assigned_approver=approver,
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


@ROLES_BP.post("api/roles/<role_id>/members")
@authorized()
async def add_role_member(request, role_id):
    """Add a member to a role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    approver = await fetch_relationships("role_owners", "role_id", role_id).run(
        request.app.config.DB_CONN
    )
    batch_list = Role().member.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        pack_id=request.json.get("pack_id"),
        next_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
        assigned_approver=approver,
    )
    batch_status = await utils.send(
        request.app.config.VAL_CONN,
        batch_list,
        request.app.config.TIMEOUT,
        request.json.get("tracker") and True,
    )
    role_resource = await roles_query.fetch_role_resource(
        request.app.config.DB_CONN, role_id
    )
    owners = role_resource.get("owners")
    requester_id = request.json.get("id")
    if requester_id in owners:
        is_proposal_ready = await wait_for_resource_in_db(
            "proposals", "proposal_id", proposal_id, max_attempts=30
        )
        if not is_proposal_ready:
            LOGGER.warning(
                "Max attempts exceeded. Proposal %s not found in RethinkDB.",
                proposal_id,
            )
            return await handle_errors(
                request,
                ApiInternalError(
                    "Max attempts exceeded. Proposal %s not found in RethinkDB."
                    % proposal_id
                ),
            )
        request.json["status"] = "APPROVED"
        request.json["reason"] = "I am the owner of this role"
        await proposals.update_proposal(request, proposal_id)
        if request.json.get("tracker"):
            events = {"batch_status": batch_status, "member_status": "MEMBER"}
            return utils.create_tracker_response(events)
        return json(
            {
                "message": "Owner is the requester. Proposal is autoapproved",
                "proposal_id": proposal_id,
            }
        )
    if request.json.get("tracker"):
        events = {"batch_status": batch_status}
        if batch_status == 1:
            events["member_status"] = "PENDING"
        return utils.create_tracker_response(events)
    return json({"proposal_id": proposal_id})


@ROLES_BP.post("api/roles/<role_id>/owners")
@authorized()
async def add_role_owner(request, role_id):
    """Add an owner to a role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    approver = await fetch_relationships("role_admins", "role_id", role_id).run(
        request.app.config.DB_CONN
    )
    batch_list = Role().owner.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        next_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
        assigned_approver=approver,
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


@ROLES_BP.post("api/roles/<role_id>/tasks")
@authorized()
async def add_role_task(request, role_id):
    """Add a task to a role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    approver = await fetch_relationships(
        "task_owners", "task_id", request.json.get("id")
    ).run(request.app.config.DB_CONN)
    batch_list = Role().task.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        task_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
        assigned_approver=approver,
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


async def reject_roles_proposals(role_id, request):
    """Reject a role's open proposals by role_id
    Args:
        role_id:
            str: a role id
        request:
            obj: a request object
    """
    # Get all open proposals associated with the role
    role_proposals = await proposals_query.fetch_open_proposals_by_role(
        request.app.config.DB_CONN, role_id
    )

    # Update to rejected:
    txn_key, txn_user_id = await utils.get_transactor_key(request=request)
    for proposal in role_proposals:
        if proposal["object_id"] == role_id:
            reason = "Role was deleted"
        else:
            reason = "Role does not exist anymore"
        batch_list = PROPOSAL_TRANSACTION[proposal["proposal_type"]][
            "REJECTED"
        ].batch_list(
            signer_keypair=txn_key,
            signer_user_id=txn_user_id,
            proposal_id=proposal["proposal_id"],
            object_id=proposal["object_id"],
            related_id=proposal["related_id"],
            reason=reason,
        )
        await utils.send(
            request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
        )


def create_role_response(request, role_id):
    """Compose the create new role response and return it as json."""
    role_resource = {
        "id": role_id,
        "name": request.json.get("name"),
        "owners": request.json.get("owners"),
        "administrators": request.json.get("administrators"),
        "members": [],
        "tasks": [],
        "proposals": [],
        "description": request.json.get("description"),
    }

    if request.json.get("metadata"):
        role_resource["metadata"] = request.json.get("metadata")
    return json({"data": role_resource})
