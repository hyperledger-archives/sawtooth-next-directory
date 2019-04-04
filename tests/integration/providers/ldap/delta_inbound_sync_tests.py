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
import rethinkdb as r
import pytest
from ldap3 import (
    Server,
    Connection,
    MOCK_SYNC,
    OFFLINE_AD_2012_R2,
    ALL_ATTRIBUTES,
    MODIFY_REPLACE,
)
from ldap3.extend.microsoft import addMembersToGroups, removeMembersFromGroups

from rbac.providers.ldap.delta_inbound_sync import insert_to_db
from rbac.providers.common.db_queries import connect_to_db


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
    server = Server("my_fake_server", get_info=OFFLINE_AD_2012_R2)
    connection = Connection(
        server,
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


def _get_group_attributes(common_name, name):
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


def create_fake_group(ldap_connection, common_name, name):
    """Puts a given user object in the mock AD server.

    Args:
        ldap_connection:
            obj: A bound ldap connection object.
        common_name:
            str: A string containing the common name of a fake AD role.
        name:
            str: A string containing the name of a fake group.
    """
    attributes = _get_group_attributes(common_name, name)
    ldap_connection.strategy.add_entry(
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % common_name,
        attributes=attributes,
    )


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
    """Gets a fake user from the mock AD server.

    Args:
        ldap_connection:
            obj: a mock ldap connection object.

        group_common_name:
            str: the common name of the fake group.

    Returns:
        fake_user:
            arr<obj>: an array containing any users with a matching common name.
    """
    search_parameters = {
        "search_base": "OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
        "search_filter": "(&(objectClass=group)(cn=%s))" % group_common_name,
        "attributes": ALL_ATTRIBUTES,
        "paged_size": len(TEST_GROUPS),
    }
    ldap_connection.search(**search_parameters)
    fake_user = ldap_connection.entries
    return fake_user


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
    insert_to_db(fake_data, when_changed, data_type)


def is_user_in_db(email):
    """Returns the number of users in rethinkdb with the given email.

    Args:
        email:
            str: an email address.
    """
    with connect_to_db() as db_connection:
        result = r.table("users").filter({"email": email}).count().run(db_connection)
        return result > 0


def get_user_next_id(distinguished_name):
    """Returns the next_id for a given user's distinguished name.

    Args:
        distinguished_name:
            str: A string containing the user's AD distinguished name.

    Returns:
        next_id:
            str: A string containing the user's unique next_id.
    """
    with connect_to_db() as db_connection:
        results = list(
            r.table("users")
            .filter({"remote_id": distinguished_name})
            .pluck("next_id")
            .run(db_connection)
        )[0]
        next_id = results["next_id"]
    return next_id


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


def get_role_id_from_cn(role_common_name):
    """Returns the NEXT role_id for a given role/group's common name.

    Args:
        role_common_name:
            str: A string containing the common name of an AD group.

    Returns:
        role_id:
            str: A string containing the NEXT role id of the corresponding role.
    """
    with connect_to_db() as db_connection:
        results = list(
            r.table("roles")
            .order_by(index=r.desc("start_block_num"))
            .filter({"name": role_common_name})
            .pluck("role_id")
            .run(db_connection)
        )[0]
        role_id = results["role_id"]
    return role_id


def get_role_members(role_id):
    """Returns a list of member user_ids from a role in rethnkDB.

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
    next_id = get_user_next_id(user_distinct_name)
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


def get_role_owners(role_id):
    """Returns a list of owner user_ids from a role in rethnkDB.

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
    next_id = get_user_next_id(user_distinct_name)
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
    time.sleep(1)
    email = "%s@clouddev.corporate.t-mobile.com" % user["common_name"]
    result = is_user_in_db(email)
    assert result is True


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
    time.sleep(1)
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
                    str: A given name of an AD suer object.
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
    time.sleep(1)
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
                    str: A given name of an AD suer object.
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
    time.sleep(1)
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
                    str: A given name of an AD suer object.
    """
    group_distinct_name = (
        "CN=%s,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB" % group["common_name"]
    )
    set_role_owner(ldap_connection, user["common_name"], group["common_name"])
    update_when_changed(ldap_connection, group_distinct_name)
    fake_group = get_fake_group(ldap_connection, group["common_name"])
    put_in_inbound_queue(fake_group, "group")
    # wait for the fake group to be ingested by rbac_ledger_sync
    time.sleep(1)

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
    time.sleep(1)
    role_id = get_role_id_from_cn(group["common_name"])
    role_owners = get_role_owners(role_id)
    assert len(role_owners) is 0
