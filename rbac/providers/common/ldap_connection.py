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

import sys
import logging

from ldap3 import Connection, Server, ALL
from ldap3.core.exceptions import LDAPSocketOpenError

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

LDAP_CONNECTION_TIMEOUT = 5


def create_ldap_connection(server, user, password):
    """Creates an open connection to an LDAP server"""

    server = Server(server, get_info=ALL)
    connection = Connection(
        server=server,
        user=user,
        password=password,
        receive_timeout=LDAP_CONNECTION_TIMEOUT,
    )

    try:
        if not connection.bind():
            LOGGER.error(
                "Error binding to LDAP server %s : %s", server, connection.result
            )
    except LDAPSocketOpenError as lsoe:
        LOGGER.error("Error opening LDAP socket to server %s. %s", server, lsoe)
        return None

    return connection
