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

import logging
import time
import os

import rethinkdb as r
from tornado import gen

from rbac.providers.error.unrecoverable_errors import (
    LdapValidationException,
    MissingLdapDestinationException,
)
from rbac.providers.ldap.outbound_sync import export_to_active_directory
from rbac.providers.ldap.ldap_message_validator import validate

LOGGER = logging.getLogger(__name__)
warning_logger = logging.StreamHandler()
warning_logger.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
warning_logger.setFormatter(log_formatter)
LOGGER.addHandler(warning_logger)

DB_HOST = "rethink"
DB_PORT = 28015
DB_NAME = "rbac"
DB_TABLE = "queue_outbound"
RETRY_INTERVAL_SECONDS_TABLE_READY = 3

ENV_VAR_MESSAGE_TARGET = "LDAP_DC"
MESSAGE_TARGET_KEY_LDAP = "provider_id"
MESSAGE_TARGET_VALUE_LDAP = os.getenv(ENV_VAR_MESSAGE_TARGET)

r.set_loop_type("tornado")


@gen.coroutine
def export_feed_change_to_ldap():
    """Fetches changes from the outbound queue table, validates and publishes them to Ldap"""

    feed = None
    connected = False
    connection = None

    # Will both be null on a delete, both have values on update.
    # Only new_val will be present on insert
    rethink_change_value_old = "old_val"
    rethink_change_value_new = "new_val"

    if MESSAGE_TARGET_VALUE_LDAP == "":
        raise MissingLdapDestinationException(
            "No message target found on the environment for outbound Ldap (key = {0}). Shutting down listener".format(
                ENV_VAR_MESSAGE_TARGET
            )
        )
    else:
        while not connected:
            try:
                connection = yield r.connect(DB_HOST, DB_PORT, DB_NAME)
                feed = (
                    yield r.table(DB_TABLE)
                    .filter({MESSAGE_TARGET_KEY_LDAP: MESSAGE_TARGET_VALUE_LDAP})
                    .changes()
                    .run(connection)
                )
                connected = True
            except r.ReqlRuntimeError as re:
                LOGGER.info(
                    "Attempt to connect to %s threw exception: %s. Retrying in %s seconds",
                    DB_TABLE,
                    str(re),
                    RETRY_INTERVAL_SECONDS_TABLE_READY,
                )
                time.sleep(RETRY_INTERVAL_SECONDS_TABLE_READY)

        while (yield feed.fetch_next()):
            new_record = yield feed.next()

            old_content = new_record[rethink_change_value_old]
            new_content = new_record[rethink_change_value_new]

            LOGGER.info("Old_content: %s. New_content: %s", old_content, new_content)

            if old_content is None and new_content is None:
                LOGGER.info("Change in RethinkDb was a deletion. Ignoring...")
            else:

                content = old_content

                if new_content is not None:
                    LOGGER.info(
                        "Change in RethinkDb was an insert or update. Exporting the new record..."
                    )
                    content = new_content

                try:
                    LOGGER.info("Validating: %s", str(content))

                    validate(content)

                    export_to_active_directory(content, connection)
                except LdapValidationException as le:
                    # TODO: Determine what to do with inadequate ldap data in the queue. Log and drop?
                    LOGGER.error(
                        "Ldap payload: %s encountered a validation error: %s",
                        content,
                        le,
                    )
