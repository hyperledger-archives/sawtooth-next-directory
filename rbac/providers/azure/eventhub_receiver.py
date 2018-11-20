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
An example to show receiving events from an Event Hub partition.
"""
import os
import sys
import logging
import time
from azure.eventhub import EventHubClient, Receiver, Offset

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

NAMESPACE = os.environ.get("AAD_EH_NAMESPACE")

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
ADDRESS = f"amqps://{NAMESPACE}.servicebus.windows.net/myeventhub"

# SAS policy and key are not required if they are encoded in the URL
USER = os.environ.get('AAD_EH_SAS_POLICY')
KEY = os.environ.get('AAD_EH_SAS_KEY')
CONSUMER_GROUP = "$default"
OFFSET = Offset("-1")
PARTITION = "0"


total = 0
last_sn = -1
last_offset = "-1"
client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
try:
    receiver = client.add_receiver(CONSUMER_GROUP, PARTITION, prefetch=5000, offset=OFFSET)
    client.run()
    start_time = time.time()
    batch = receiver.receive(timeout=5000)
    while batch:
        for event_data in batch:
            last_offset = event_data.offset
            last_sn = event_data.sequence_number
            print("Received: {}, {}".format(last_offset.value, last_sn))
            print(event_data.body_as_str())
            total += 1
        batch = receiver.receive(timeout=5000)

    end_time = time.time()
    client.stop()
    run_time = end_time - start_time
    print("Received {} messages in {} seconds".format(total, run_time))

except KeyboardInterrupt:
    pass
finally:
    client.stop()