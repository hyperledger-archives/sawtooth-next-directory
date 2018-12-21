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

import binascii
import rethinkdb as r
from sanic.response import json

from sawtooth_sdk.protobuf import client_batch_submit_pb2
from sawtooth_sdk.protobuf import validator_pb2

from rbac.common.logs import get_logger
from rbac.common.crypto.secrets import decrypt_private_key
from rbac.common.crypto.secrets import deserialize_api_key
from rbac.server.api.errors import ApiBadRequest, ApiInternalError, ApiUnauthorized
from rbac.server.db import auth_query
from rbac.server.db import blocks_query
from rbac.common.crypto.keys import Key

LOGGER = get_logger(__name__)

SIGNATURE_KEY = "RBAC_AUTH_SIGNATURE"
PAYLOAD_KEY = "RBAC_AUTH_HEADER_PAYLOAD"


def validate_fields(required_fields, body):
    try:
        for field in required_fields:
            if body.get(field) is None:
                raise ApiBadRequest("Bad Request: {} field is required".format(field))
    except ValueError:
        raise ApiBadRequest("Bad Request: Improper JSON format")


def create_authorization_response(token, data):
    """Create destructured token response payload, splitting a
    token into its signature and payload components"""
    response = json({"data": data, "token": token})
    response.cookies[SIGNATURE_KEY] = ".".join(token.split(".")[0:2])
    response.cookies[PAYLOAD_KEY] = token.split(".")[2]

    response.cookies[SIGNATURE_KEY]["httponly"] = True
    return response


def extract_request_token(request):
    """If a request was initiated by the chatbot engine, retrieve
    the auth token directly from the slot field, otherwise return
    the Authorization header value or cookie token values."""

    if "Authorization" in request.headers:
        return request.headers["Authorization"]

    token_signature = request.cookies.get(SIGNATURE_KEY)
    token_payload = request.cookies.get(PAYLOAD_KEY)

    if token_signature and token_payload:
        return ".".join([token_signature, token_payload])

    try:
        return request.json["tracker"]["slots"]["token"]
    except (KeyError, TypeError):
        pass

    raise ApiUnauthorized("Unauthorized: No authentication token provided")


async def create_response(conn, request_url, data, head_block, start=None, limit=None):
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
    return json(response)


async def get_response_paging_info(conn, table, url, start, limit, head_block_num):
    total = await get_table_count(conn, table, head_block_num)

    prev_start = start - limit
    if prev_start < 0:
        prev_start = 0
    last_start = ((total - 1) // limit) * limit
    next_start = start + limit
    if next_start > last_start:
        next_start = last_start

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
    if table == "blocks":
        return (
            await r.table(table)
            .between(r.minval, head_block_num, right_bound="closed")
            .count()
            .run(conn)
        )
    return await r.table(table).count().run(conn)


def get_request_paging_info(request):
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
    try:
        head_block_id = request.args["head"][0]
        head_block = await blocks_query.fetch_block_by_id(
            request.app.config.DB_CONN, head_block_id
        )
    except KeyError:
        head_block = await blocks_query.fetch_latest_block_with_retry(
            request.app.config.DB_CONN, 5
        )
    return head_block


async def get_transactor_key(request):
    id_dict = deserialize_api_key(
        request.app.config.SECRET_KEY, extract_request_token(request)
    )
    user_id = id_dict.get("id")

    auth_data = await auth_query.fetch_info_by_user_id(
        request.app.config.DB_CONN, user_id
    )
    encrypted_private_key = auth_data.get("encrypted_private_key")
    private_key = decrypt_private_key(
        request.app.config.AES_KEY, user_id, encrypted_private_key
    )
    hex_private_key = binascii.hexlify(private_key)
    return Key(hex_private_key)


async def send(conn, batch_list, timeout):
    batch_request = client_batch_submit_pb2.ClientBatchSubmitRequest()
    batch_request.batches.extend(list(batch_list.batches))

    validator_response = await conn.send(
        validator_pb2.Message.CLIENT_BATCH_SUBMIT_REQUEST,
        batch_request.SerializeToString(),
        timeout,
    )

    client_response = client_batch_submit_pb2.ClientBatchSubmitResponse()
    client_response.ParseFromString(validator_response.content)

    if (
        client_response.status
        == client_batch_submit_pb2.ClientBatchSubmitResponse.INTERNAL_ERROR
    ):
        raise ApiInternalError("Internal Error")
    elif (
        client_response.status
        == client_batch_submit_pb2.ClientBatchSubmitResponse.INVALID_BATCH
    ):
        raise ApiBadRequest("Invalid Batch")
    elif (
        client_response.status
        == client_batch_submit_pb2.ClientBatchSubmitResponse.QUEUE_FULL
    ):
        raise ApiInternalError("Queue Full")

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

    if status_response.status != client_batch_submit_pb2.ClientBatchStatusResponse.OK:
        raise ApiInternalError("Internal Error")

    resp = status_response.batch_statuses[0]

    if resp.status == client_batch_submit_pb2.ClientBatchStatus.COMMITTED:
        return resp
    elif resp.status == client_batch_submit_pb2.ClientBatchStatus.INVALID:
        raise ApiBadRequest(
            "Bad Request: {}".format(resp.invalid_transactions[0].message)
        )
    elif resp.status == client_batch_submit_pb2.ClientBatchStatus.PENDING:
        raise ApiInternalError("Internal Error: Transaction submitted but timed out.")
    elif resp.status == client_batch_submit_pb2.ClientBatchStatus.UNKNOWN:
        raise ApiInternalError("Internal Error: Something went wrong. Try again later.")
