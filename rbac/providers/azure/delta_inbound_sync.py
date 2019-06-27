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

"""
A receiver module that pulls entries from the Azure EventHub to be used by the
Inbound AAD Delta Sync.
"""
import os
from datetime import datetime
import rethinkdb as r
from azure.eventhub import EventHubClient, Offset

from rbac.common.logs import get_default_logger
from rbac.providers.common.expected_errors import ExpectedError
from rbac.providers.common.db_queries import connect_to_db, save_sync_time
from rbac.providers.common.common import check_last_sync

LOGGER = get_default_logger(__name__)

TENANT_ID = os.getenv("TENANT_ID")
NAMESPACE = os.environ.get("AAD_EH_NAMESPACE")
EVENTHUB_NAME = os.environ.get("AAD_EH_NAME")
LISTENER_POLLING_DELAY = os.environ.get("LISTENER_POLLING_DELAY", "1")

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
ADDRESS = "amqps://{}.servicebus.windows.net/{}".format(NAMESPACE, EVENTHUB_NAME)

# SAS policy and key are not required if they are encoded in the URL
USER = os.environ.get("AAD_EH_SAS_POLICY")
KEY = os.environ.get("AAD_EH_SAS_KEY")
CONSUMER_GROUP = os.environ.get("AAD_EH_CONSUMER_GROUP")
OFFSET = Offset("-1")
PARTITION = "0"


VALID_OPERATIONS = {
    "Add user": "user",
    "Add group": "group",
    "Update user": "user",
    "Update group": "group",
    "Delete user": "user",
    "Delete group": "group",
    "Hard Delete user": "user",
    "Add member to group": "group",
    "Update user attribute": "user",
    "Remove member from group": "group",
}


def inbound_sync_listener():
    """Initialize a delta inbound sync with Azure Active Directory."""
    while True:  # pylint: disable=too-many-nested-blocks
        provider_id = TENANT_ID
        try:
            initial_sync_time = check_last_sync("azure-user", "initial")
            LOGGER.info(initial_sync_time)
            LOGGER.info("This is your initial sync time")
            initial_sync_time = initial_sync_time["timestamp"][:26]
            latest_delta_sync_time = get_last_delta_sync(provider_id, "delta")
            if latest_delta_sync_time:
                latest_delta_sync_time = latest_delta_sync_time["timestamp"][:26]
                previous_sync_datetime = datetime.strptime(
                    latest_delta_sync_time, "%Y-%m-%dT%H:%M:%S.%f"
                )
            else:
                previous_sync_datetime = datetime.strptime(
                    initial_sync_time, "%Y-%m-%dT%H:%M:%S.%f"
                )
            # Create an eventhub client.
            LOGGER.info(ADDRESS)
            client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
            try:
                LOGGER.info("Opening connection to EventHub...")
                # Set prefetch to 1, we only want one event at a time.
                receiver = client.add_receiver(
                    CONSUMER_GROUP, PARTITION, prefetch=1, offset=OFFSET
                )
                # Open the connection to the EventHub.
                client.run()
                # Get one event from EventHub.
                batch = receiver.receive(timeout=5000)
                while batch:
                    for event_data in batch:
                        # Get the event as a json record from the batch of events.
                        event_json = event_data.body_as_json()
                        record = event_json["records"][0]
                        operation_name = record["operationName"]
                        time = record["time"][:26]
                        record_timestamp = datetime.strptime(
                            time, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                        # Only process events logged after the previous initial/delta sync.
                        # Only grab events concerning User or Group objects.
                        if (
                            operation_name in VALID_OPERATIONS
                            and record_timestamp > previous_sync_datetime
                        ):
                            data = {
                                "initated_by": record["properties"]["initiatedBy"],
                                "target_resources": record["properties"][
                                    "targetResources"
                                ],
                                "operation_name": operation_name,
                                "resultType": record["resultType"],
                            }
                            LOGGER.info("Operation name: %s", operation_name)
                            LOGGER.info("Record to Change: %s", record)
                            record_timestamp_utc = record_timestamp.isoformat()
                            insert_change_to_db(data, record_timestamp_utc)
                            sync_source = "azure-" + VALID_OPERATIONS[operation_name]
                            provider_id = TENANT_ID
                            conn = connect_to_db()
                            save_sync_time(
                                provider_id,
                                sync_source,
                                "delta",
                                conn,
                                record_timestamp_utc,
                            )
                            conn.close()
                            previous_sync_datetime = record_timestamp
                    batch = receiver.receive(timeout=50)
                LOGGER.info("Closing connection to EventHub...")
                # Close the connection to the EventHub.
                client.stop()
            except KeyboardInterrupt:
                pass
            finally:
                client.stop()
        except ExpectedError as err:
            LOGGER.debug(
                (
                    "%s Repolling after %s seconds...",
                    err.__str__,
                    LISTENER_POLLING_DELAY,
                )
            )
            time.sleep(LISTENER_POLLING_DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err


def insert_change_to_db(data, record_timestamp):
    """Insert change individually to rethinkdb from changelog eventhub of azure"""
    inbound_entry = {
        "data": data,
        "data_type": VALID_OPERATIONS[data["operation_name"]],
        "sync_type": "delta",
        "timestamp": record_timestamp,
        "provider_id": TENANT_ID,
    }
    conn = connect_to_db()
    r.table("inbound_queue").insert(inbound_entry).run(conn)
    conn.close()


def get_last_delta_sync(provider_id, sync_type):
    """Search and get last delta sync entry from the specified provider."""
    try:
        conn = connect_to_db()
        last_sync = (
            r.table("sync_tracker")
            .filter({"provider_id": provider_id, "sync_type": sync_type})
            .max("timestamp")
            .coerce_to("object")
            .run(conn)
        )
        conn.close()
        return last_sync
    except r.ReqlNonExistenceError:
        return None
    except (r.ReqlOpFailedError, r.ReqlDriverError) as err:
        raise ExpectedError(err)
    except Exception as err:
        LOGGER.warning(type(err).__name__)
        raise err
