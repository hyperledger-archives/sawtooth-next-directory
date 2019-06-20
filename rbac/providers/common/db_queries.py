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
""" Database (RethinkDB) helper functions"""
from datetime import timezone
from datetime import datetime as dt
import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.providers.common.expected_errors import ExpectedError
from rbac.utils import connect_to_db

LOGGER = get_default_logger(__name__)


def get_last_sync(source, sync_type):
    """
        Search and get last sync entry from the specified source. Throws
        ExpectedError if sync_tracker table has not been initialized.
    """
    try:
        conn = connect_to_db()
        last_sync = (
            r.table("sync_tracker")
            .filter({"source": source, "sync_type": sync_type})
            .max("timestamp")
            .coerce_to("object")
            .run(conn)
        )
        conn.close()
        return last_sync
    except (r.ReqlOpFailedError, r.ReqlDriverError) as err:
        raise ExpectedError(err)
    except r.ReqlNonExistenceError:
        LOGGER.debug("The sync_tracker table is empty.")
    except Exception as err:
        LOGGER.warning(type(err).__name__)
        raise err


def save_sync_time(provider_id, sync_source, sync_type, conn, timestamp=None):
    """Saves sync time for the current data type into the RethinkDB table 'sync_tracker'."""
    if timestamp:
        last_sync_time = timestamp
    else:
        last_sync_time = dt.now().replace(tzinfo=timezone.utc).isoformat()
    sync_entry = {
        "provider_id": provider_id,
        "timestamp": last_sync_time,
        "source": sync_source,
        "sync_type": sync_type,
    }
    r.table("sync_tracker").insert(sync_entry).run(conn)


def peek_at_queue(table_name, provider_id=None):
    """Returns a single entry from table_name with the oldest timestamp and matching
    provider_id."""
    try:
        conn = connect_to_db()
        if provider_id:
            queue_entry = (
                r.table(table_name)
                .filter({"provider_id": provider_id, "status": "UNCONFIRMED"})
                .min("timestamp")
                .coerce_to("object")
                .run(conn)
            )
            conn.close()
            return queue_entry
        queue_entry = r.table(table_name).min("timestamp").coerce_to("object").run(conn)
        conn.close()
        return queue_entry
    except (r.ReqlNonExistenceError, r.ReqlOpFailedError, r.ReqlDriverError):
        return None


def put_entry_changelog(queue_entry, direction):
    """Puts the referenced document in the changelog table."""
    queue_entry["changelog_timestamp"] = dt.now().isoformat()
    queue_entry["direction"] = direction
    conn = connect_to_db()
    result = (
        r.table("changelog")
        .insert(queue_entry, return_changes=True, conflict="error")
        .run(conn)
    )
    conn.close()
    LOGGER.debug(result)


def delete_entry_queue(object_id, table_name):
    """Delete a document from the outbound queue table."""
    conn = connect_to_db()
    result = r.table(table_name).get(object_id).delete(return_changes=True).run(conn)
    conn.close()
    LOGGER.debug(result)


def update_outbound_entry_status(entry_id):
    """ Change outbound_queue entry's status from UNCONFIRMED to CONFIRMED

    Args:
        entry_id: (str) Id field of outbound_queue entry
    """
    conn = connect_to_db()
    r.table("outbound_queue").get(entry_id).update({"status": "CONFIRMED"}).run(conn)
    conn.close()
