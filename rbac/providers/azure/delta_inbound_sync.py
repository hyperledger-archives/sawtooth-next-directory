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

"""
A receiver module that pulls entries from the Azure EventHub to be used by the 
Inbound AAD Delta Sync.
"""
import os
import sys
import logging
import time
from datetime import datetime
from rbac.providers.common.expected_errors import ExpectedError
from azure.eventhub import EventHubClient, Receiver, Offset

from rbac.providers.common.inbound_filters import (
    inbound_user_filter,
    inbound_group_filter,
)

from rbac.providers.common.rethink_db import (
    connect_to_db
)

from rbac.providers.common.common import save_sync_time, check_last_sync

DELAY = os.environ.get("DELAY")

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

NAMESPACE = os.environ.get("AAD_EH_NAMESPACE")
EVENTHUB_NAME = os.environ.get("AAD_EH_NAME")

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
ADDRESS = f"amqps://{NAMESPACE}.servicebus.windows.net/{EVENTHUB_NAME}"

# SAS policy and key are not required if they are encoded in the URL
USER = os.environ.get("AAD_EH_SAS_POLICY")
KEY = os.environ.get("AAD_EH_SAS_KEY")
CONSUMER_GROUP = os.environ.get("AAD_EH_CONSUMER_GROUP")
OFFSET = Offset("-1")
PARTITION = "0"

VALID_OPERATIONS = [
    "Add user",
    "Add group",
    "Update user",
    "Update group",
    "Delete user",
    "Delete group",
    "Hard Delete user",
    "Add member to group",
    "Update user attribute",
    "Remove member from group",
]

def inbound_sync_listener():
    while True:
        try:
            LOGGER.info("Connecting to RethinkDB...")
            connect_to_db()
            LOGGER.info("Successfully connected to RethinkDB!")

            previous_sync_time = check_last_sync("azure-user", "initial")[0]['timestamp'][:26]
            previous_sync_datetime = datetime.strptime(previous_sync_time, "%Y-%m-%dT%H:%M:%S.%f")
            
            LOGGER.info("Previous sync time: %s", previous_sync_datetime)

            # Create an eventhub client.
            client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
            try:
                LOGGER.info("Opening connection to EventHub...")
                # Set prefetch to 1, we only want one event at a time.
                receiver = client.add_receiver(CONSUMER_GROUP, PARTITION, prefetch=1, offset=OFFSET)
                # Open the connection to the EventHub.
                client.run()
                # Get one event from EventHub.
                batch = receiver.receive(timeout=5000)
                while batch:
                    for event_data in batch:
                        # Get the event as a json record from the batch of events.
                        event_json = event_data.body_as_json()
                        record = event_json['records'][0]
                        operation_name = record['operationName']
                        time = record['time'][:26]
                        date_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
                        # Only process events logged after the previous initial/delta sync.
                        # Only grab events concerning User or Group objects.
                        if operation_name in VALID_OPERATIONS and date_time <= previous_sync_datetime:
                            for resource in record['properties']['targetResources']:
                                # TODO: Put User or Group object into the inbound queue.
                                # TODO: Update previous sync time.
                                LOGGER.info("Operation name: %s", operation_name)
                                LOGGER.info("Resource: %s", resource)
                    batch = receiver.receive(timeout=5000)
                LOGGER.info("Closing connection to EventHub...")
                # Close the connection to the EventHub.
                client.stop()
            except KeyboardInterrupt:
                pass
            finally:
                client.stop()
        except ExpectedError as err:
                LOGGER.debug(("%s Repolling after %s seconds...", err.__str__, DELAY))
                time.sleep(DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
