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
"""Utility functions to assist with tests in cleanup or running."""
from time import sleep
import rethinkdb as r
from rbac.providers.common.db_queries import connect_to_db
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


def add_role_member(session, role_id, payload):
    """Create a proposal for adding a role member

    Args:
        session:
            object: current session object

        role_id:
            str: id of role that is to be added to

        payload:
            dictionary: in the format of
                {
                    "id": "ID OF USER CURRENTLY BEING ADDED"
                }
    """
    response = session.post(
        "http://rbac-server:8000/api/roles/{}/members".format(role_id), json=payload
    )
    sleep(3)
    return response


def create_test_role(session, role_payload):
    """Create a role and authenticate to use api endpoints during testing."""
    response = session.post("http://rbac-server:8000/api/roles", json=role_payload)
    sleep(3)
    return response


def create_test_task(session, task_payload):
    """Create a task and authenticate to use api endpoints during testing."""
    response = session.post("http://rbac-server:8000/api/tasks", json=task_payload)
    sleep(3)
    return response


def create_test_user(session, user_payload):
    """Create a user and authenticate to use api endpoints during testing."""
    response = session.post("http://rbac-server:8000/api/users", json=user_payload)
    sleep(3)
    return response


def delete_user_by_username(username):
    """Delete a user from db by the username."""
    conn = connect_to_db()
    r.table("users").filter({"username": username}).delete().run(conn)
    r.table("auth").filter({"username": username}).delete().run(conn)
    conn.close()


def delete_role_by_name(name):
    """Delete a role from db by the name."""
    conn = connect_to_db()
    try:
        role_id = r.table("roles").filter({"name": name}).coerce_to("array").run(conn)
        r.table("roles").filter({"name": name}).delete().run(conn)
        r.table("role_owners").filter({"role_id": role_id[0]["role_id"]}).delete().run(
            conn
        )
        r.table("role_members").filter({"role_id": role_id[0]["role_id"]}).delete().run(
            conn
        )
        r.table("role_admins").filter({"role_id": role_id[0]["role_id"]}).delete().run(
            conn
        )
        r.table("role_tasks").filter({"role_id": role_id[0]["role_id"]}).delete().run(
            conn
        )
        conn.close()
    except KeyError:
        conn.close()


def delete_pack_by_name(name):
    """Delete a pack from db by the name."""
    conn = connect_to_db()
    pack_id = r.table("packs").filter({"name": name}).coerce_to("array").run(conn)
    r.table("packs").filter({"name": name}).delete().run(conn)
    r.table("pack_owners").filter({"pack_id": pack_id[0]["pack_id"]}).delete().run(conn)
    r.table("role_packs").filter({"identifiers": [pack_id[0]["pack_id"]]}).delete().run(
        conn
    )
    conn.close()


def delete_task_by_name(name):
    """Delete a task from db by the name."""
    conn = connect_to_db()
    task_id = r.table("tasks").filter({"name": name}).coerce_to("array").run(conn)
    r.table("tasks").filter({"name": name}).delete().run(conn)
    r.table("task_owners").filter({"task_id": task_id[0]["task_id"]}).delete().run(conn)
    r.table("role_tasks").filter({"identifiers": [task_id[0]["task_id"]]}).delete().run(
        conn
    )
    conn.close()


def insert_role(role_data):
    """Inserting a role to the database"""
    conn = connect_to_db()
    r.table("roles").insert(role_data).run(conn)
    conn.close()


def insert_user(user_data):
    """Inserting a user to the database"""
    conn = connect_to_db()
    r.table("users").insert(user_data).run(conn)
    conn.close()


def get_proposal_with_retry(session, proposal_id):
    """Gets proposal via proposal API, retries 4 times."""
    retry = 0
    max_retries = 4
    while True:
        response = session.get(
            "http://rbac-server:8000/api/proposals/{}".format(proposal_id)
        )
        if response.status_code == 200:
            break
        elif retry > max_retries:
            break
        else:
            retry += 1
            LOGGER.info("retrying get proposal... %s", retry)
            sleep(5)
    return response


def is_user_in_db(email):
    """Returns the number of users in rethinkdb with the given email.

    Args:
        email:
            str: an email address.
    """
    with connect_to_db() as db_connection:
        result = r.table("users").filter({"email": email}).count().run(db_connection)
        return result > 0


def get_user_in_db_by_email(email):
    """Returns the user in rethinkdb with the given email.

    Args:
        email:
            str: an email address.
    """
    with connect_to_db() as db_connection:
        result = (
            r.table("users")
            .filter({"email": email})
            .coerce_to("array")
            .run(db_connection)
        )
        return result


def get_user_next_id(remote_id):
    """Returns the next_id for a given user's remote id.

    Args:
        remote_id:
            str: A string containing the user's remote id.

    Returns:
        next_id:
            str: A string containing the user's unique next_id.
    """
    with connect_to_db() as db_connection:
        results = list(
            r.table("users")
            .filter({"remote_id": remote_id})
            .pluck("next_id")
            .run(db_connection)
        )[0]
        next_id = results["next_id"]
    return next_id


def get_role_owners(role_id):
    """Returns a list of owner next_ids from a role in rethinkDB.

    Args:
        role_id:
            str: a NEXT role_id from rethinkDB.
    """
    with connect_to_db() as db_connection:
        role_owners = (
            r.table("role_owners")
            .filter({"role_id": role_id})
            .pluck("related_id")
            .coerce_to("array")
            .run(db_connection)
        )
    return role_owners


def get_role(name):
    """Returns a role in rethinkDB via name.

    Args:
        name:
            str: a name of a role in rethinkDB.
    """
    with connect_to_db() as db_connection:
        role = (
            r.table("roles")
            .filter({"name": name})
            .coerce_to("array")
            .run(db_connection)
        )
    return role


def is_group_in_db(name):
    """Returns the number of groups from the roles table in rethinkdb with
    the given name.

    Args:
        name:
            str: The name of a fake group.
    """
    with connect_to_db() as db_connection:
        result = r.table("roles").filter({"name": name}).count().run(db_connection)
        return result > 0


def get_role_id_from_cn(role_name):
    """Returns the NEXT role_id for a given role name.

    Args:
        role_common_name:
            str: A string containing the name of a role.

    Returns:
        role_id:
            str: A string containing the NEXT role id of the corresponding role.
    """
    with connect_to_db() as db_connection:
        results = list(
            r.table("roles")
            .order_by(index=r.desc("start_block_num"))
            .filter({"name": role_name})
            .pluck("role_id")
            .run(db_connection)
        )[0]
        role_id = results["role_id"]
    return role_id


def get_role_admins(role_id):
    """Returns a list of admin next_ids from a role in rethinkDB.

    Args:
        role_id:
            str: a NEXT role_id from rethinkDB.
    """
    with connect_to_db() as db_connection:
        role_admins = (
            r.table("role_admins")
            .filter({"role_id": role_id})
            .pluck("related_id")
            .coerce_to("array")
            .run(db_connection)
        )
    return role_admins


def get_role_members(role_id):
    """Returns a list of member user_ids from a role in rethinkDB.

    Args:
        role_id:
            str: a NEXT role_id from rethinkDB.
    """
    with connect_to_db() as db_connection:
        role_members = (
            r.table("role_members")
            .filter({"role_id": role_id})
            .pluck("related_id")
            .coerce_to("array")
            .run(db_connection)
        )
    return role_members


def log_in(session, credentials_payload):
    """Log in as the user with the given credentials for the given session

    Args:
        session:
            object: current session object

        credentials_payload:
            dictionary: in the format of
                {
                    "id": "USERNAME OF USER",
                    "password": "PASSWORD OF ASSOCIATED USER"
                }
    """
    response = session.post(
        "http://rbac-server:8000/api/authorization/", json=credentials_payload
    )
    sleep(3)
    return response


def update_proposal(session, proposal_id, proposal_payload):
    """Updates a created proposal

    Args:
        session:
            object: current session object

        proposal_id:
            str: id of proposal to be updated.

        proposal_payload:
            dictionary: in the format of
                {
                    "status": ("APPROVED"/"REJECT"),
                    "reason": "REASON OF STATUS",
                }
    """
    response = session.patch(
        "http://rbac-server:8000/api/proposals/{}".format(proposal_id),
        json=proposal_payload,
    )
    sleep(3)
    return response
