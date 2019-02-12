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
from sanic import Blueprint
from sanic.response import json

from rbac.common.logs import get_logger
from rbac.server.api.auth import authorized
from rbac.server.db import db_utils
from rbac.server.db.packs_query import search_packs
from rbac.server.db.roles_query import search_roles
from rbac.server.db.users_query import search_users

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

    # Create resopnse data object
    data = {"packs": [], "roles": [], "users": []}

    # Run search queries
    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )
    if "pack" in search_query["search_object_types"]:
        # Fetch packs with search input string
        pack_results = await search_packs(conn, search_query)
        data["packs"] = pack_results

    if "role" in search_query["search_object_types"]:
        # Fetch roles with search input string
        role_results = await search_roles(conn, search_query)
        data["roles"] = role_results

    if "user" in search_query["search_object_types"]:
        # Fetch users with search input string
        user_results = await search_users(conn, search_query)
        data["users"] = user_results

    conn.close()

    return json({"data": data})
