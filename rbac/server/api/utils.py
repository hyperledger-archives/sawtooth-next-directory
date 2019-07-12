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
"""Utility functions to support APIs."""
import binascii
import datetime as dt
import rethinkdb as r

from sanic.response import json
from sawtooth_sdk.protobuf import client_batch_submit_pb2
from sawtooth_sdk.protobuf import validator_pb2

from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import decrypt_private_key, deserialize_api_key
from rbac.common.logs import get_default_logger
from rbac.server.api.errors import ApiBadRequest, ApiInternalError, ApiUnauthorized
from rbac.server.db import blocks_query
from rbac.server.db.auth_query import get_auth_by_next_id
from rbac.server.db.db_utils import create_connection
from rbac.server.db.roles_query import (
    get_role_by_name,
    get_role_membership,
    fetch_role_owners,
)


LOGGER = get_default_logger(__name__)


def validate_fields(required_fields, body):
    """Checks that all required_fields are in body, raises exception if not."""
    try:
        for field in required_fields:
            if body.get(field) is None:
                raise ApiBadRequest("Bad Request: {} field is required".format(field))
    except ValueError:
        raise ApiBadRequest("Bad Request: Improper JSON format")


def create_authorization_response(token, data):
    """Create authentication response payload"""
    response = json({"data": data, "token": token})
    return response


def extract_request_token(request):
    """If a request was initiated by the chatbot engine, retrieve
    the auth token directly from the tracker slot. Otherwise return
    the 'Authorization' header token."""

    if request.token is not None:
        return request.token
    try:
        return request.json["tracker"]["slots"]["token"]
    except (KeyError, TypeError):
        pass

    raise ApiUnauthorized("Unauthorized: No authentication token provided")


async def create_response(conn, request_url, data, head_block, start=None, limit=None):
    """Creates json response."""
    conn.reconnect(noreply_wait=False)

    base_url = request_url.split("?")[0]
    table = base_url.split("/")[4]
    url = "{}?head={}".format(base_url, head_block.get("id"))
    response = {
        "data": data,
        "head": head_block.get("id"),
        "link": "{}&start={}&limit={}".format(url, start, limit),
    }
    if start is not None and limit is not None:
        response["paging"] = await get_response_paging_info(
            conn, table, url, start, limit, head_block.get("num")
        )
    conn.close()
    return json(response)


def create_tracker_response(events):
    """Create JSON event payload used to modify the chatbot tracker"""
    response = {"events": []}
    for name, value in events.items():
        response["events"].append({"event": "slot", "name": name, "value": value})
    return json(response)


async def get_response_paging_info(conn, table, url, start, limit, head_block_num):
    """Get paging info for paged responses."""
    conn.reconnect(noreply_wait=False)

    total = await get_table_count(conn, table, head_block_num)

    prev_start = start - limit
    if prev_start < 0:
        prev_start = 0
    last_start = ((total - 1) // limit) * limit
    next_start = start + limit
    if next_start > last_start:
        next_start = last_start

    conn.close()

    return {
        "start": start,
        "limit": limit,
        "total": total,
        "first": "{}&start=0&limit={}".format(url, limit),
        "prev": "{}&start={}&limit={}".format(url, prev_start, limit),
        "next": "{}&start={}&limit={}".format(url, next_start, limit),
        "last": "{}&start={}&limit={}".format(url, last_start, limit),
    }


async def get_table_count(conn, table, head_block_num):
    """Get count of items in table."""
    conn.reconnect(noreply_wait=False)

    if table == "blocks":
        table_count = await (
            r.table(table)
            .between(r.minval, head_block_num, right_bound="closed")
            .count()
            .run(conn)
        )
        conn.close()
        return table_count
    table_count = await r.table(table).count().run(conn)
    conn.close()
    return table_count


def get_request_paging_info(request):
    """Get paging start/limit out of request."""
    try:
        start = int(request.args["start"][0])
    except KeyError:
        start = 0
    try:
        limit = int(request.args["limit"][0])
        if limit > 1000:
            limit = 1000
    except KeyError:
        limit = 100
    return start, limit


async def get_request_block(request):
    """Get headblock from request or newest."""
    conn = await create_connection()
    try:
        head_block_id = request.args["head"][0]
        head_block = await blocks_query.fetch_block_by_id(conn, head_block_id)
    except KeyError:
        head_block = await blocks_query.fetch_latest_block_with_retry(conn, 5)
    conn.close()
    return head_block


async def get_transactor_key(request):
    """Get transactor key out of request."""
    id_dict = deserialize_api_key(
        request.app.config.SECRET_KEY, extract_request_token(request)
    )
    next_id = id_dict.get("id")

    auth_data = await get_auth_by_next_id(next_id)
    encrypted_private_key = auth_data.get("encrypted_private_key")
    private_key = decrypt_private_key(
        request.app.config.AES_KEY, next_id, encrypted_private_key
    )
    hex_private_key = binascii.hexlify(private_key)
    return Key(hex_private_key), next_id


async def send(conn, batch_list, timeout, webhook=False):
    """Send batch_list to sawtooth."""
    batch_request = client_batch_submit_pb2.ClientBatchSubmitRequest()
    batch_request.batches.extend(list(batch_list.batches))
    validator_response = await conn.send(
        validator_pb2.Message.CLIENT_BATCH_SUBMIT_REQUEST,
        batch_request.SerializeToString(),
        timeout,
    )
    client_response = client_batch_submit_pb2.ClientBatchSubmitResponse()
    client_response.ParseFromString(validator_response.content)
    status = client_response.status

    if not webhook:
        if status == client_batch_submit_pb2.ClientBatchSubmitResponse.INTERNAL_ERROR:
            raise ApiInternalError("Internal Error")
        elif status == client_batch_submit_pb2.ClientBatchSubmitResponse.INVALID_BATCH:
            raise ApiBadRequest("Invalid Batch")
        elif status == client_batch_submit_pb2.ClientBatchSubmitResponse.QUEUE_FULL:
            raise ApiInternalError("Queue Full")
    elif status != client_batch_submit_pb2.ClientBatchSubmitResponse.OK:
        return None

    status_request = client_batch_submit_pb2.ClientBatchStatusRequest()
    status_request.batch_ids.extend(
        list(b.header_signature for b in batch_list.batches)
    )
    status_request.wait = True
    status_request.timeout = timeout
    validator_response = await conn.send(
        validator_pb2.Message.CLIENT_BATCH_STATUS_REQUEST,
        status_request.SerializeToString(),
        timeout,
    )
    status_response = client_batch_submit_pb2.ClientBatchStatusResponse()
    status_response.ParseFromString(validator_response.content)
    status = status_response.status

    if not webhook:
        if status != client_batch_submit_pb2.ClientBatchStatusResponse.OK:
            raise ApiInternalError("Internal Error")
    elif status != client_batch_submit_pb2.ClientBatchStatusResponse.OK:
        return None

    response = status_response.batch_statuses[0]
    status = response.status

    if not webhook:
        if status == client_batch_submit_pb2.ClientBatchStatus.INVALID:
            raise ApiBadRequest(
                "Bad Request: {}".format(response.invalid_transactions[0].message)
            )
        elif status == client_batch_submit_pb2.ClientBatchStatus.PENDING:
            raise ApiInternalError("Internal Error: Transaction timed out.")
        elif status == client_batch_submit_pb2.ClientBatchStatus.UNKNOWN:
            raise ApiInternalError("Internal Error: Unspecified error.")
    return status


async def check_admin_status(next_id):
    """Verfiy that a user is a member of NEXT admins.  Return boolean.
    Args:
        next_id:
            str: user's next_id
    """
    conn = await create_connection()
    admin_role = await get_role_by_name(conn, "NextAdmins")
    if not admin_role:
        raise ApiInternalError("NEXT administrator group has not been created.")
    admin_membership = await get_role_membership(
        conn, next_id, admin_role[0]["role_id"]
    )
    conn.close()
    if admin_membership:
        return True
    return False


async def check_role_owner_status(next_id, role_id):
    """Verify that the given user is an owner of the given role.
    Args:
        next_id:
            str: The next_id of a given user to check status of.
        role_id:
            str: The next_id of a given role to query against.
    Returns:
        owner_status:
            bool: Returns True if the next_id is in the role's owner list.
                Returns False if the next_id is NOT in the role's owner list.
    """
    with await create_connection() as conn:
        role_owners = await fetch_role_owners(conn, role_id)
        return bool(next_id in role_owners)


async def send_notification(next_id, proposal_id, frequency=0):
    """Send an entry to the notifications table for notification queue

    Args:
        next_id:
            str: id for the user that is to be sent a notification
        proposal_id:
            str: id of a proposal user is to be notified about
        frequency:
            int: number representing time """
    conn = await create_connection()
    notification = (
        await r.table("notifications")
        .insert(
            {
                "next_id": next_id,
                "proposal_id": proposal_id,
                "frequency": frequency,
                "timestamp": r.now(),
            }
        )
        .run(conn)
    )
    conn.close()
    return notification


def log_request(request, sensitive=False):
    """Utility logger for all requests to be logged to file.

    Args:
        request:
            obj: incoming request object
        sensitive:
            bool: contains info that should not be logged
    """
    if sensitive:
        LOGGER.info("A request was made at %s to %s", dt.datetime.now(), request.url)
        return
    LOGGER.info(
        "The following request (%s) was made at %s with a payload of: %s",
        request,
        dt.datetime.now(),
        request.json,
    )
