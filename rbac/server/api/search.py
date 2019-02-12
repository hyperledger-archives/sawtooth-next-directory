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
import math

from sanic import Blueprint
from sanic.response import json

from rbac.common.logs import get_logger
from rbac.server.api.auth import authorized
from rbac.server.db import db_utils
from rbac.server.db.packs_query import search_packs, search_packs_count
from rbac.server.db.roles_query import search_roles, search_roles_count
from rbac.server.db.users_query import search_users, search_users_count

LOGGER = get_logger(__name__)
SEARCH_BP = Blueprint("search")


@SEARCH_BP.post("api/search")
@authorized()
async def search_all(request):
    """API Endpoint to get all roles, packs, or users containing a string."""
    search_query = request.json.get("query")

    # Check for valid payload containing query and search object types
    if search_query is None:
        errors = {"errors": "No query parameter recieved."}
        return json(errors)
    if "search_object_types" not in search_query:
        errors = {"errors": "No search_object_types for search recieved."}
        return json(errors)
    if "search_input" not in search_query:
        errors = {"errors": "No search_input string for search recieved."}
        return json(errors)

    # Create response data object
    data = {"packs": [], "roles": [], "users": []}

    # Pagination and total pages
    try:
        paging = search_paginate(
            int(search_query["page_size"]), int(search_query["page"])
        )
    except KeyError:
        paging = (0, 50)

    object_counts = []

    # Run search queries
    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )
    if "pack" in search_query["search_object_types"]:
        # Fetch packs with search input string

        pack_results = await search_packs(conn, search_query, paging)
        data["packs"] = pack_results
        object_counts.append(await search_packs_count(conn, search_query))

    if "role" in search_query["search_object_types"]:
        # Fetch roles with search input string
        role_results = await search_roles(conn, search_query, paging)
        data["roles"] = role_results
        object_counts.append(await search_roles_count(conn, search_query))

    if "user" in search_query["search_object_types"]:
        # Fetch users with search input string
        user_results = await search_users(conn, search_query, paging)
        data["users"] = user_results
        object_counts.append(await search_users_count(conn, search_query))

    conn.close()

    total_pages = get_total_pages(object_counts, int(search_query["page_size"]))

    return json(
        {"data": data, "page": search_query["page"], "total_pages": total_pages}
    )


def search_paginate(page_size, page_num):
    """Paginate the results for the frontend."""
    if page_size <= 0:
        page_size = 50
    start = (page_num - 1) * page_size
    end = page_num * page_size
    return (start, end)


def get_total_pages(size_list, page_size):
    """Get the maximum total pages to request."""
    if size_list:
        return int(math.ceil(max(size_list) / page_size))
    return 0
