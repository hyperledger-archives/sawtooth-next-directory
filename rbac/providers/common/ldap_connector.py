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
""" LDAP Connector
"""
import time

from ldap3 import Connection, Server, ALL
from ldap3.core.exceptions import LDAPSocketOpenError

from rbac.providers.common.provider_errors import LdapBindException
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)

LDAP_READ_TIMEOUT_SECS = 10
LDAP_CONNECT_TIMEOUT_SECS = 6
LDAP_CONNECT_RETRY_SECS = 10


def create_connection(server, user, password):
    """Creates an open connection to an LDAP server"""

    server = Server(server, get_info=ALL, connect_timeout=LDAP_CONNECT_TIMEOUT_SECS)
    connection = Connection(
        server=server,
        user=user,
        password=password,
        receive_timeout=LDAP_READ_TIMEOUT_SECS,
    )

    try:
        if not connection.bind():
            raise LdapBindException(
                "Error binding to LDAP server {}. Result: {}".format(
                    server, connection.result
                )
            )
    except LDAPSocketOpenError as lsoe:
        LOGGER.warning("Error opening LDAP socket to server %s. %s", server, lsoe)
        return None

    return connection


def await_connection(server, user, password):
    """Retries connecting to an LDAP server indefinitely"""

    connection = create_connection(server, user, password)

    while connection is None:
        LOGGER.info(
            "Failed to connect to Active Directory. Retrying in %s seconds",
            LDAP_CONNECT_RETRY_SECS,
        )
        time.sleep(LDAP_CONNECT_RETRY_SECS)
        connection = create_connection(server, user, password)

    return connection


def can_connect_to_ldap(server, user, password):
    """Able to connect to LDAP"""
    return create_connection(server, user, password) is not None
