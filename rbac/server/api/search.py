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
"""APIs and functions utilized to search."""
import math

from sanic import Blueprint
from sanic.response import json
from sanic_openapi import doc

from rbac.common.logs import get_default_logger
from rbac.server.api.auth import authorized
from rbac.server.api.utils import log_request
from rbac.server.db.db_utils import create_connection
from rbac.server.db.packs_query import search_packs, search_packs_count
from rbac.server.db.roles_query import search_roles, search_roles_count
from rbac.server.db.users_query import search_users, search_users_count

LOGGER = get_default_logger(__name__)
SEARCH_BP = Blueprint("search")


@SEARCH_BP.post("api/search")
@doc.summary("API Endpoint to get all roles, packs, or users containing a string.")
@doc.description("API Endpoint to get all roles, packs, or users containing a string.")
@doc.consumes(
    doc.JsonBody(
        {
            "query": {
                "page_size": int,
                "page": int,
                "search_object_types": [str],
                "search_input": str,
            }
        },
        description="For search_object_types, you may include: role, pack, and/or user.",
    ),
    location="body",
    content_type="application/json",
)
@doc.produces(
    {"data": {"roles": {}, "packs": {}, "users": {}}, "page": int, "total_pages": int},
    description="Success response with search results",
    content_type="application/json",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def search_all(request):
    """API Endpoint to get all roles, packs, or users containing a string."""
    log_request(request)
    search_query = request.json.get("query")

    # Check for valid payload containing query and search object types
    errors = validate_search_payload(search_query)
    if errors:
        return json(errors)

    # Create response data object
    data = {"packs": [], "roles": [], "users": []}

    # Pagination and total pages
    try:
        paging = search_paginate(search_query["page_size"], search_query["page"])
    except KeyError:
        paging = (0, 50)

    object_counts = []

    # Run search queries
    conn = await create_connection()
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

    total_pages = get_total_pages(object_counts, search_query["page_size"])

    return json(
        {"data": data, "page": search_query["page"], "total_pages": total_pages}
    )


def validate_search_payload(search_query):
    """Validate the search payload for necessary fields and return errors on non-existence."""
    if search_query is None:
        return {"errors": "No query parameter received."}
    if "search_object_types" not in search_query:
        return {"errors": "No search_object_types for search received."}
    if "search_input" not in search_query:
        return {"errors": "No search_input string for search received."}
    return {}


def search_paginate(page_size=50, page_num=1):
    """Paginate the results for the frontend."""
    page_size = int(page_size)
    page_num = int(page_num)
    if page_size <= 0:
        page_size = 50
    if page_num <= 0:
        page_num = 1
    start = (page_num - 1) * page_size
    end = page_num * page_size
    return (start, end)


def get_total_pages(size_list, page_size=50):
    """Get the maximum total pages to request."""
    page_size = int(page_size)
    if size_list:
        return int(math.ceil(max(size_list) / page_size))
    return 0
