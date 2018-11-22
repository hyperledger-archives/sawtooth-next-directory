#! /usr/bin/env python3

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

import logging
import sys
import time
from datetime import datetime as dt
from datetime import timezone
import rethinkdb as r

from rbac.providers.common.expected_errors import ExpectedError

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DELAY = 1


def save_sync_time(sync_source, sync_type):
    """Saves sync time for the current data type into the RethinkDB table 'sync_tracker'."""
    last_sync_time = dt.now().replace(tzinfo=timezone.utc).isoformat()
    sync_entry = {
        "timestamp": last_sync_time,
        "source": sync_source,
        "sync_type": sync_type,
    }
    r.table("sync_tracker").insert(sync_entry).run()


def get_last_sync(source, sync_type):
    """
        Search and get last sync entry from the specified source. Throws
        ExpectedError if sync_tracker table has not been initialized.
    """
    try:
        last_sync = (
            r.table("sync_tracker")
            .filter({"source": source, "sync_type": sync_type})
            .coerce_to("array")
            .run()
        )
        return last_sync
    except (r.ReqlOpFailedError, r.ReqlDriverError) as err:
        raise ExpectedError(err)
    except Exception as err:
        LOGGER.warning(type(err).__name__)
        raise err


def check_last_sync(sync_source, sync_type):
    """
        Check to see if a sync has occurred and return payload. If the
        the sync_tracker table is not initialized, this function will
        keep checking until the table has been initialized.
    """
    LOGGER.debug("Checking for previous %s initial sync...", sync_source)
    while True:
        try:
            db_payload = get_last_sync(sync_source, sync_type)
            return db_payload
        except ExpectedError:
            LOGGER.debug(
                "Sync tracker table has not been initialized. Checking again in %s seconds",
                DELAY,
            )
            time.sleep(DELAY)
            continue
        except Exception as err:
            LOGGER.warning(type(err).__name__)
            raise err
