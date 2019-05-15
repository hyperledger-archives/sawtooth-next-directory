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
"""Users APIs."""
import os
from uuid import uuid4
import hashlib

from environs import Env
from sanic import Blueprint
from sanic.response import json

from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import encrypt_private_key, generate_api_key
from rbac.common.user import User
from rbac.server.api import utils
from rbac.server.api.auth import authorized
from rbac.server.api.errors import ApiBadRequest
from rbac.server.api.proposals import compile_proposal_resource
from rbac.server.db import auth_query
from rbac.server.db import proposals_query
from rbac.server.db import roles_query
from rbac.server.db import users_query
from rbac.server.db import packs_query
from rbac.server.db.db_utils import create_connection
from rbac.common.logs import get_default_logger
from rbac.common.sawtooth import batcher
from rbac.server.blockchain_transactions.delete_user_transaction import (
    create_delete_user_txns,
)
from rbac.server.blockchain_transactions.delete_role_owner_transaction import (
    create_delete_role_owner_txns,
)


LOGGER = get_default_logger(__name__)
AES_KEY = os.getenv("AES_KEY")
USERS_BP = Blueprint("users")


@USERS_BP.get("api/users")
@authorized()
async def fetch_all_users(request):
    """Returns all users."""
    conn = await create_connection()
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    user_resources = await users_query.fetch_all_user_resources(conn, start, limit)

    conn.close()

    return await utils.create_response(
        conn, request.url, user_resources, head_block, start=start, limit=limit
    )


@USERS_BP.post("api/users")
async def create_new_user(request):
    """Create a new user."""
    env = Env()
    admin_role = {
        "name": env("NEXT_ADMIN_NAME"),
        "username": env("NEXT_ADMIN_USER"),
        "email": env("NEXT_ADMIN_EMAIL"),
        "password": env("NEXT_ADMIN_PASS"),
    }
    if request.json != admin_role:
        if not env.int("ENABLE_NEXT_BASE_USE"):
            raise ApiBadRequest("Not a valid action. Source not enabled")
    required_fields = ["name", "username", "password", "email"]
    utils.validate_fields(required_fields, request.json)
    username_created = request.json.get("username")
    conn = await create_connection()
    # Check if username already exists
    if await users_query.fetch_username_match_count(conn, username_created) > 0:
        # Throw Error response to Next_UI
        raise ApiBadRequest(
            "Username already exists. Please give a different Username."
        )
    conn.close()

    # Generate keys
    key_pair = Key()
    next_id = str(uuid4())
    encrypted_private_key = encrypt_private_key(
        AES_KEY, key_pair.public_key, key_pair.private_key_bytes
    )
    if request.json.get("metadata") is None or request.json.get("metadata") == {}:
        set_metadata = {}
    else:
        set_metadata = request.json.get("metadata")
    set_metadata["sync_direction"] = "OUTBOUND"

    # Build create user transaction
    batch_list = User().batch_list(
        signer_keypair=key_pair,
        signer_user_id=next_id,
        next_id=next_id,
        name=request.json.get("name"),
        username=request.json.get("username"),
        email=request.json.get("email"),
        metadata=set_metadata,
        manager_id=request.json.get("manager"),
        key=key_pair.public_key,
    )

    # Submit transaction and wait for complete
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )

    # Save new user in auth table
    hashed_password = hashlib.sha256(
        request.json.get("password").encode("utf-8")
    ).hexdigest()

    auth_entry = {
        "next_id": next_id,
        "hashed_password": hashed_password,
        "encrypted_private_key": encrypted_private_key,
        "username": request.json.get("username"),
        "email": request.json.get("email"),
    }

    mapping_data = {
        "next_id": next_id,
        "provider_id": None,
        "remote_id": None,
        "public_key": key_pair.public_key,
        "encrypted_key": encrypted_private_key,
        "active": True,
    }

    # Insert to user_mapping and close
    conn = await create_connection()
    await auth_query.create_auth_entry(auth_entry)
    await users_query.create_user_map_entry(conn, mapping_data)
    conn.close()

    # Send back success response
    return create_user_response(request, next_id)


@USERS_BP.get("api/users/<next_id>")
@authorized()
async def get_user(request, next_id):
    """Get a specific user by next_id."""
    conn = await create_connection()
    head_block = await utils.get_request_block(request)
    # this takes 4 seconds
    user_resource = await users_query.fetch_user_resource(conn, next_id)
    conn.close()

    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.delete("api/users/<next_id>")
@authorized()
async def delete_user(request, next_id):
    """Delete a specific user by next_id."""

    txn_list = []
    txn_key, _ = await utils.get_transactor_key(request)
    txn_list = await create_delete_role_owner_txns(txn_key, next_id, txn_list)
    txn_list = create_delete_user_txns(txn_key, next_id, txn_list)

    if txn_list:
        batch = batcher.make_batch_from_txns(
            transactions=txn_list, signer_keypair=txn_key
        )
    batch_list = batcher.batch_to_list(batch=batch)

    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )

    conn = await create_connection()
    await auth_query.delete_auth_entry_by_next_id(conn, next_id)
    await roles_query.delete_role_admin_by_next_id(conn, next_id)
    await roles_query.delete_role_member_by_next_id(conn, next_id)
    await packs_query.delete_pack_owner_by_next_id(conn, next_id)
    await users_query.delete_metadata_by_next_id(conn, next_id)
    # TODO: We have to remove next_id reference entry from task table.
    conn.close()

    return json(
        {"message": "User {} successfully deleted".format(next_id), "deleted": 1}
    )


@USERS_BP.get("api/user/<next_id>/summary")
@authorized()
async def get_user_summary(request, next_id):
    """This endpoint is for returning summary data for a user, just it's next_id,name, email."""
    conn = await create_connection()
    head_block = await utils.get_request_block(request)
    user_resource = await users_query.fetch_user_resource_summary(conn, next_id)
    conn.close()

    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.get("api/users/<next_id>/summary")
@authorized()
async def get_users_summary(request, next_id):
    """This endpoint is for returning summary data for a user, just their next_id, name, email."""
    conn = await create_connection()
    head_block = await utils.get_request_block(request)
    user_resource = await users_query.fetch_user_resource_summary(conn, next_id)
    conn.close()

    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.get("api/users/<next_id>/relationships")
@authorized()
async def get_user_relationships(request, next_id):
    """Get relationships for a specific user, by next_id."""
    conn = await create_connection()
    head_block = await utils.get_request_block(request)
    user_resource = await users_query.fetch_user_relationships(conn, next_id)
    conn.close()
    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.put("api/users/<next_id>/manager")
@authorized()
async def update_manager(request, next_id):
    """Update a user's manager."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = User().manager.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        next_id=next_id,
        new_manager_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
        assigned_approver=[request.json.get("id")],
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


@USERS_BP.get("api/users/<next_id>/proposals/open")
@authorized()
async def fetch_open_proposals(request, next_id):
    """Get open proposals for a user, by their next_id."""
    conn = await create_connection()

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(conn, start, limit)
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(conn, proposal)
        proposal_resources.append(proposal_resource)

    open_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "OPEN"
            and next_id in proposal_resource["approvers"]
        ):
            open_proposals.append(proposal_resource)

    conn.close()

    return await utils.create_response(
        conn, request.url, open_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.get("api/users/<next_id>/proposals/confirmed")
@authorized()
async def fetch_confirmed_proposals(request, next_id):
    """Get confirmed proposals for a user, by their next_id."""
    conn = await create_connection()
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(conn, start, limit)
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(conn, proposal)
        proposal_resources.append(proposal_resource)

    confirmed_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "CONFIRMED"
            and next_id in proposal_resource["approvers"]
        ):
            confirmed_proposals.append(proposal_resource)

    conn.close()

    return await utils.create_response(
        conn, request.url, confirmed_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.get("api/users/<next_id>/proposals/rejected")
@authorized()
async def fetch_rejected_proposals(request, next_id):
    """Get confirmed proposals for a user, by their next_id."""
    conn = await create_connection()

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(conn, start, limit)
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(conn, proposal)
        proposal_resources.append(proposal_resource)

    rejected_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "REJECTED"
            and next_id in proposal_resource["approvers"]
        ):
            rejected_proposals.append(proposal_resource)

    conn.close()

    return await utils.create_response(
        conn, request.url, rejected_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.patch("api/users/<next_id>/roles/expired")
@authorized()
async def update_expired_roles(request, next_id):
    """Manually expire user role membership"""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    conn = await create_connection()
    await roles_query.expire_role_member(conn, request.json.get("id"), next_id)
    conn.close()
    return json({"role_id": request.json.get("id")})


def create_user_response(request, next_id):
    """Compose the json response for a create new user request."""
    token = generate_api_key(request.app.config.SECRET_KEY, next_id)
    user_resource = {
        "id": next_id,
        "name": request.json.get("name"),
        "username": request.json.get("username"),
        "email": request.json.get("email"),
        "ownerOf": [],
        "administratorOf": [],
        "memberOf": [],
        "proposals": [],
    }
    if request.json.get("manager"):
        user_resource["manager"] = request.json.get("manager")
    if request.json.get("metadata"):
        user_resource["metadata"] = request.json.get("metadata")
    return utils.create_authorization_response(
        token, {"message": "Authorization successful", "user": user_resource}
    )
