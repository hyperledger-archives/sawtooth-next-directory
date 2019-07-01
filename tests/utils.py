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
from rbac.common.logs import get_default_logger
from rbac.providers.common.db_queries import connect_to_db

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


def add_role_owner(session, role_id, payload):
    """Create a proposal for adding a role owner
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
    return session.post(
        "http://rbac-server:8000/api/roles/{}/owners".format(role_id), json=payload
    )


def approve_proposal(session, proposal_id):
    """Create a role and authenticate to use api endpoints during testing."""
    proposal_payload = {"status": "APPROVED", "reason": "Approved by integration test"}
    response = session.patch(
        "http://rbac-server:8000/api/proposals/{}".format(proposal_id),
        json=proposal_payload,
    )
    sleep(3)
    return response


def create_test_task(session, task_payload):
    """Create a task and authenticate to use api endpoints during testing."""
    response = session.post("http://rbac-server:8000/api/tasks", json=task_payload)
    sleep(3)
    return response


def create_test_pack(session, pack_payload):
    """Create a pack and authenticate to use api endpoints during testing."""
    response = session.post("http://rbac-server:8000/api/packs", json=pack_payload)
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
    except (KeyError, IndexError):
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


def get_outbound_queue_depth():
    """Returns the number of items in the outbound queue."""
    with connect_to_db() as db_connection:
        result = r.table("outbound_queue").count().run(db_connection)
        return result


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


def wait_for_prpsl_rjctn_in_db(object_id, max_attempts=10, delay=0.5):
    """Polls rethinkdb for the requested proposal until it has been rejected.
    Useful when commiting a delete transaction in sawtooth and waiting for the
    related proposals to be rejected for dependent chained transactions.

    Args:
        object_id
            str:    Object_id of the proposal to wait for.
        max_attempts:
            int:    The number of times to attempt to find the given role before
                    giving up and returning False.
                    Default value: 10
        delay:
            float:  The number of seconds to wait between query attempts.
                    Default value: 0.5
    Returns:
        resource_removed:
            bool:
                True:   If the role is successfully found within the given
                        number of attempts.
            bool:
                False:  If the role is not found after the given number of
                        attempts.
    """
    is_proposal_closed = False
    count = 0
    with connect_to_db() as conn:
        while not is_proposal_closed and count < max_attempts:
            resource = (
                r.table("proposals")
                .filter({"object_id": object_id, "status": "REJECTED"})
                .coerce_to("array")
                .run(conn)
            )
            if resource:
                is_proposal_closed = True
            count += 1
            sleep(delay)
    return is_proposal_closed


def wait_for_resource_removal_in_db(
    table, index, identifier, max_attempts=10, delay=0.5
):
    """Polls rethinkdb for the requested resource until it has been removed.
    Useful when commiting a delete transaction in sawtooth and waiting for the
    resource to be removed from rethink for dependent chained transactions.

    Args:
        table:
            str:    the name of a table to query for the resource in.
        index:
            str:    the name of the index of the identifier to query for.
        identifier:
            str:    A id for a given resource to wait for.
        max_attempts:
            int:    The number of times to attempt to find the given role before
                    giving up and returning False.
                        Default value: 10
        delay:
            float:  The number of seconds to wait between query attempts.
                        Default value: 0.5
    Returns:
        resource_removed:
            bool:
                True:   If the role was successfully removed within the given
                        number of attempts.
            bool:
                False:  If the role is  found after the given number of
                        attempts.
    """
    resource_removed = False
    count = 0
    with connect_to_db() as conn:
        while not resource_removed and count < max_attempts:
            resource = (
                r.table(table).filter({index: identifier}).coerce_to("array").run(conn)
            )
            if not resource:
                resource_removed = True
            count += 1
            sleep(delay)
    return resource_removed


def wait_for_role_in_db(role_id, max_attempts=10, delay=0.5):
    """ Polls rethinkdb for the requested role. Useful when commiting a
    transaction in sawtooth and waiting for the resource to be upserted in
    rethink for depended chained transactions.

    Args:
        role_id:
            str:    A next_id for a given role to wait for.
        max_attempts:
            int:    The number of times to attempt to find the given role before
                    giving up and returning False.
                    Default value: 10
        delay:
            float:  The number of seconds to wait between query attempts.
                    Default value: 0.5
    Returns:
        bool:
            True:   If the role is successfully found within the given number of
                    attempts.
        bool:
            False:  If the role is not found after the given number of attempts.
    """
    role_found = False
    count = 0
    while not role_found and count < max_attempts:
        role_found = is_role_in_db(role_id)
        count += 1
        sleep(delay)
    return role_found


def is_role_in_db(role_id):
    """Returns whether the role is in the roles table in rethink.
    Args:
        email:
            str: an email address.
    Returns:
        True: The role was found in rethink
        False: the role was not found in rethink
    """
    with connect_to_db() as db_connection:
        result = (
            r.table("roles").filter({"role_id": role_id}).count().run(db_connection)
        )
        return result > 0


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


def get_pack_by_pack_id(pack_id):
    """Returns pack by pack_id

    Args:
        pack_id:
            str: pack_id of pack to query
    """
    with connect_to_db() as db_connection:
        pack = (
            r.table("packs")
            .filter({"pack_id": pack_id})
            .coerce_to("array")
            .run(db_connection)
        )
    return pack


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


def get_user_mapping_entry(next_id):
    """Returns user_mapping entry for given user next_id.

    Args:
        next_id:
            str: a user's unique id.
    Returns:
        user_mapping_entry:
            dict: user_mapping entry of given user
    """
    with connect_to_db() as db_connection:
        return (
            r.table("user_mapping")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(db_connection)
        )


def get_auth_entry(next_id):
    """Returns auth entry for given user next_id.

    Args:
        next_id:
            str: a user's unique id.
    Returns:
        auth_entry:
            dict: auth entry of given user
    """
    with connect_to_db() as db_connection:
        return (
            r.table("auth")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(db_connection)
        )


def get_user_metadata_entry(next_id):
    """Returns metadta entry for given user next_id.

    Args:
        next_id:
            str: a user's unique id.
    Returns:
        metadata_entry:
            dict: metadata entry of given user
    """
    with connect_to_db() as db_connection:
        return (
            r.table("metadata")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(db_connection)
        )


def check_user_is_pack_owner(pack_id, next_id):
    """Returns a pack_owners entry for given user next_id.

    Args:
        pack_id:
            str: a pack's unique id.
        next_id:
            str: a user's unique id.
    Returns:
        pack_owners_entry:
            dict: pack_owners entry for given user and pack id
    """
    with connect_to_db() as db_connection:
        return (
            r.table("pack_owners")
            .filter({"identifiers": [next_id], "pack_id": pack_id})
            .coerce_to("array")
            .run(db_connection)
        )


def get_deleted_user_entries(next_id):
    """Returns a list of entries from tables relating to a
    user's deletion. Tables include: users, metadata, auth and
    user_mapping. After a successful deletion, this function
    should return an empty list.

    Args:
        next_id:
            str: a user's unique id.
    Returns:
        related_entries:
            dict: Contains entries from tables: users,
                metadta, user_mapping, and auth for a
                given user
    """
    with connect_to_db() as db_connection:
        return (
            r.table("users")
            .union(r.table("metadata"))
            .union(r.table("user_mapping"))
            .union(r.table("auth"))
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(db_connection)
        )


def get_pack_owners_by_user(next_id):
    """Returns all pack_owners entries for given user next_id.

    Args:
        next_id:
            str: a user's unique id.
    Returns:
        pack_owner_entries:
            dict: pack_owner entries of given user
    """
    with connect_to_db() as db_connection:
        return (
            r.table("pack_owners")
            .filter({"identifiers": [next_id]})
            .coerce_to("array")
            .run(db_connection)
        )


def update_manager(session, next_id, payload):
    """Update manager and authenticate to use api endpoints during testing."""
    response = session.put(
        "http://rbac-server:8000/api/users/{}/manager".format(next_id), json=payload
    )
    sleep(3)
    return response


def get_outbound_queue_entry(data, max_attempts=10, delay=0.5):
    """ Gets an entry from outbound_queue table that matches the passed in
    data dictionary.

    Args:
        data: (dict) Entry from users/roles table without created_date field.
        max_attempts:
            int: The number of times to attempt to find the given outbound_queue
                 entry.
                    Default value: 10
        delay
            float: The number of seconds to wait between query attempts.
                Default value: 0.5
    Returns:
        outbound_queue_entry: (dict) The entry that has the data field
            matching the data parameter. This entry would contain the
            following fields: data, data_type, provider_id, sync_type,
            timestamp.
    """
    query_count = 0
    outbound_queue_entry = []
    with connect_to_db() as conn:
        while not outbound_queue_entry and query_count < max_attempts:
            outbound_queue_entry = (
                r.table("outbound_queue")
                .filter({"data": data})
                .coerce_to("array")
                .run(conn)
            )
            if not outbound_queue_entry:
                query_count += 1
                sleep(delay)
    return outbound_queue_entry
