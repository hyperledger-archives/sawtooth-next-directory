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
"""LDAP Inbound Delta Sync Test"""
# pylint: disable=redefined-outer-name
# NOTE: disabling for pytest as per:
# https://stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint

import time
from datetime import datetime, timedelta, timezone
import requests

from ldap3 import (
    Server,
    Connection,
    MOCK_SYNC,
    OFFLINE_AD_2012_R2,
    ALL_ATTRIBUTES,
    MODIFY_REPLACE,
)
from ldap3.extend.microsoft import addMembersToGroups, removeMembersFromGroups
import pytest
import rethinkdb as r
from environs import Env

from rbac.common.crypto.secrets import generate_api_key
from rbac.common.logs import get_default_logger
from rbac.providers.common.db_queries import connect_to_db
from rbac.providers.ldap.delta_inbound_sync import (
    insert_updated_entries,
    insert_deleted_entries,
    remove_outbound_duplicates,
)
from tests.utilities.creation_utils import create_next_admin, create_test_role
from tests.utilities.db_queries import get_role_by_name
from tests.utils import (
    check_user_is_pack_owner,
    create_test_pack,
    delete_role_by_name,
    delete_pack_by_name,
    get_auth_entry,
    get_deleted_user_entries,
    get_role_id_from_cn,
    get_role_admins,
    get_role_members,
    get_role_owners,
    get_user_in_db_by_email,
    get_user_mapping_entry,
    get_user_metadata_entry,
    get_user_next_id,
    get_pack_owners_by_user,
    is_user_in_db,
    is_group_in_db,
    wait_for_resource_removal_in_db,
)

LOGGER = get_default_logger(__name__)

SERVER = Server("my_fake_server", get_info=OFFLINE_AD_2012_R2)

# ------------------------------------------------------------------------------
# <==== BEGIN TEST PARAMETERS =================================================>
# ------------------------------------------------------------------------------

TEST_USERS = [
    {"common_name": "User0", "name": "Zeroth User", "given_name": "Zeroth"},
    {"common_name": "User1", "name": "First User", "given_name": "First"},
    {"common_name": "User2", "name": "Second User", "given_name": "Second"},
    {"common_name": "User3", "name": "Third User", "given_name": "Third"},
    {"common_name": "User4", "name": "Fourth User", "given_name": "Fourth"},
]

TEST_GROUPS = [{"common_name": "test_group", "name": "test_group"}]

# entry_data, outbound_status, expected_result.
TEST_CHECK_OUTBOUND_QUEUE = [
    (
        {"data": {"members": ["test_user_1"], "remote_id": "role_1"}},
        "UNCONFIRMED",
        True,
    ),
    (
        {"data": {"members": ["test_user_1, test_user_2"], "remote_id": "role_2"}},
        "CONFIRMED",
        True,
    ),
    ({"data": {"members": ["test_user_3"], "remote_id": "role_3"}}, None, False),
]

# ------------------------------------------------------------------------------
# <==== END TEST PARAMETERS ===================================================>
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# <==== BEGIN TEST FIXTURES ===================================================>
# ------------------------------------------------------------------------------


@pytest.fixture(autouse=True, scope="module")
def ldap_connection():
    """Binds and yields a mock ldap connection for integration testing.
    """
    connection = Connection(
        SERVER,
        user="cn=my_user,ou=test,o=lab",
        password="my_password",
        client_strategy=MOCK_SYNC,
    )
    connection.bind()
    yield connection
    connection.unbind()


# ------------------------------------------------------------------------------
# <==== END TEST FIXTURES =====================================================>
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# <==== BEGIN TEST HELPER FUNCTIONS ===========================================>
# ------------------------------------------------------------------------------


def _get_user_attributes(common_name, name, given_name):
    """Generates valid AD user attributes for creating a fake user in a mock AD.

    Args:
        common_name:
            str: A common name for a fake user.

        name:
            str: A username for a fake user.

        given_name:
            str: A given name for a fake user.

    Returns:
        attributes:
            obj: a dict of fake user attributes.
    """
    attributes = {
        "cn": common_name,
        "displayName": name,
        "distinguishedName": "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB"
        % common_name,
        "givenName": given_name,
        "name": name,
        "objectCategory": "CN=Person,CN=Schema,CN=Configuration,DC=AD2012,DC=LAB",
        "objectClass": ["top", "person", "organizationalPerson", "user"],
        "sn": "%s_sn" % common_name,
        "userPassword": "P@ssw0rd123",
        "mail": "%s@clouddev.corporate.t-mobile.com" % common_name,
        "whenChanged": datetime.utcnow().replace(tzinfo=timezone.utc),
        "whenCreated": datetime.utcnow().replace(tzinfo=timezone.utc),
    }
    return attributes


def _get_group_attributes(common_name, name, owner=""):
    """Generates valid AD group attributes for creating a fake group in a mock AD.

    Args:
        common_name:
            str: A common name for a fake group.

        name:
            str: A username for a fake group.

    Returns:
        attributes:
            obj: a dict of fake group attributes.
    """
    group = {
        "cn": common_name,
        "distinguishedName": "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB"
        % common_name,
        "name": name,
        "objectCategory": "CN=Group,CN=Schema,CN=Configuration,DC=AD2012,DC=LAB",
        "objectClass": ["top", "group"],
        "whenChanged": datetime.utcnow().replace(tzinfo=timezone.utc),
        "whenCreated": datetime.utcnow().replace(tzinfo=timezone.utc),
    }
    if owner:
        group["managedBy"] = owner
    return group


def create_fake_user(ldap_connection, common_name, name, given_name):
    """Puts a given user object in the mock AD server.

    Args:
        ldap_connection:
            obj: A bound ldap connection object.

        common_name:
            str: A string containing the common name of a fake AD user.

        name:
            str: A string containing the username of a fake AD user.

        given_name:
            str: A string containing the given name of a fake AD user.
    """
    attributes = _get_user_attributes(common_name, name, given_name)
    ldap_connection.strategy.add_entry(
        "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB" % common_name,
        attributes=attributes,
    )


def create_fake_group(ldap_connection, common_name, name, owner=""):
    """Puts a given user object in the mock AD server.

    Args:
        ldap_connection:
            obj: A bound ldap connection object.
        common_name:
            str: A string containing the common name of a fake AD role.
        name:
            str: A string containing the name of a fake group.
        owner:
    """
    attributes = _get_group_attributes(common_name, name, owner)
    ldap_connection.strategy.add_entry(
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % common_name,
        attributes=attributes,
    )


def create_next_role_ldap(user, role_name):
    """" Create a NEXT role as an imported LDAP user

    Args:
        user:
            dict: User table entry for imported LDAP user
        role_name:
            str: Name of role

    Returns:
        role_id:
            str: UUID of newly created NEXT role

    Raises:
        ValueError: When user was not auth successfully.
    """
    token = ldap_auth_login(user)

    if token:
        user_next_id = user["next_id"]

        role_data = {
            "name": role_name,
            "owners": [user_next_id],
            "administrators": [user_next_id],
        }
        with requests.Session() as session:
            session.headers.update({"Authorization": token})
            response = create_test_role(session, role_data)
            return response.json()["data"]["id"]
    raise ValueError("Unsuccessful authentication.")


def create_pack_ldap(user, pack_name):
    """" Create a NEXT pack as an imported LDAP user

    Args:
        user:
            dict: User table entry for imported LDAP user
        pack_name:
            str: Name of pack

    Returns:
        pack_id:
            str: UUID of newly created NEXT pack

    Raises:
        ValueError: When user was not auth successfully.
    """
    token = ldap_auth_login(user)

    if token:
        user_next_id = user["next_id"]

        pack_data = {
            "description": "LDAP test pack",
            "name": pack_name,
            "owners": [user_next_id],
            "roles": [],
        }
        with requests.Session() as session:
            session.headers.update({"Authorization": token})
            response = create_test_pack(session, pack_data)
            return response.json()["data"]["pack_id"]
    raise ValueError("Unsuccessful authentication.")


def ldap_auth_login(user):
    """" Authenticate as a test LDAP user and create a new entry in
    auth RethinkDB table.

    Args:
        user:
            dict: User table entry for imported LDAP user

    Returns:
        token:
            str: Bearer token upon user's successful authentication
    """
    env = Env()
    ldap_conn = Connection(
        SERVER,
        user=user["remote_id"],
        password="P@ssw0rd123",
        client_strategy=MOCK_SYNC,
    )

    # On successful bind, create auth table entry
    if ldap_conn.bind():
        conn = connect_to_db()
        user_map = (
            r.table("user_mapping")
            .filter({"next_id": user["next_id"]})
            .coerce_to("array")
            .run(conn)
        )
        auth_entry = {
            "next_id": user["next_id"],
            "username": user["username"],
            "email": user["email"],
            "encrypted_private_key": user_map[0]["encrypted_key"],
            "public_key": user_map[0]["public_key"],
        }
        r.table("auth").insert(auth_entry).run(conn)
        conn.close()
        return generate_api_key(env("SECRET_KEY"), user["next_id"])
    return None


def get_fake_user(ldap_connection, user_common_name):
    """Gets a fake user from the mock AD server.

    Args:
        ldap_connection:
            obj: a mock ldap connection object.

        user_common_name:
            str: the common name of the fake user.

    Returns:
        fake_user:
            arr<obj>: an array containing any users with a matching common name.
    """
    search_parameters = {
        "search_base": "OU=Users,OU=Accounts,DC=AD2012,DC=LAB",
        "search_filter": "(&(objectClass=person)(cn=%s))" % user_common_name,
        "attributes": ALL_ATTRIBUTES,
        "paged_size": len(TEST_USERS),
    }
    ldap_connection.search(**search_parameters)
    fake_user = ldap_connection.entries
    return fake_user


def get_fake_group(ldap_connection, group_common_name):
    """Gets a fake group from the mock AD server.

    Args:
        ldap_connection:
            obj: a mock ldap connection object.

        group_common_name:
            str: the common name of the fake group.

    Returns:
        fake_user:
            arr<obj>: an array containing any groups with a matching common name.
    """
    search_parameters = {
        "search_base": "OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
        "search_filter": "(&(objectClass=group)(cn=%s))" % group_common_name,
        "attributes": ALL_ATTRIBUTES,
        "paged_size": len(TEST_GROUPS),
    }
    ldap_connection.search(**search_parameters)
    return ldap_connection.entries


def put_in_inbound_queue(fake_data, data_type):
    """Puts a fake ( user | group ) object in the inbound queue to be ingested by
    rbac_ledger_sync.

    Args:
        fake_data:
            obj: a fake ( user | group ) object to insert.
        data_type:
            str: type of object "user"/"group"
    """
    when_changed = (datetime.utcnow() - timedelta(days=1)).replace(tzinfo=timezone.utc)
    insert_updated_entries(fake_data, when_changed, data_type)


def is_user_a_role_member(role_common_name, user_common_name):
    """Checks to see if a given user is a member of the given role/group in
    rethinkDB.

    Args:
        user_common_name:
            str: string containing the common name of an AD user object.

        role_common_name:
            str: string containing the common name of an AD role/group object.

    Returns:
        bool:
            True: if the user is a member of the given group.

            False: if the user is not a member of the given group.
    """
    role_id = get_role_id_from_cn(role_common_name)
    user_distinct_name = (
        "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB" % user_common_name
    )
    next_id = get_user_next_id(remote_id=user_distinct_name)
    user_is_role_member = False
    for member in get_role_members(role_id):
        if member["related_id"] == next_id:
            user_is_role_member = True
    return user_is_role_member


def update_when_changed(ldap_connection, object_distinct_name):
    """Replace the whenChanged AD attribute to a newer datetime. This is required
    for delta inbound sync as old timestamps are ignored.

    Args:
        ldap_connection:
            obj: a mock ldap connection object.

        object_distinct_name:
            str: a string containing a valid AD object's distinct name.
    """
    ldap_connection.modify(
        object_distinct_name,
        {
            "whenChanged": [
                MODIFY_REPLACE,
                datetime.utcnow().replace(tzinfo=timezone.utc),
            ]
        },
    )


def set_role_owner(ldap_connection, user_common_name, role_common_name):
    """adds or replaces the role owner of the given group with the given user.

    Args:
        ldap_connection:
            obj: a mock ldap connection object.
        user_common_name:
            str: string containing the common name of an AD user object.

        role_common_name:
            str: string containing the common name of an AD role/group object.
    """
    user_distinct_name = [
        "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB" % user_common_name
    ]
    role_distinct_name = (
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % role_common_name
    )
    ldap_connection.modify(
        role_distinct_name, {"managedBy": [MODIFY_REPLACE, user_distinct_name]}
    )


def clear_role_owners(ldap_connection, role_common_name):
    """removes any owners in the given role.

    Args:
        ldap_connection:
            obj: a mock ldap connection object.
        role_common_name:
            str: string containing the common name of an AD user object.
    """
    role_distinct_name = (
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % role_common_name
    )
    ldap_connection.modify(role_distinct_name, {"managedBy": [MODIFY_REPLACE, []]})


def is_user_the_role_owner(role_common_name, user_common_name):
    """Checks to see if a given user is an owner of the given role/group in
    rethinkDB.

    Args:
        user_common_name:
            str: string containing the common name of an AD user object.

        role_common_name:
            str: string containing the common name of an AD role/group object.

    Returns:
        bool:
            True: if the user is an owner of the given group.

            False: if the user is not an owner of the given group.
    """
    role_id = get_role_id_from_cn(role_common_name)
    user_distinct_name = (
        "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB" % user_common_name
    )
    next_id = get_user_next_id(remote_id=user_distinct_name)
    role_owners = get_role_owners(role_id)
    user_is_role_owner = False
    if len(role_owners) is 1:
        if role_owners[0]["related_id"] == next_id:
            user_is_role_owner = True
    return user_is_role_owner


# ------------------------------------------------------------------------------
# <==== END TEST HELPER FUNCTIONS =============================================>
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# <==== BEGIN SETUP FUNCTIONS =================================================>
# ------------------------------------------------------------------------------


def setup_module():
    """actions to be performed to configure the database before tests are run.
    """
    with connect_to_db() as db_connection:
        successful_insert = False
        result = 0
        while not successful_insert:
            try:
                result = (
                    r.table("roles").index_create("start_block_num").run(db_connection)
                )
                successful_insert = True
            except r.errors.ReqlOpFailedError:
                time.sleep(1)
        # extra time to allow for db initialization
        time.sleep(10)
        return result


# ------------------------------------------------------------------------------
# <==== BEGIN SETUP FUNCTIONS =================================================>
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# <==== BEGIN TEARDOWN FUNCTIONS ==============================================>
# ------------------------------------------------------------------------------


def teardown_module():
    """actions to be performed to clear configurations after tests are run.
    """
    with connect_to_db() as db_connection:
        # remove the index we created
        r.table("roles").index_drop("start_block_num").run(db_connection)
        for user in TEST_USERS:
            # remove any users, role members, and role owners that we created
            r.table("users").filter({"cn": user["common_name"]}).delete().run(
                db_connection
            )
            user_distinct_name = (
                "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB" % user["common_name"]
            )
            r.table("role_members").filter(
                {"related_id": user_distinct_name}
            ).delete().run(db_connection)
            r.table("role_owners").filter(
                {"related_id": user_distinct_name}
            ).delete().run(db_connection)
        for group in TEST_GROUPS:
            # remove any roles we created
            r.table("roles").filter({"cn": group["common_name"]}).delete().run(
                db_connection
            )


# ------------------------------------------------------------------------------
# <==== BEGIN TEARDOWN FUNCTIONS ==============================================>
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# <==== BEGIN TEST FUNCTIONS ==================================================>
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("user", TEST_USERS)
def test_create_fake_user(ldap_connection, user):
    """Creates a fake user and inserts it to the inbound queue for ingestion
    by rbac_ledger_sync. Waits 15 seconds. Checks if the fake user exists in
    the users table in rethinkDB.

    Args:
        ldap_connection:
            obj: A bound mock ldap connection object

        user:
            obj: dict:
                common_name:
                    str: A string containing the common name of an AD user.

                name:
                    str: A string containing the username of an AD user.

                given_name:
                    str: a string containing the given name of an AD user.
    """
    create_fake_user(ldap_connection, **user)
    fake_user = get_fake_user(ldap_connection, user["common_name"])
    put_in_inbound_queue(fake_user, "user")
    # wait for the fake user to be ingested by rbac_ledger_sync
    time.sleep(2)
    email = "%s@clouddev.corporate.t-mobile.com" % user["common_name"]
    result = is_user_in_db(email)
    syncflag_fetched = is_user_inbound(user["common_name"])
    assert result is True
    assert syncflag_fetched is True


def is_user_inbound(username_provided):
    """ Function returns TRUE,
        If the sync_direction flag in metadata field
        is set to INBOUND for the inbound sync users.
    """
    with connect_to_db() as db_connection:
        count_result = (
            r.table("users")
            .filter(
                {
                    "username": username_provided,
                    "metadata": {"sync_direction": "INBOUND"},
                }
            )
            .count()
            .run(db_connection)
        )
        return count_result > 0


@pytest.mark.parametrize("group", TEST_GROUPS)
def test_create_fake_group(ldap_connection, group):
    """Creates a fake group and inserts it to the inbound queue for ingestion
    by rbac_ledger_sync. Waits 15 seconds. Checks if the fake group exists in
    the groups table in rethinkDB.

    Args:
        ldap_connection:
            obj: A bound mock ldap connection

        group:
            obj: dict:
                common_name:
                    str: A common name of a group AD object.
                name:
                    str: A name of a group AD object.
    """
    create_fake_group(ldap_connection, **group)
    fake_group = get_fake_group(ldap_connection, group["common_name"])
    put_in_inbound_queue(fake_group, "group")
    # wait for the fake group to be ingested by rbac_ledger_sync
    time.sleep(3)
    result = is_group_in_db(group["common_name"])
    assert result is True


@pytest.mark.parametrize("user", TEST_USERS)
@pytest.mark.parametrize("group", TEST_GROUPS)
def test_add_group_member(ldap_connection, group, user):
    """Adds a user as a member of the given group.

    Args:
        ldap_connection:
            obj: A bound mock ldap connection

        group:
            obj: dict:
                common_name:
                    str: A common name of a group AD object.
                name:
                    str: A name of a group AD object.

        user:
            obj: dict:
                common_name:
                    str: A common name of an AD user object.

                name:
                    str: A username of an AD user object.

                given_name:
                    str: A given name of an AD user object.
    """
    user_distinct_name = [
        "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB" % user["common_name"]
    ]
    group_distinct_name = [
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % group["common_name"]
    ]
    addMembersToGroups.ad_add_members_to_groups(
        ldap_connection, user_distinct_name, group_distinct_name, fix=True
    )
    update_when_changed(ldap_connection, group_distinct_name)
    fake_group = get_fake_group(ldap_connection, group["common_name"])
    put_in_inbound_queue(fake_group, "group")
    # wait for the fake group to be ingested by rbac_ledger_sync
    time.sleep(3)
    result = is_user_a_role_member(group["common_name"], user["common_name"])
    assert result is True


@pytest.mark.parametrize("user", TEST_USERS)
@pytest.mark.parametrize("group", TEST_GROUPS)
def test_remove_group_member(ldap_connection, group, user):
    """removes a user as a member of the given group.

    Args:
        ldap_connection:
            obj: A bound mock mock_ldap_connection

        group:
            obj: dict:
                common_name:
                    str: A common name of a group AD object.
                name:
                    str: A name of a group AD object.

        user:
            obj: dict:
                common_name:
                    str: A common name of an AD user object.

                name:
                    str: A username of an AD user object.

                given_name:
                    str: A given name of an AD user object.
    """
    user_distinct_name = [
        "CN=%s,OU=Users,OU=Accounts,DC=AD2012,DC=LAB" % user["common_name"]
    ]
    group_distinct_name = [
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % group["common_name"]
    ]

    removeMembersFromGroups.ad_remove_members_from_groups(
        ldap_connection, user_distinct_name, group_distinct_name, fix=True
    )
    update_when_changed(ldap_connection, group_distinct_name)
    fake_group = get_fake_group(ldap_connection, group["common_name"])
    put_in_inbound_queue(fake_group, "group")
    # wait for the fake group to be ingested by rbac_ledger_sync
    time.sleep(3)
    result = is_user_a_role_member(group["common_name"], user["common_name"])
    assert result is False


@pytest.mark.parametrize("user", TEST_USERS)
@pytest.mark.parametrize("group", TEST_GROUPS)
def test_add_replace_group_owner(ldap_connection, group, user):
    """adds a user as an owner of the given group.

    Args:
        ldap_connection:
            obj: A bound mock ldap connection

        group:
            obj: dict:
                common_name:
                    str: A common name of a group AD object.
                name:
                    str: A name of a group AD object.

        user:
            obj: dict:
                common_name:
                    str: A common name of an AD user object.

                name:
                    str: A username of an AD user object.

                given_name:
                    str: A given name of an AD user object.
    """
    group_distinct_name = (
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % group["common_name"]
    )
    set_role_owner(ldap_connection, user["common_name"], group["common_name"])
    update_when_changed(ldap_connection, group_distinct_name)
    fake_group = get_fake_group(ldap_connection, group["common_name"])
    put_in_inbound_queue(fake_group, "group")
    # wait for the fake group to be ingested by rbac_ledger_sync
    time.sleep(3)

    result = is_user_the_role_owner(group["common_name"], user["common_name"])
    assert result is True


@pytest.mark.parametrize("group", TEST_GROUPS)
def test_remove_group_owner(ldap_connection, group):
    """removes any owners of the given group.

    Args:
        ldap_connection:
            obj: A bound mock mock_ldap_connection

        group:
            obj: dict:
                common_name:
                    str: A common name of a group AD object.
                name:
                    str: A name of a group AD object.
    """
    group_distinct_name = (
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % group["common_name"]
    )
    clear_role_owners(ldap_connection, group["common_name"])
    update_when_changed(ldap_connection, group_distinct_name)
    fake_group = get_fake_group(ldap_connection, group["common_name"])
    put_in_inbound_queue(fake_group, "group")
    # wait for the fake group to be ingested by rbac_ledger_sync
    time.sleep(3)
    role_id = get_role_id_from_cn(group["common_name"])
    role_owners = get_role_owners(role_id)
    assert len(role_owners) is 0


def test_delete_user(ldap_connection):
    """Deletes a AD user in NEXT

    Args:
        ldap_connection:
            obj: A bound mock mock_ldap_connection
    """
    # Create fake user and attach as owner to a role
    with requests.Session() as session:
        create_next_admin(session)
        create_fake_user(ldap_connection, "jchan20", "Jackie Chan", "Jackie")
        user_remote_id = "CN=jchan20,OU=Users,OU=Accounts,DC=AD2012,DC=LAB"
        create_fake_group(ldap_connection, "jchan_role", "jchan_role", user_remote_id)
        group_distinct_name = (
            "CN=jchan_role,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB"
        )
        addMembersToGroups.ad_add_members_to_groups(
            ldap_connection, user_remote_id, group_distinct_name, fix=True
        )
        fake_user = get_fake_user(ldap_connection, "jchan20")
        put_in_inbound_queue(fake_user, "user")
        fake_group = get_fake_group(ldap_connection, "jchan_role")
        put_in_inbound_queue(fake_group, "group")
        time.sleep(3)

        # See if owner and role are in the system
        email = "jchan20@clouddev.corporate.t-mobile.com"
        assert is_user_in_db(email) is True
        assert is_group_in_db("jchan_role") is True

        # See if all LDAP user has entries in the following
        # off chain tables: user_mapping and metadata
        user = get_user_in_db_by_email(email)
        next_id = user[0]["next_id"]
        assert get_user_mapping_entry(next_id)
        assert get_user_metadata_entry(next_id)

        # See that the owner is assigned to correct role
        role = get_role_by_name("jchan_role")
        owners = get_role_owners(role[0]["role_id"])
        members = get_role_members(role[0]["role_id"])
        assert owners[0]["related_id"] == next_id
        assert members[0]["related_id"] == next_id

        # Create a NEXT role with LDAP user as an admin and
        # check for LDAP user's entry in auth table
        next_role_id = create_next_role_ldap(user=user[0], role_name="managers")
        admins = get_role_admins(next_role_id)
        assert admins[0]["related_id"] == next_id
        assert get_auth_entry(next_id)

        # Create a NEXT pack with LDAP user as an owner
        next_pack_id = create_pack_ldap(user=user[0], pack_name="technology department")
        assert check_user_is_pack_owner(next_pack_id, next_id)

        # Delete user and verify LDAP user and related off chain
        # table entries have been deleted, role still exists
        # and role relationships have been deleted
        insert_deleted_entries([user_remote_id], "user_deleted")
        time.sleep(3)

        assert get_deleted_user_entries(next_id) == []
        assert get_pack_owners_by_user(next_id) == []
        assert is_group_in_db("jchan_role") is True
        assert get_role_owners(role[0]["role_id"]) == []
        assert get_role_admins(next_role_id) == []
        assert get_role_members(role[0]["role_id"]) == []

        delete_role_by_name("managers")
        delete_pack_by_name("technology department")


def test_delete_role(ldap_connection):
    """Delete a AD role in NEXT and all related tables

    Args:
        ldap_connection:
            obj: A bound mock mock_ldap_connection
    """
    create_fake_user(ldap_connection, "jchan", "Jackie C", "Jackiec")
    user_remote_id = "CN=jchan,OU=Users,OU=Accounts,DC=AD2012,DC=LAB"
    fake_user = get_fake_user(ldap_connection, "jchan")
    put_in_inbound_queue(fake_user, "user")

    create_fake_group(ldap_connection, "sysadmins", "sysadmins", user_remote_id)
    fake_group = get_fake_group(ldap_connection, "sysadmins")
    put_in_inbound_queue(fake_group, "group")
    time.sleep(3)
    group_distinct_name = "CN=sysadmins,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB"
    addMembersToGroups.ad_add_members_to_groups(
        ldap_connection, user_remote_id, group_distinct_name, fix=True
    )

    assert is_user_the_role_owner("sysadmins", "jchan") is True
    assert is_group_in_db("sysadmins") is True

    role = get_role_by_name("sysadmins")
    role_id = role[0]["role_id"]
    insert_deleted_entries(
        ["CN=sysadmins,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB"],
        "group_deleted",
    )
    time.sleep(3)

    is_role_removed = wait_for_resource_removal_in_db("roles", "name", "sysadmins")
    assert is_role_removed is True
    is_owner_removed = wait_for_resource_removal_in_db(
        "role_owners", "role_id", role_id
    )
    assert is_owner_removed is True
    is_member_removed = wait_for_resource_removal_in_db(
        "role_members", "role_id", role_id
    )
    assert is_member_removed is True


def test_created_date_comparison(ldap_connection):
    """ Tests that imported users/roles have the same created_date
    value in RethinkDB as the created_date in their source.
    """
    create_fake_group(ldap_connection, "pokemons", "pokemons")
    fake_group = get_fake_group(ldap_connection, "pokemons")
    put_in_inbound_queue(fake_group, "group")
    time.sleep(2)
    ldap_role = get_role_by_name("pokemons")
    assert fake_group[0].whenCreated.value == ldap_role[0]["created_date"]


@pytest.mark.parametrize(
    "entry_data, outbound_status, expected_result", TEST_CHECK_OUTBOUND_QUEUE
)
def test_outbound_queue_check(entry_data, outbound_status, expected_result):
    """ Tests that any inbound queue entries are checked against the outbound
    queue before insertion. If a duplicate entry exists in the outbound queue
    the function should return `True`, indicating the entry has already been
    written to sawtooth and that both entries should be deleted. Otherwise,
    the function should return `False`, indicating that the entry should be
    inserted.

    Args:
        entry_data:
            obj:    A dict containing a valid NEXT role object. Only
                    the `whenChanged` key is directly called in this obj, so
                    the rest may be arbitrary for this test (update if needed).
        outbound_status:
            str:    A string containing a valid NEXT `status` (
                    `CONFIRMED` or `UNCONFIRMED`). May be an empty string.
        expected_result:
            bool:   The boolean value that is expected to be returned by
                    put_in_outbound_queue().
    """
    with connect_to_db() as conn:
        if expected_result:
            outbound_entry = {**entry_data}
            if outbound_status:
                outbound_entry["status"] = outbound_status
                result = (
                    r.table("outbound_queue")
                    .insert(outbound_entry)
                    .coerce_to("object")
                    .run(conn)
                )
                assert result["inserted"] > 0
        result = remove_outbound_duplicates(entry_data["data"], conn)
        assert result == expected_result
