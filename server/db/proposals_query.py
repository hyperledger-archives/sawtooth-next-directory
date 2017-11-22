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

import rethinkdb as r


LOGGER = logging.getLogger(__name__)


def fetch_proposal_ids_by_target(target, head_block_num):
    return r.table('proposals')\
        .get_all(target, index='target_id')\
        .filter(lambda doc:
                (head_block_num >= doc['start_block_num'])
                & (head_block_num < doc['end_block_num']))\
        .get_field('proposal_id')\
        .coerce_to('array')
