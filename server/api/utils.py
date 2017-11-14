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

from api.errors import ApiBadRequest, ApiInternalError

from sanic.response import json

from sawtooth_rest_api.protobuf import client_pb2
from sawtooth_rest_api.protobuf import validator_pb2

from db import blocks_query


LOGGER = logging.getLogger(__name__)


def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest(
                "Bad Request: {} field is required".format(field)
            )


async def create_response(conn, data, head_block_num):
    head_block = await blocks_query.fetch_block_by_num(conn, head_block_num)
    link = ''
    response = {
        'data': data,
        'head': head_block.get('block_id'),
        'link': link
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
