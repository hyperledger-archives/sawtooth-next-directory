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
"""Start the Azure provider with initial sync and two listeners for inbound and outbound deltas."""
import os
from environs import Env

from rbac.common.logs import get_default_logger
from rbac.providers.azure.delta_outbound_sync import outbound_sync_listener
from rbac.providers.azure.delta_inbound_sync import inbound_sync_listener
from rbac.providers.azure.initial_inbound_sync import initialize_aad_sync
from rbac.providers.common.threading import DeltaSyncThread

LOGGER = get_default_logger(__name__)


def main():
    """Start the initial sync and two delta threads."""
    env = Env()
    azure_sync = env.int("ENABLE_AZURE_SYNC", 0)
    if not azure_sync:
        LOGGER.warning("Azure sync not enabled. Exiting...")
        return
    tenant_id = os.getenv("TENANT_ID")
    if not tenant_id:
        LOGGER.warning("No Azure provider configured, exiting...")
        return

    initialize_aad_sync()
    # Create sync listener threads.
    inbound_sync_thread = DeltaSyncThread("Azure Inbound", inbound_sync_listener)
    outbound_sync_thread = DeltaSyncThread("Azure Outbound", outbound_sync_listener)
    # Start sync listener threads.
    inbound_sync_thread.start()
    outbound_sync_thread.start()
