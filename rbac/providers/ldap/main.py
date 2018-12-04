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

import os
import asyncio
import logging
import sys

from rbac.providers.ldap import ldap_inbound_service, ldap_outbound_service

TOP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, TOP_DIR)

ENV_VAR_MESSAGE_TARGET = "LDAP_DC"
MESSAGE_TARGET_KEY_LDAP = "provider_id"
MESSAGE_TARGET_VALUE_LDAP = os.getenv(ENV_VAR_MESSAGE_TARGET)

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def start_ldap_sync():

    loop = asyncio.get_event_loop()

    LOGGER.info("Waiting for tables to be available")
    loop.run_until_complete(ldap_inbound_service.wait_until_tables_are_available())
    LOGGER.info("Tables are available")

    # Run the initial sync coroutines in parallel
    LOGGER.info("Importing existing records from inbound and outbound queues")
    loop.run_until_complete(
        asyncio.gather(
            *[
                ldap_outbound_service.export_preexisting_outbound_queue_records(),
                ldap_inbound_service.import_preexisting_ldap_inbound_records(),
            ]
        )
    )

    # Run the threads in parallel after the coroutines complete
    LOGGER.info("Starting long-running outbound sync tasks...")
    asyncio.ensure_future(ldap_outbound_service.sync_outbound_queue_to_active_dir())
    asyncio.ensure_future(ldap_inbound_service.sync_inbound_queue_to_active_dir())
    loop.run_forever()
