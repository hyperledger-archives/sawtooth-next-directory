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
""" Threading classes used for provider syncs
"""
import threading

from rbac.common.logs import get_logger

LOGGER = get_logger(__name__)


class DeltaSyncThread(threading.Thread):
    """Custom class that runs a delta sync listener in its thread."""

    def __init__(self, name, function):
        """Initialize the OutboundSyncThread class"""
        threading.Thread.__init__(self)
        self.name = "{} Delta Sync Thread".format(name)
        self.function_to_thread = function

    def run(self):
        """Start the OutboundSyncThread"""
        LOGGER.info("Starting %s", self.name)
        self.function_to_thread()
        LOGGER.info("Exiting %s", self.name)
