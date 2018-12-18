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
# ------------------------------------------------------------------------------

import logging

import rethinkdb as r


LOGGER = logging.getLogger(__name__)


def fetch_relationships(table, index, identifier, head_block_num):
    return (
        r.table(table)
        .get_all(identifier, index=index)
        .get_field("identifiers")
        .coerce_to("array")
        .concat_map(lambda identifiers: identifiers)
    )


def fetch_relationships_by_id(table, identifier, key, head_block_num):
    return (
        r.table(table)
        .filter(lambda doc: doc["identifiers"].contains(identifier), default=True)
        .get_field(key)
        .distinct()
        .coerce_to("array")
    )
