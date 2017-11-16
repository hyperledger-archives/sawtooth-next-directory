# Copyright 2017 Intel Corporation
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

import logging

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from Crypto.Cipher import AES

from sanic.response import json

from sawtooth_rest_api.protobuf import client_pb2
from sawtooth_rest_api.protobuf import validator_pb2

from api.errors import ApiBadRequest, ApiInternalError

from db import auth_query
from db import blocks_query

from rbac_transaction_creation.common import Key


LOGGER = logging.getLogger(__name__)


def validate_fields(required_fields, body):
    try:
        for field in required_fields:
            if body.get(field) is None:
                raise ApiBadRequest(
                    "Bad Request: {} field is required".format(field)
                )
    except ValueError:
        raise ApiBadRequest("Bad Request: Improper JSON format")


async def create_response(conn, url, data, head_block_num):
    head_block = await blocks_query.fetch_block_by_num(conn, head_block_num)
    head_block_id = head_block.get('block_id')
    if '?head=' not in url:
        url += '?head={}'.format(head_block_id)
    response = {
        'data': data,
        'head': head_block_id,
        'link': url
    }
    return json(response)


async def get_request_block_num(request):
    try:
        head_block_id = request.args['head'][0]
        head_block = await blocks_query.fetch_block_by_id(
            request.app.config.DB_CONN,
            head_block_id
        )
    except KeyError:
        head_block = await blocks_query.fetch_latest_block(
            request.app.config.DB_CONN
        )
    return head_block.get('block_num')


async def get_transactor_key(request):
    id_dict = deserialize_apikey(
        request.app.config.SECRET_KEY,
        request.token
    )
    user_id = id_dict.get('id')

    auth_data = await auth_query.fetch_info_by_user_id(
        request.app.config.DB_CONN, user_id
    )
    encrypted_private_key = auth_data.get('encrypted_private_key')
    private_key = decrypt_private_key(
        request.app.config.AES_KEY,
        user_id,
        encrypted_private_key
    )
    return Key(user_id, private_key)


def generate_apikey(secret_key, user_id):
    serializer = Serializer(secret_key)
    token = serializer.dumps({'id': user_id})
    return token.decode('ascii')


def deserialize_apikey(secret_key, token):
    serializer = Serializer(secret_key)
    return serializer.loads(token)


def decrypt_private_key(aes_key, user_id, encrypted_private_key):
    init_vector = bytes.fromhex(user_id[:32])
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, init_vector)
    return cipher.decrypt(encrypted_private_key)


def encrypt_private_key(aes_key, user_id, private_key):
    init_vector = bytes.fromhex(user_id[:32])
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, init_vector)
    return cipher.encrypt(private_key)


async def send(conn, batch_list, timeout):
    batch_request = client_pb2.ClientBatchSubmitRequest()
    batch_request.batches.extend(list(batch_list.batches))
    batch_request.wait_for_commit = True

    validator_response = await conn.send(
        validator_pb2.Message.CLIENT_BATCH_SUBMIT_REQUEST,
        batch_request.SerializeToString(), timeout
    )

    client_response = client_pb2.ClientBatchSubmitResponse()
    client_response.ParseFromString(validator_response.content)
    resp = client_response.batch_statuses[0]

    if resp.status == client_pb2.BatchStatus.COMMITTED:
        return resp
    elif resp.status == client_pb2.BatchStatus.INVALID:
        raise ApiBadRequest('Bad Request: {}'.format(
            resp.invalid_transactions[0].message
        ))
    elif resp.status == client_pb2.BatchStatus.PENDING:
        raise ApiInternalError(
            'Internal Error: Transaction submitted but timed out.'
        )
    elif resp.status == client_pb2.BatchStatus.UNKNOWN:
        raise ApiInternalError(
            'Internal Error: Something went wrong. Try again later.'
        )
