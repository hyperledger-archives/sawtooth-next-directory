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

import rethinkdb as r
from sanic import Blueprint
from sanic.response import json

from rbac.common.logs import get_default_logger
from rbac.common.role import Role
from rbac.server.api.errors import ApiBadRequest
from rbac.server.api.auth import authorized
from rbac.server.api import utils
from rbac.server.api import proposals

from rbac.server.db import roles_query
from rbac.server.db.db_utils import create_connection
from rbac.server.db.relationships_query import fetch_relationships

LDAP_DC = os.getenv("LDAP_DC")
GROUP_BASE_DN = os.getenv("GROUP_BASE_DN")

LOGGER = get_default_logger(__name__)

ROLES_BP = Blueprint("roles")


@ROLES_BP.get("api/roles")
@authorized()
async def get_all_roles(request):
    """Get all roles."""
    conn = await create_connection()

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    role_resources = await roles_query.fetch_all_role_resources(conn, start, limit)
    conn.close()
    return await utils.create_response(
        conn, request.url, role_resources, head_block, start=start, limit=limit
    )


@ROLES_BP.post("api/roles")
@authorized()
async def create_new_role(request):
    """Create a new role."""
    required_fields = ["name", "administrators", "owners"]
    utils.validate_fields(required_fields, request.json)
    conn = await create_connection()
    role_title = " ".join(request.json.get("name").split())
    response = await roles_query.roles_search_duplicate(conn, role_title)
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
        await utils.send(
            request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
        )
        conn.close()
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
            outbound_entry = {
                "data": data_formatted,
                "data_type": "group",
                "timestamp": r.now(),
                "provider_id": LDAP_DC,
            }
            # Insert to outbound_queue and close
            conn = await create_connection()
            role_outbound_resource = await roles_query.insert_to_outboundqueue(
                conn, outbound_entry
            )
            conn.close()
        else:
            LOGGER.info(
                "The role being created is NextAdmins, which is local to NEXT and will not be inserted into the outbound_queue."
            )
        return create_role_response(request, role_id)
    raise ApiBadRequest(
        "Error: Could not create this role because the role name already exists."
    )


@ROLES_BP.get("api/roles/<role_id>")
@authorized()
async def get_role(request, role_id):
    """Get a specific role by role_id."""
    conn = await create_connection()

    head_block = await utils.get_request_block(request)
    role_resource = await roles_query.fetch_role_resource(conn, role_id)
    conn.close()
    return await utils.create_response(conn, request.url, role_resource, head_block)


@ROLES_BP.get("api/roles/check")
@authorized()
async def check_role_name(request):
    """Check if a role exists with provided name."""
    conn = await create_connection()
    response = await roles_query.roles_search_duplicate(conn, request.args.get("name"))
    conn.close()
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


@ROLES_BP.post("api/roles/<role_id>/admins")
@authorized()
async def add_role_admin(request, role_id):
    """Add an admin to role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    conn = await create_connection()
    approver = await fetch_relationships("role_admins", "role_id", role_id).run(conn)
    conn.close()
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
    conn = await create_connection()
    approver = await fetch_relationships("role_owners", "role_id", role_id).run(conn)
    conn.close()
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
    conn = await create_connection()
    role_resource = await roles_query.fetch_role_resource(conn, role_id)
    owners = role_resource.get("owners")
    conn.close()
    requester_id = request.json.get("id")
    if requester_id in owners:
        request.json["status"] = "APPROVED"
        request.json["reason"] = "I am the owner of this role"
        await proposals.update_proposal(request, proposal_id)
        return json(
            {
                "message": "Owner is the requester. Proposal is autoapproved",
                "proposal_id": proposal_id,
            }
        )
    if request.json.get("tracker"):
        return utils.create_tracker_response("batch_status", batch_status)
    return json({"proposal_id": proposal_id})


@ROLES_BP.post("api/roles/<role_id>/owners")
@authorized()
async def add_role_owner(request, role_id):
    """Add an owner to a role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    conn = await create_connection()
    approver = await fetch_relationships("role_admins", "role_id", role_id).run(conn)
    conn.close()
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
    conn = await create_connection()
    approver = await fetch_relationships(
        "task_owners", "task_id", request.json.get("id")
    ).run(conn)
    conn.close()
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
