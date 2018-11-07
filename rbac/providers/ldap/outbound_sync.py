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
# ------------------------------------------------------------------------------

import json
import logging
import os
import sys

import rethinkdb as r
import ldap3
from ldap3 import (ALL, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, Connection,
                   Server)

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DEFAULT_CONFIG = {
    "DB_HOST": "rethink",
    "DB_PORT": 28015,
    "DB_NAME": "rbac",
    "OUTBOUND_DB_TABLE": "queue_outbound",
}


def getenv(name, default):
    value = os.getenv(name)
    if value is None or value is "":
        return default
    return value


DB_HOST = getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])
OUTBOUND_DB_TABLE = getenv("OUTBOUND_DB_TABLE", DEFAULT_CONFIG["OUTBOUND_DB_TABLE"])

LDAP_DC = os.environ.get("LDAP_DC")
LDAP_SERVER = os.environ.get("LDAP_SERVER")
LDAP_USER = os.environ.get("LDAP_USER")
LDAP_PASS = os.environ.get("LDAP_PASS")

USER_SEARCH_FILTER = "(&(objectClass=person)(distinguishedName={}))"
GROUP_SEARCH_FILTER = "(&(objectClass=group)(distinguishedName={}))"

USER_ATTR_LIST = {
    "given_name": "givenName",
    "name": "displayName",
    "manager": "manager",
}
USER_REQUIRED_ATTR = {"cn", "user_principal_name"}

GROUP_ATTR_LIST = {
    "description": "description",
    "members": "member",
    "owners": "managedBy",
}
GROUP_REQUIRED_ATTR = {"group_type"}


def process_ldap_outbound():
    """
        Get earliest entry in outbound queue table and check if entry is from provider LDAP_DC.
        If entry is from LDAP_DC, process entry.

        This function will be replaced with LDAP Outbound Queue listener.
    """
    r.connect(host=DB_HOST, port=DB_PORT, db=DB_NAME).repl()

    while (
        not r.table(OUTBOUND_DB_TABLE)
        .filter("provider_id: " + LDAP_DC)
        .is_empty()
        .run()
    ):
        LOGGER.debug("%s has an item", OUTBOUND_DB_TABLE)
        outbound_entry = (
            r.table(OUTBOUND_DB_TABLE)
            .order_by("timestamp")
            .filter("provider_id:" + LDAP_DC)
            .coerce_to("array")[0]
            .run()
        )
        process_entry(outbound_entry)


def process_entry(outbound_entry):
    """
        Process outbound_entry as a AD user or AD group. If entry is neither,
        throw ValueError.
    """
    sawtooth_entry = outbound_entry["data"]
    distinguished_name = sawtooth_entry["distinguished_name"][0]
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASS)
    conn.bind()
    if outbound_entry["data_type"] == "user":
        process_user_entry(distinguished_name, sawtooth_entry, conn)
        remove_db_entry(outbound_entry)

    elif outbound_entry["data_type"] == "group":
        process_group_entry(distinguished_name, sawtooth_entry, conn)
        remove_db_entry(outbound_entry)

    else:
        raise ValueError(
            "Outbound queue record does not contain proper data type: {}".format(
                outbound_entry["data_type"]
            )
        )


def process_user_entry(distinguished_name, sawtooth_entry, conn):
    """
        Search AD to see if user from sawtooth exists. If an AD user exists, update the
        AD user. If the AD user does not exist, create a new AD user.
    """
    search_filter = USER_SEARCH_FILTER.format(distinguished_name)
    conn.search(LDAP_DC, search_filter, attributes=ldap3.ALL_ATTRIBUTES)
    if conn.entries:
        entry_json = json.loads(conn.entries[0].entry_to_json())
        ad_user = entry_json["attributes"]
        update_ad_user(
            distinguished_name=distinguished_name,
            ad_user=ad_user,
            sawtooth_entry=sawtooth_entry,
            conn=conn,
        )
    else:
        create_ad_user(distinguished_name, sawtooth_entry, conn)


def update_ad_user(distinguished_name, ad_user, sawtooth_entry, conn):
    """Update existing AD user with any updated attributes from sawtooth_entry."""
    for sawtooth_attribute, ad_attribute in USER_ATTR_LIST.items():
        if sawtooth_entry[sawtooth_attribute]:
            if sawtooth_entry[sawtooth_attribute] != ad_user[ad_attribute]:
                conn.modify(
                    distinguished_name,
                    {
                        ad_attribute: [
                            (MODIFY_REPLACE, [sawtooth_entry[sawtooth_attribute][0]])
                        ]
                    },
                )


def create_ad_user(distinguished_name, sawtooth_entry, conn):
    """Create new AD user using attributes from sawtooth_entry."""
    LOGGER.info("Creating new AD user: %s", distinguished_name)
    if all(attribute in sawtooth_entry for attribute in USER_REQUIRED_ATTR):
        conn.add(
            dn=distinguished_name,
            object_class={"person", "organizationalPerson", "user"},
            attributes={
                "cn": sawtooth_entry["user_name"],
                "userPrincipalName": sawtooth_entry["user_principal_name"],
            },
        )
        for sawtooth_attribute, ad_attribute in USER_ATTR_LIST.items():
            if sawtooth_entry[sawtooth_attribute]:
                conn.modify(
                    distinguished_name,
                    {
                        ad_attribute: [
                            (MODIFY_REPLACE, [sawtooth_entry[sawtooth_attribute][0]])
                        ]
                    },
                )
    else:
        LOGGER.info(
            "Cannot create a new user because required attributes were missing."
        )


def process_group_entry(distinguished_name, sawtooth_entry, conn):
    """
        Search AD to see if group from sawtooth exists. If an AD group exists, update the
        AD group. If the AD group does not exist, create a new AD group.
    """
    search_filter = GROUP_SEARCH_FILTER.format(distinguished_name)
    conn.search(LDAP_DC, search_filter, attributes=ldap3.ALL_ATTRIBUTES)
    if conn.entries:
        entry_json = json.loads(conn.entries[0].entry_to_json())
        ad_group = entry_json["attributes"]
        update_ad_group(distinguished_name, sawtooth_entry, ad_group, conn)
    else:
        create_ad_group(
            distinguished_name=distinguished_name,
            sawtooth_entry=sawtooth_entry,
            conn=conn,
        )


def update_ad_group(distinguished_name, sawtooth_entry, ad_group, conn):
    """Update existing AD group with any updated attributes from sawtooth_entry."""
    for sawtooth_attribute, ad_attribute in GROUP_ATTR_LIST.items():
        if sawtooth_entry[sawtooth_attribute]:
            if sawtooth_attribute == "members":
                if sorted(sawtooth_entry.get(sawtooth_attribute)) != sorted(
                    ad_group.get(ad_attribute)
                ):
                    update_ad_group_members(
                        distinguished_name=distinguished_name,
                        ad_group=ad_group,
                        sawtooth_entry=sawtooth_entry,
                        conn=conn,
                    )
            else:
                if sawtooth_entry.get(sawtooth_attribute) != ad_group.get(ad_attribute):
                    conn.modify(
                        distinguished_name,
                        {
                            ad_attribute: [
                                (
                                    MODIFY_REPLACE,
                                    [sawtooth_entry[sawtooth_attribute][0]],
                                )
                            ]
                        },
                    )


def update_ad_group_members(distinguished_name, ad_group, sawtooth_entry, conn):
    """Add or remove members from a AD group."""
    LOGGER.debug("Adding or removing members from group %s", distinguished_name)
    if "member" in ad_group:
        for ad_group_member in ad_group["member"]:
            if ad_group_member not in sawtooth_entry.get("members"):
                LOGGER.info(
                    "Removing %s from group %s", ad_group_member, distinguished_name
                )
                conn.modify(
                    dn=distinguished_name,
                    changes={"member": [(MODIFY_DELETE, [ad_group_member])]},
                )
    elif "members" in sawtooth_entry and "member" in ad_group:
        for sawtooth_group_member in sawtooth_entry["members"]:
            if sawtooth_group_member not in ad_group["member"]:
                LOGGER.info(
                    "Adding %s into group %s", sawtooth_group_member, distinguished_name
                )
                conn.modify(
                    dn=distinguished_name,
                    changes={"member": [(MODIFY_ADD, [sawtooth_group_member])]},
                )
    else:
        new_ad_group_members_add(
            distinguished_name=distinguished_name,
            sawtooth_entry=sawtooth_entry,
            conn=conn,
        )


def new_ad_group_members_add(distinguished_name, sawtooth_entry, conn):
    """Add members to a AD group with no existing members."""
    for sawtooth_group_member in sawtooth_entry["members"]:
        LOGGER.info(
            "Adding %s into group %s", sawtooth_group_member, distinguished_name
        )
        conn.modify(
            dn=distinguished_name,
            changes={"member": [(MODIFY_ADD, [sawtooth_group_member])]},
        )


def create_ad_group(distinguished_name, sawtooth_entry, conn):
    """Create new AD group using attributes from sawtooth_entry."""
    LOGGER.info("Creating new AD group: %s", distinguished_name)
    if all(attribute in sawtooth_entry for attribute in GROUP_REQUIRED_ATTR):
        conn.add(
            dn=distinguished_name,
            object_class={"group", "top"},
            attributes={"groupType": sawtooth_entry["group_types"]},
        )

        for sawtooth_attribute, ad_attribute in GROUP_ATTR_LIST.items():
            if sawtooth_entry[sawtooth_attribute]:
                if sawtooth_attribute == "members":
                    new_ad_group_members_add(
                        distinguished_name=distinguished_name,
                        sawtooth_entry=sawtooth_entry,
                        conn=conn,
                    )
            else:
                conn.modify(
                    distinguished_name,
                    {
                        ad_attribute: [
                            (MODIFY_ADD, [sawtooth_entry[sawtooth_attribute][0]])
                        ]
                    },
                )
    else:
        LOGGER.info(
            "Cannot create a new AD group because required attributes were missing."
        )


def remove_db_entry(entry):
    """Remove entry from queue outbound table in RethinkDB."""
    entry_id = entry["id"]
    r.table(OUTBOUND_DB_TABLE).get(entry_id).delete().run()


if __name__ == "__main__":
    process_ldap_outbound()
