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
from rbac.server.api.errors import ApiNotFound
from rbac.server.db.proposals_query import fetch_proposal_ids_by_opener
from rbac.server.db.relationships_query import (
    fetch_relationships,
    fetch_relationships_by_id,
)

LOGGER = get_default_logger(__name__)


async def fetch_all_task_resources(conn, start, limit):
    resources = (
        await r.table("tasks")
        .order_by(index="task_id")
        .slice(start, start + limit)
        .map(
            lambda task: task.merge(
                {
                    "id": task["task_id"],
                    "owners": fetch_relationships(
                        "task_owners", "task_id", task["task_id"]
                    ),
                    "administrators": fetch_relationships(
                        "task_admins", "task_id", task["task_id"]
                    ),
                    "roles": fetch_relationships_by_id(
                        "role_tasks", task["task_id"], "role_id"
                    ),
                    "proposals": fetch_proposal_ids_by_opener(task["task_id"]),
                }
            )
        )
        .without("task_id")
        .coerce_to("array")
        .run(conn)
    )
    return resources


async def fetch_task_resource(conn, task_id):
    resource = (
        await r.table("tasks")
        .get_all(task_id, index="task_id")
        .merge(
            {
                "id": r.row["task_id"],
                "owners": fetch_relationships("task_owners", "task_id", task_id),
                "administrators": fetch_relationships(
                    "task_admins", "task_id", task_id
                ),
                "roles": fetch_relationships_by_id("role_tasks", task_id, "role_id"),
                "proposals": fetch_proposal_ids_by_opener(task_id),
            }
        )
        .without("task_id")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No task with the id {} exists".format(task_id))
