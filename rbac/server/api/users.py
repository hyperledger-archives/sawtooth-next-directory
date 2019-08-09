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
from itsdangerous import BadSignature
from sanic import Blueprint
from sanic.response import json
from sanic_openapi import doc

from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import encrypt_private_key, generate_api_key
from rbac.common.logs import get_default_logger
from rbac.common.sawtooth import batcher
from rbac.common.user import User
from rbac.server.api.auth import authorized
from rbac.server.api.errors import (
    ApiBadRequest,
    ApiDisabled,
    ApiForbidden,
    ApiInternalError,
    ApiTargetConflict,
    ApiUnauthorized,
    handle_errors,
)
from rbac.server.api.proposals import compile_proposal_resource, PROPOSAL_TRANSACTION
from rbac.server.api.utils import (
    check_admin_status,
    create_authorization_response,
    create_response,
    get_request_block,
    get_request_paging_info,
    get_transactor_key,
    log_request,
    send,
    send_notification,
    validate_fields,
)
from rbac.server.db import auth_query
from rbac.server.db import proposals_query
from rbac.server.db import roles_query
from rbac.server.db import users_query
from rbac.server.db.db_utils import create_connection
from rbac.server.blockchain_transactions.user_transaction import create_delete_user_txns
from rbac.server.blockchain_transactions.role_transaction import (
    create_del_ownr_by_user_txns,
    create_del_admin_by_user_txns,
    create_del_mmbr_by_user_txns,
)


LOGGER = get_default_logger(__name__)
AES_KEY = os.getenv("AES_KEY")
USERS_BP = Blueprint("users")


@USERS_BP.get("api/users")
@doc.summary("Returns all users.")
@doc.description("Returns all users.")
@doc.consumes({"head": str}, location="query")
@doc.consumes({"start": int}, location="query")
@doc.consumes({"limit": int}, location="query")
@doc.produces(
    {
        "data": [
            {
                "id": str,
                "name": str,
                "username": str,
                "distinguished_name": str,
                "created_date": int,
                "remote_id": str,
                "email": str,
                "ownerOf": {"tasks": [str], "roles": [str], "packs": [str]},
                "memberOf": [str],
                "proposals": {
                    "pack_id": str,
                    "object_id": str,
                    "status": str,
                    "proposal_id": str,
                },
                "manager": str,
                "metadata": dict,
            }
        ],
        "head": str,
        "link": str,
        "paging": {
            "first": str,
            "last": str,
            "limit": int,
            "next": str,
            "prev": str,
            "start": int,
            "total": int,
        },
    },
    content_type="application/json",
    description="A list of all users.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def fetch_all_users(request):
    """Returns all users."""
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)
    conn = await create_connection()
    user_resources = await users_query.fetch_all_user_resources(conn, start, limit)
    conn.close()

    return await create_response(
        conn, request.url, user_resources, head_block, start=start, limit=limit
    )


@USERS_BP.post("api/users")
@doc.summary("Create a new user.")
@doc.description(
    "Create a new user. Restricted to administrator use. Restricted to NEXT standalone mode."
)
@doc.consumes(
    doc.JsonBody({"name": str, "username": str, "password": str, "email": str}),
    location="body",
    content_type="application/json",
    required=True,
)
@doc.produces(
    {"data": {"user": {"id": str}}},
    content_type="application/json",
    description="The next_id of the newly created user.",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    403,
    {"message": str, "code": int},
    description="Forbidden: The provided credentials are not authorized to perform the requested action.",
)
@doc.response(
    409, {"message": str, "code": int}, description="Username already exists."
)
@doc.response(
    405,
    {"message": str, "code": int},
    description="Not a valid action. Source not enabled.",
)
@doc.response(
    503,
    {"message": str, "code": int},
    description="There was an error submitting the sawtooth transaction.",
)
async def create_new_user(request):
    """Create a new user. Must be an adminsitrator.

    Args:
        request:
            obj: incoming request object
    """
    log_request(request, True)
    # Validate that we have all fields
    required_fields = ["name", "username", "password", "email"]
    validate_fields(required_fields, request.json)
    # Check if username already exists
    conn = await create_connection()
    username = request.json.get("username")
    if await users_query.fetch_username_match_count(conn, username) > 0:
        # Throw Error response to Next_UI
        return await handle_errors(
            request, ApiTargetConflict("Username already exists.")
        )
    conn.close()

    # Check to see if they are trying to create the NEXT admin
    env = Env()
    next_admin = {
        "name": env("NEXT_ADMIN_NAME"),
        "username": env("NEXT_ADMIN_USER"),
        "email": env("NEXT_ADMIN_EMAIL"),
        "password": env("NEXT_ADMIN_PASS"),
    }
    if request.json != next_admin:
        # Try to see if they are in NEXT
        if not env.int("ENABLE_NEXT_BASE_USE"):
            raise ApiDisabled("Not a valid action. Source not enabled.")
        txn_key, txn_user_id, next_id, key_pair = await non_admin_creation(request)
    else:
        txn_key, txn_user_id, next_id, key_pair = await next_admin_creation(request)
    if request.json.get("metadata") is None:
        set_metadata = {}
    else:
        set_metadata = request.json.get("metadata")
    set_metadata["sync_direction"] = "OUTBOUND"
    # Build create user transaction
    batch_list = User().batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        next_id=next_id,
        name=request.json.get("name"),
        username=request.json.get("username"),
        email=request.json.get("email"),
        metadata=set_metadata,
        manager_id=request.json.get("manager"),
        key=key_pair.public_key,
    )

    # Submit transaction and wait for complete
    sawtooth_response = await send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    if not sawtooth_response:
        return await handle_errors(
            request,
            ApiInternalError("There was an error submitting the sawtooth transaction."),
        )

    # Save new user in auth table
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password = request.json.get("password").encode("utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", password, salt, 100000).hex()

    encrypted_private_key = encrypt_private_key(
        AES_KEY, key_pair.public_key, key_pair.private_key_bytes
    )
    auth_entry = {
        "next_id": next_id,
        "salt": salt,
        "hashed_password": hashed_password,
        "encrypted_private_key": encrypted_private_key,
        "username": request.json.get("username"),
        "email": request.json.get("email"),
    }

    mapping_data = {
        "next_id": next_id,
        "provider_id": "NEXT-created",
        "remote_id": None,
        "public_key": key_pair.public_key,
        "encrypted_key": encrypted_private_key,
        "active": True,
    }

    # Insert to user_mapping and close
    await auth_query.create_auth_entry(auth_entry)
    conn = await create_connection()
    await users_query.create_user_map_entry(conn, mapping_data)
    conn.close()

    # Send back success response
    return json({"data": {"user": {"id": next_id}}})


async def next_admin_creation(request):
    """Creating the admin user.  Used exclusively for the creation of the NEXT admin

    Args:
        request:
            obj: a request object
    """
    try:
        txn_key, txn_user_id = await get_transactor_key(request)
        is_admin = await check_admin_status(txn_user_id)
        if not is_admin:
            raise ApiUnauthorized(
                "You do not have the authorization to create an account."
            )
    except ApiUnauthorized:
        txn_key = Key()
        txn_user_id = str(uuid4())
    key_pair = txn_key
    next_id = txn_user_id
    return txn_key, txn_user_id, next_id, key_pair


async def non_admin_creation(request):
    """Creating non-admin users.

    Args:
        request:
            obj: a request object
    """
    try:
        txn_key, txn_user_id = await get_transactor_key(request)
        is_admin = await check_admin_status(txn_user_id)
        if not is_admin:
            raise ApiForbidden(
                "You do not have the authorization to create an account."
            )
        next_id = str(uuid4())
        key_pair = Key()
        return txn_key, txn_user_id, next_id, key_pair
    except BadSignature:
        raise ApiForbidden("You do not have the authorization to create an account.")


# TODO: Change → api/users/<next_id>
@USERS_BP.put("api/users/update")
@doc.summary("Update the details associated with a user.")
@doc.description(
    "Update the details associated with a user. Restricted to NEXT standalone mode. Restricted to administrator use."
)
@doc.consumes(
    doc.JsonBody({"next_id": str, "name": str, "username": str, "email": str}),
    location="body",
    content_type="application/json",
    required=True,
)
@doc.produces(
    {"message": str},
    content_type="application/json",
    description="User information was successfully updated.",
)
@doc.response(
    400, {"message": str, "code": int}, description="You are not a NEXT Administrator."
)
@doc.response(
    400,
    {"message": str, "code": int},
    description="Username already exists. Please give a different Username.",
)
@doc.response(400, {"message": str}, description="Bad Request: Improper JSON format.")
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    403,
    {"message": str, "code": int},
    description="Forbidden: The provided credentials are not authorized to perform the requested action.",
)
@doc.response(
    405,
    {"message": str, "code": int},
    description="This action is not enabled in this mode.",
)
@doc.response(
    503,
    {"message": str, "code": int},
    description="There was an error submitting the sawtooth transaction.",
)
@authorized()
async def update_user_details(request):
    """Update the details associated with a user.  This is NEXT admin only capability.

    Args:
        request:
            obj: request object from inbound request
    """
    log_request(request)
    # Checks for action viability
    env = Env()
    if not env.int("ENABLE_NEXT_BASE_USE", 0):
        raise ApiDisabled("This action is not enabled in this mode.")
    required_fields = ["next_id", "name", "username", "email"]
    validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await get_transactor_key(request)
    is_admin = await check_admin_status(txn_user_id)
    if not is_admin:
        raise ApiForbidden("You are not a NEXT Administrator.")
    conn = await create_connection()
    user = await users_query.users_search_duplicate(conn, request.json.get("username"))
    if user and user[0]["next_id"] != request.json.get("next_id"):
        conn.close()
        raise ApiBadRequest(
            "Username already exists. Please give a different Username."
        )

    # Get resources for update
    user_info = await users_query.fetch_user_resource(conn, request.json.get("next_id"))
    if "manager_id" in user_info:
        manager = user_info["manager_id"]
    else:
        manager = ""
    conn.close()
    if request.json.get("metadata") is None or request.json.get("metadata") == {}:
        set_metadata = {}
    else:
        set_metadata = request.json.get("metadata")
    set_metadata["sync_direction"] = "OUTBOUND"

    # Build and submit transaction
    batch_list = User().update.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        next_id=request.json.get("next_id"),
        name=request.json.get("name"),
        username=request.json.get("username"),
        email=request.json.get("email"),
        metadata=set_metadata,
        manager_id=manager,
    )
    await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)

    # Update_auth_table
    auth_updates = {
        "username": request.json.get("username"),
        "email": request.json.get("email"),
    }
    await auth_query.update_auth(request.json.get("next_id"), auth_updates)

    # Send back success response
    return json({"message": "User information was successfully updated."})


@USERS_BP.get("api/users/<next_id>")
@doc.summary("Get a specific user by next_id.")
@doc.description("Get a specific user by next_id.")
@doc.consumes({"head": str}, location="query")
@doc.produces(
    {
        "id": str,
        "name": str,
        "email": str,
        "subordinates": [str],
        "ownerOf": {"tasks": [str], "roles": [str], "packs": [str]},
        "administratorOf": {"tasks": [str], "roles": [str], "packs": [str]},
        "memberOf": [str],
        "proposals": [str],
        "expired": [str],
    },
    content_type="application/json",
    description="The matching user object.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def get_user(request, next_id):
    """Get a specific user by next_id."""
    log_request(request)
    head_block = await get_request_block(request)
    conn = await create_connection()
    user_resource = await users_query.fetch_user_resource(conn, next_id)
    conn.close()

    return await create_response(conn, request.url, user_resource, head_block)


@USERS_BP.delete("api/users/<next_id>")
@doc.summary("Delete a specific user by next_id.")
@doc.description("Delete a specific user by next_id.")
@doc.produces(
    {"message": str, "deleted": int},
    content_type="application/json",
    description="A user deletion status message.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    405,
    {"message": str, "code": int},
    description="Not a valid action. Source not enabled.",
)
@authorized()
async def delete_user(request, next_id):
    """Delete a specific user by next_id."""
    log_request(request)
    env = Env()
    if not env.int("ENABLE_NEXT_BASE_USE"):
        raise ApiDisabled("Not a valid action. Source not enabled.")
    txn_list = []
    txn_key, _ = await get_transactor_key(request)
    txn_list = await create_del_ownr_by_user_txns(txn_key, next_id, txn_list)
    txn_list = await create_del_admin_by_user_txns(txn_key, next_id, txn_list)
    txn_list = await create_del_mmbr_by_user_txns(txn_key, next_id, txn_list)
    txn_list = create_delete_user_txns(txn_key, next_id, txn_list)

    if txn_list:
        batch = batcher.make_batch_from_txns(
            transactions=txn_list, signer_keypair=txn_key
        )
    batch_list = batcher.batch_to_list(batch=batch)
    await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)

    await reject_users_proposals(next_id, request)

    return json(
        {"message": "User {} successfully deleted".format(next_id), "deleted": 1}
    )


# TODO: remap to `api/users/<next_id>/summary` and refactor client accordingly.
@USERS_BP.get("api/user/<next_id>/summary")
@doc.summary("Returns summary data for a user.")
@doc.description("Returns a user's next_id, name, and email fields.")
@doc.consumes({"head": str}, location="query")
@doc.produces(
    {
        "link": str,
        "data": {
            "remote_id": str,
            "email": str,
            "metadata": {},
            "id": str,
            "name": str,
            "username": str,
            "created_date": int,
            "distinguished_name": str,
        },
        "head": str,
    },
    content_type="application/json",
    description="A summarized user object.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    404,
    {"message": str, "code": int},
    description="Not Found: No user with the id <next_id> exists.",
)
@authorized()
async def get_user_summary(request, next_id):
    """This endpoint is for returning summary data for a user, just it's next_id,name, email."""
    log_request(request)
    head_block = await get_request_block(request)
    conn = await create_connection()
    user_resource = await users_query.fetch_user_resource_summary(conn, next_id)
    conn.close()

    return await create_response(conn, request.url, user_resource, head_block)


@USERS_BP.get("api/users/<next_id>/relationships")
@doc.summary("Get relationships for a specific user, by next_id.")
@doc.description("Get relationships for a specific user, by next_id.")
@doc.consumes({"head": str}, location="query")
@doc.produces(
    {
        "link": str,
        "data": {
            "managers": [str],
            "id": str,
            "direct_reports": [str],
            "peers": [str],
            "distinguished_name": str,
            "created_date": int,
        },
        "head": str,
    },
    content_type="application/json",
    description="Lists of direct reports, peers, and managers for the given user.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    404,
    {"message": str, "code": int},
    description="Not Found: No user with the id <next_id> exists.",
)
@authorized()
async def get_user_relationships(request, next_id):
    """Get relationships for a specific user, by next_id."""
    log_request(request)
    head_block = await get_request_block(request)
    conn = await create_connection()
    user_resource = await users_query.fetch_user_relationships(conn, next_id)
    conn.close()

    return await create_response(conn, request.url, user_resource, head_block)


@USERS_BP.put("api/users/<next_id>/manager")
@doc.summary("Update a user's manager.")
@doc.description("Update a user's manager.")
@doc.consumes(
    doc.JsonBody({"id": str}),
    location="body",
    content_type="application/json",
    required=True,
)
@doc.produces(
    {"proposal_id": str},
    content_type="application/json",
    description="The ID of the newly opened proposal to change the target user's manager.",
)
@doc.response(
    400,
    {"message": str, "code": int},
    description="Proposal opener is not a Next Admin.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    405,
    {"message": str, "code": int},
    description="Not a valid action. Source not enabled.",
)
@authorized()
async def update_manager(request, next_id):
    """Update a user's manager."""
    log_request(request)
    env = Env()
    if not env.int("ENABLE_NEXT_BASE_USE"):
        raise ApiDisabled("Not a valid action. Source not enabled")
    required_fields = ["id"]
    validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await get_transactor_key(request)
    proposal_id = str(uuid4())
    if await check_admin_status(txn_user_id):
        conn = await create_connection()
        next_admins_list = await users_query.get_next_admins(conn)
        conn.close()
        batch_list = User().manager.propose.batch_list(
            signer_keypair=txn_key,
            signer_user_id=txn_user_id,
            proposal_id=proposal_id,
            next_id=next_id,
            new_manager_id=request.json.get("id"),
            reason=request.json.get("reason"),
            metadata=request.json.get("metadata"),
            assigned_approver=next_admins_list,
        )
        await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)
        await send_notification(request.json.get("id"), proposal_id)
    else:
        raise ApiBadRequest("Proposal opener is not a Next Admin.")
    return json({"proposal_id": proposal_id})


@USERS_BP.put("api/users/password")
@doc.summary("Update a user's password.")
@doc.description(
    "Update a user's password. Restricted to administrator use. Restricted to NEXT standalone mode."
)
@doc.consumes(
    doc.JsonBody({"next_id": str, "password": str}),
    location="body",
    content_type="application/json",
    required=True,
)
@doc.produces(
    {"message": str},
    content_type="application/json",
    description="Password update status message.",
)
@doc.response(
    400, {"message": str, "code": int}, description="You are not a NEXT Administrator."
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    403,
    {"message": str, "code": int},
    description="Forbidden: The provided credentials are not authorized to perform the requested action.",
)
@doc.response(
    405,
    {"message": str, "code": int},
    description="Not a valid action. Source not enabled.",
)
@authorized()
async def update_password(request):
    """Update a user's password.  The request must come from an admin.
    Args:
        request:
            obj: a request object
    """
    log_request(request)
    env = Env()
    if not env.int("ENABLE_NEXT_BASE_USE"):
        raise ApiDisabled("Not a valid action. Source not enabled")
    required_fields = ["next_id", "password"]
    validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await get_transactor_key(request)
    is_admin = await check_admin_status(txn_user_id)
    if not is_admin:
        raise ApiBadRequest("You are not a NEXT Administrator.")

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password = request.json.get("password").encode("utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", password, salt, 100000).hex()

    conn = await create_connection()
    await users_query.update_user_password(
        conn, request.json.get("next_id"), hashed_password=hashed_password, salt=salt
    )
    conn.close()
    return json({"message": "Password successfully updated"})


@USERS_BP.get("api/users/<next_id>/proposals/open")
@doc.summary("Get open proposals for a user, by their next_id.")
@doc.description("Get open proposals for a user, by their next_id.")
@doc.consumes({"head": str}, location="query")
@doc.consumes({"start": int}, location="query")
@doc.consumes({"limit": int}, location="query")
@doc.produces(
    {
        "link": str,
        "paging": {
            "last": str,
            "next": str,
            "first": str,
            "limit": int,
            "total": int,
            "start": int,
            "prev": str,
        },
        "data": [
            {
                "close_reason": str,
                "target": str,
                "id": str,
                "pack_id": str,
                "assigned_approver": [str],
                "approvers": [str],
                "created_date": int,
                "object": str,
                "status": str,
                "open_reason": str,
                "metadata": {},
                "closer": str,
                "opener": str,
                "type": str,
            }
        ],
        "head": str,
    },
    content_type="Application/json",
    description="List of open proposals the given user has opened.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def fetch_open_proposals(request, next_id):
    """Get open proposals for a user, by their next_id.
    Args:
        request:
            obj: request object to api
        next_id:
            str: next_id of user for open proposals as assigned_approval
    """
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)
    conn = await create_connection()
    proposals = await proposals_query.fetch_all_proposal_resources(conn, start, limit)
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(conn, proposal)
        proposal_resources.append(proposal_resource)
    conn.close()
    open_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "OPEN"
            and next_id in proposal_resource["assigned_approver"]
        ):
            open_proposals.append(proposal_resource)

    return await create_response(
        conn, request.url, open_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.get("api/users/<next_id>/proposals/confirmed")
@doc.summary("Get confirmed proposals for a user, by their next_id.")
@doc.description("Get confirmed proposals for a user, by their next_id.")
@doc.consumes({"head": str}, location="query")
@doc.consumes({"start": int}, location="query")
@doc.consumes({"limit": int}, location="query")
@doc.produces(
    {
        "link": str,
        "paging": {
            "last": str,
            "next": str,
            "first": str,
            "limit": int,
            "total": int,
            "start": int,
            "prev": str,
        },
        "data": [
            {
                "close_reason": str,
                "target": str,
                "id": str,
                "pack_id": str,
                "assigned_approver": [str],
                "approvers": [str],
                "created_date": int,
                "object": str,
                "closed_date": int,
                "status": str,
                "open_reason": str,
                "metadata": {},
                "closer": str,
                "opener": str,
                "type": str,
            }
        ],
        "head": str,
    },
    content_type="Application/json",
    description="List of confirmed proposals the given user has opened.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def fetch_confirmed_proposals(request, next_id):
    """Get confirmed proposals for a user, by their next_id."""
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)
    conn = await create_connection()
    proposals = await proposals_query.fetch_all_proposal_resources(conn, start, limit)
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(conn, proposal)
        proposal_resources.append(proposal_resource)
    conn.close()

    confirmed_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "CONFIRMED"
            and next_id in proposal_resource["approvers"]
        ):
            confirmed_proposals.append(proposal_resource)

    return await create_response(
        conn, request.url, confirmed_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.get("api/users/<next_id>/proposals/rejected")
@doc.summary("Get rejected proposals for a user, by their next_id.")
@doc.description("Get rejected proposals for a user, by their next_id.")
@doc.consumes({"head": str}, location="query")
@doc.consumes({"start": int}, location="query")
@doc.consumes({"limit": int}, location="query")
@doc.produces(
    {
        "link": str,
        "paging": {
            "last": str,
            "next": str,
            "first": str,
            "limit": int,
            "total": int,
            "start": int,
            "prev": str,
        },
        "data": [
            {
                "close_reason": str,
                "target": str,
                "id": str,
                "pack_id": str,
                "assigned_approver": [str],
                "approvers": [str],
                "created_date": int,
                "object": str,
                "closed_date": int,
                "status": str,
                "open_reason": str,
                "metadata": {},
                "closer": str,
                "opener": str,
                "type": str,
            }
        ],
        "head": str,
    },
    content_type="Application/json",
    description="List of confirmed proposals the given user has opened.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def fetch_rejected_proposals(request, next_id):
    """Get confirmed proposals for a user, by their next_id."""
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)
    conn = await create_connection()
    proposals = await proposals_query.fetch_all_proposal_resources(conn, start, limit)
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(conn, proposal)
        proposal_resources.append(proposal_resource)
    conn.close()

    rejected_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "REJECTED"
            and next_id in proposal_resource["approvers"]
        ):
            rejected_proposals.append(proposal_resource)

    return await create_response(
        conn, request.url, rejected_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.patch("api/users/<next_id>/roles/expired")
@doc.summary("Manually expire a user's role membership.")
@doc.description("Manually expire a user's role membership.")
@doc.consumes(
    doc.JsonBody({"id": str}),
    location="body",
    content_type="application/json",
    required=True,
)
@doc.produces(
    {"role_id": str},
    content_type="application/json",
    description="The next_id of the targeted role.",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def update_expired_roles(request, next_id):
    """Manually expire user role membership"""
    log_request(request)
    required_fields = ["id"]
    validate_fields(required_fields, request.json)

    conn = await create_connection()
    await roles_query.expire_role_member(conn, request.json.get("id"), next_id)
    conn.close()
    return json({"role_id": request.json.get("id")})


async def reject_users_proposals(next_id, request):
    """Reject a users open proposals via next_id if they are the opener or assigned_approver
    Args:
        next_id:
            str: a users id
        request:
            obj: a request object
    """
    # Get all open proposals associated with the user
    conn = await create_connection()
    proposals = await proposals_query.fetch_open_proposals_by_user(conn, next_id)
    conn.close()

    # Update to rejected:
    txn_key, txn_user_id = await get_transactor_key(request=request)
    for proposal in proposals:
        if proposal["opener"] == next_id:
            reason = "Opener was deleted"
        else:
            reason = "Assigned Appover was deleted."

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
        await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)


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
    return create_authorization_response(
        token, {"message": "Authorization successful", "user": user_resource}
    )


@USERS_BP.get("api/users/check")
@doc.summary("Check if a user exists with provided username.")
@doc.description("Check if a user exists with provided username.")
@doc.consumes({"username": str}, location="query", required=False)
@doc.produces(
    {"exists": bool},
    content_type="application/json",
    description="User existence status.",
)
async def check_user_name(request):
    """Check if a user exists with provided username."""
    log_request(request)
    conn = await create_connection()
    response = await users_query.users_search_duplicate(
        conn, request.args.get("username")
    )
    conn.close()
    return json({"exists": bool(response)})
