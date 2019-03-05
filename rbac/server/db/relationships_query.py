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

import rethinkdb as r

from rbac.common.logs import get_default_logger


LOGGER = get_default_logger(__name__)


def fetch_relationships(table, index, identifier):
    return (
        r.table(table)
        .get_all(identifier, index=index)
        .get_field("identifiers")
        .coerce_to("array")
        .concat_map(lambda identifiers: identifiers)
    )


def fetch_relationships_by_id(table, identifier, key):
    return (
        r.table(table)
        .filter(lambda doc: doc["identifiers"].contains(identifier), default=True)
        .get_field(key)
        .distinct()
        .coerce_to("array")
    )
