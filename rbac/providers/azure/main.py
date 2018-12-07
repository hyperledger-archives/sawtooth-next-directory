#!/usr/bin/env python3
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
""" Azure Active Directory Provider
"""
import threading
import logging

from rbac.providers.azure.initial_inbound_sync import initialize_aad_sync
from rbac.providers.azure.delta_outbound_sync import outbound_sync_listener
from rbac.providers.azure.delta_inbound_sync import inbound_sync_listener

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class InboundSyncThread(threading.Thread):
    """Custom Thread subclass that runs an AAD inbound sync listener in its own
    thread."""

    def __init__(self):
        """Initialize the InboundSyncThread class"""
        threading.Thread.__init__(self)
        self.name = "AAD Inbound Delta Sync Thread"

    def run(self):
        """Start the InboundSyncThread"""
        LOGGER.info("Starting %s", self.name)
        inbound_sync_listener()
        LOGGER.info("Exiting %s", self.name)


class OutboundSyncThread(threading.Thread):
    """Custom Thread subclass that runs an AAD outbound sync listener in its own
    thread."""

    def __init__(self):
        """Initialize the OutboundSyncThread class"""
        threading.Thread.__init__(self)
        self.name = "AAD Outbound Delta Sync Thread"

    def run(self):
        """Start the OutboundSyncThread"""
        LOGGER.info("Starting %s", self.name)
        outbound_sync_listener()
        LOGGER.info("Exiting %s", self.name)


def main():
    """ Starts the provider threads
    """
    initialize_aad_sync()
    # Create sync listener threads.
    inbound_sync_thread = InboundSyncThread()
    outbound_sync_thread = OutboundSyncThread()
    # Start sync listener threads.
    inbound_sync_thread.start()
    outbound_sync_thread.start()
