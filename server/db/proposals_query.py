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

from api.errors import ApiNotFound

import rethinkdb as r


LOGGER = logging.getLogger(__name__)


async def fetch_all_proposal_resources(conn, head_block_num, start, limit):
    return await r.table('proposals')\
        .order_by(index='proposal_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .slice(start, start+limit)\
        .map(lambda proposal: proposal.merge({
            'id': proposal['proposal_id'],
            'type': proposal['proposal_type'],
            'object': proposal['object_id'],
            'target': proposal['target_id']
        }))\
        .map(lambda proposal: (proposal['metadata'] == "").branch(
            proposal.without('metadata'), proposal
        ))\
        .without(
            'start_block_num',
            'end_block_num',
            'proposal_id',
            'proposal_type',
            'object_id',
            'target_id'
        )\
        .coerce_to('array').run(conn)


async def fetch_proposal_resource(conn, proposal_id, head_block_num):
    resource = await r.table('proposals')\
        .get_all(proposal_id, index='proposal_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .map(lambda proposal: proposal.merge({
            'id': proposal['proposal_id'],
            'type': proposal['proposal_type'],
            'object': proposal['object_id'],
            'target': proposal['target_id']
        }))\
        .map(lambda proposal: (proposal['metadata'] == "").branch(
            proposal.without('metadata'), proposal
        ))\
        .without(
            'start_block_num',
            'end_block_num',
            'proposal_id',
            'proposal_type',
            'object_id',
            'target_id'
        )\
        .coerce_to('array').run(conn)
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound(
            'Not Found: No proposal with the id {} exists'.format(proposal_id)
        )


def fetch_approver_ids(table, object_id, head_block_num):
    return r.table(table)\
        .get_all(object_id)\
        .filter(lambda doc:
                (head_block_num >= doc['start_block_num'])
                & (head_block_num < doc['end_block_num']))\
        .pluck('identifiers', 'manager')\
        .coerce_to('array')\
        .concat_map(lambda identifiers: identifiers)


def fetch_proposal_ids_by_target(target, head_block_num):
    return r.table('proposals')\
        .get_all(target, index='target_id')\
        .filter(lambda doc:
                (head_block_num >= doc['start_block_num'])
                & (head_block_num < doc['end_block_num']))\
        .get_field('proposal_id')\
        .coerce_to('array')

def fetch_proposal_ids_by_opener(opener, head_block_num):
    return r.table('proposals')\
        .get_all(opener, index='opener')\
        .filter(lambda doc:
                (head_block_num >= doc['start_block_num'])
                & (head_block_num < doc['end_block_num']))\
        .get_field('proposal_id')\
        .coerce_to('array')
