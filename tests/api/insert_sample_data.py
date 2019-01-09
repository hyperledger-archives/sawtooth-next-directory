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
# -----------------------------------------------------------------------------

import time
import re
import json
import dredd_hooks as hooks
from requests import request


API_PATH = "api"

MIN_NAME_LENGTH = 5

INVALID_SPEC_IDS = {
    "proposal": "63467642-6067-4c82-a096-1a1972d776b3",
    "role": "1f68397b-5b38-4aec-9913-4541c7e1d4c4",
    "task": "7ea843aa-1650-4530-94b1-a445d2a8193a",
    "user": "02178c1bcdb25407394348f1ff5273adae287d8ea328184546837957e71c7de57a",
    "manager": "02a06f344c6074e4bd0ca8a2abe45ee6ec92bf9cdd7b7a67c804350bfff4d4a8c0",
}

USER = {"name": "Bob Bobson", "password": "12345"}

MANAGER = {"name": "Suzie Suzerson", "password": "67890"}

ROLE = {
    "name": "Test Administrator",
    "owners": [],  # USER will be appended
    "administrators": [],  # USER will be appended
}

TASK = {"name": "test-user-permissions", "owners": [], "administrators": []}


seeded_data = {}


def get_base_api_url(txn):
    protocol = txn.get("protocol", "http:")
    host = txn.get("host", "localhost")
    port = txn.get("port", "8000")
    return "{}//{}:{}/{}/".format(protocol, host, port, API_PATH)


def api_request(method, base_url, path, body=None, auth=None):
    url = base_url + path

    auth = auth or seeded_data.get("auth", None)
    headers = {"Authorization": auth} if auth else None

    response = request(method, url, json=body, headers=headers)
    response.raise_for_status()

    parsed = response.json()
    return parsed.get("data", parsed)


def api_submit(base_url, path, resource, auth=None):
    return api_request("POST", base_url, path, body=resource, auth=auth)


def patch_body(txn, update):
    old_body = json.loads(txn["request"]["body"])

    new_body = {}
    for key, value in old_body.items():
        new_body[key] = value
    for key, value in update.items():
        new_body[key] = value

    txn["request"]["body"] = json.dumps(new_body)


def sub_nested_strings(dct, pattern, replacement):
    for key in dct.keys():
        if isinstance(dct[key], dict):
            sub_nested_strings(dct[key], pattern, replacement)
        elif isinstance(dct[key], str):
            dct[key] = re.sub(pattern, replacement, dct[key])


@hooks.before_all
def initialize_sample_resources(txns):
    base_url = get_base_api_url(txns[0])

    def submit(p, r, a=None):
        return api_submit(base_url, p, r, a)

    # Create MANAGER
    manager_response = submit("users", MANAGER)
    seeded_data["manager_auth"] = manager_response["authorization"]
    seeded_data["manager"] = manager_response["user"]

    # Create USER
    USER["manager"] = seeded_data["manager"]["id"]
    user_response = submit("users", USER)
    seeded_data["auth"] = user_response["authorization"]
    seeded_data["user"] = user_response["user"]

    # Create ROLE
    ROLE["owners"].append(seeded_data["user"]["id"])
    ROLE["administrators"].append(seeded_data["user"]["id"])
    seeded_data["role"] = submit("roles", ROLE)

    # Create TASK
    TASK["owners"].append(seeded_data["user"]["id"])
    TASK["administrators"].append(seeded_data["user"]["id"])
    seeded_data["task"] = submit("tasks", TASK)

    # Create a proposal
    proposal_path = "roles/{}/owners".format(seeded_data["role"]["id"])
    proposal_body = {"id": seeded_data["manager"]["id"]}
    proposal_auth = seeded_data["manager_auth"]

    proposal_response = submit(proposal_path, proposal_body, proposal_auth)
    seeded_data["proposal"] = {"id": proposal_response["proposal_id"]}

    # Get head block id
    time.sleep(2)
    head_id = api_request("GET", base_url, "blocks/latest")["id"]

    # Replace example identifiers with ones from seeded data
    for txn in txns:
        txn["request"]["headers"]["Authorization"] = seeded_data["auth"]
        sub_nested_strings(txn, "[0-9a-f]{128}", head_id)

        for name, spec_id in INVALID_SPEC_IDS.items():
            sub_nested_strings(txn, spec_id, seeded_data[name]["id"])


@hooks.before("/api/users > POST > 200 > application/json")
@hooks.before("/api/roles > POST > 200 > application/json")
def lengthen_user_name(txn):
    current_name = json.loads(txn["request"]["body"])["name"]
    if len(current_name) < MIN_NAME_LENGTH:
        patch_body(txn, {"name": current_name * MIN_NAME_LENGTH})


@hooks.before("/api/authorization > POST > 200 > application/json")
def add_credentials(txn):
    patch_body(txn, {"id": seeded_data["user"]["id"], "password": USER["password"]})


@hooks.before("/api/roles > POST > 200 > application/json")
@hooks.before("/api/tasks > POST > 200 > application/json")
def add_owners_and_admins(txn):
    patch_body(
        txn,
        {
            "administrators": [seeded_data["user"]["id"]],
            "owners": [seeded_data["user"]["id"]],
        },
    )


@hooks.before("/api/roles/{id}/tasks > POST > 200 > application/json")
@hooks.before("/api/roles/{id}/tasks > DELETE > 200 > application/json")
def add_task_id(txn):
    patch_body(txn, {"id": seeded_data["task"]["id"]})


@hooks.before("/api/users > POST > 200 > application/json")
def add_manager(txn):
    patch_body(txn, {"manager": seeded_data["manager"]["id"]})


@hooks.before("/api/roles/{id}/admins > DELETE > 200 > application/json")
@hooks.before("/api/roles/{id}/members > DELETE > 200 > application/json")
@hooks.before("/api/roles/{id}/owners > DELETE > 200 > application/json")
@hooks.before("/api/roles/{id}/admins > POST > 200 > application/json")
@hooks.before("/api/roles/{id}/members > POST > 200 > application/json")
@hooks.before("/api/roles/{id}/owners > POST > 200 > application/json")
@hooks.before("/api/tasks/{id}/admins > POST > 200 > application/json")
@hooks.before("/api/tasks/{id}/owners > POST > 200 > application/json")
@hooks.before("/api/users/{id}/manager > PUT > 200 > application/json")
@hooks.before("/api/users/{id}/manager > DELETE > 200 > application/json")
def add_manager_id(txn):
    txn["request"]["headers"]["Authorization"] = seeded_data["manager_auth"]
    patch_body(txn, {"id": seeded_data["manager"]["id"]})


@hooks.before("/api/tasks/{id}/admins > DELETE > 200 > application/json")
@hooks.before("/api/tasks/{id}/owners > DELETE > 200 > application/json")
def add_user_id(txn):
    patch_body(txn, {"id": seeded_data["user"]["id"]})
