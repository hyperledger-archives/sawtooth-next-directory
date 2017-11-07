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
# -----------------------------------------------------------------------------

import logging


LOGGER = logging.getLogger(__name__)


def get_delta_handler(database):
    """Returns a delta handler with a reference to a specific Database object.
    The handler takes delta event and updates the Database appropriately.
    """
    return lambda delta: _handle_delta(database, delta)


def _handle_delta(database, delta):
    new_block = {'block_num': delta.block_num, 'block_id': delta.block_id}
    block_results = database.insert('blocks', new_block)
    if block_results['inserted'] == 0:
        LOGGER.warning(
            'Failed to insert block #%s: %s',
            delta.block_num,
            delta.block_id)
