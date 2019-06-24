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
"""Database queries for testing"""
import time
import rethinkdb as r

from rbac.utils import connect_to_db


def get_role_by_id(role_id):
    """"Get role information from roles table by role id.

    Args:
        role_id:
            str: id of role to retrieve
    """
    conn = connect_to_db()
    role = (
        r.db("rbac")
        .table("roles")
        .filter({"next_id": role_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    return role


def get_role_by_name(name):
    """Get role information from roles table by role name.

    Args:
        name:
            str: name of role to retrieve
    """
    conn = connect_to_db()
    user = (
        r.table("roles")
        .filter(lambda doc: (doc["name"].match("(?i)^" + name + "$")))
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    return user


def get_role_members(role_id):
    """Get the role members of a role

    Args:
        role_id:
            str: id of role to see members
    """
    conn = connect_to_db()
    members = (
        r.table("role_members")
        .filter({"role_id": role_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    return members


def get_user_by_id(next_id):
    """"Get user information from users table by user id.

    Args:
        next_id:
            str: id of user to retrieve
    """
    conn = connect_to_db()
    user = (
        r.db("rbac")
        .table("roles")
        .filter({"next_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    return user


def get_user_by_username(username):
    """Get user information from users table by username.

    Args:
        username:
            str:  username of user to retrieve
    """
    conn = connect_to_db()
    user = (
        r.table("users")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    return user


def wait_for_resource_in_db(table, index, identifier, max_attempts=15, delay=0.3):
    """Polls rethinkdb for the requested resource until it exists.

    Args:
        table:
            str: name of a table to query for the resource in
        index:
            str: name of the index of the identifier to query for
        identifier:
            str: a match of the resource in the index selected
        max_attempts:
            int: number of attempts to find resource before giving up and returning False
                Default value: 15
        delay:
            float: number of seconds to wait between query attempts.
                Default value: 0.3
    Returns:
        resource_removed:
            bool: if the role is found within given number of attempts
    """
    resource_found = False
    count = 0
    with connect_to_db() as conn:
        while not resource_found and count < max_attempts:
            resource = (
                r.table(table).filter({index: identifier}).coerce_to("array").run(conn)
            )
            if resource:
                resource_found = True
            count += 1
            time.sleep(delay)
    return resource_found
