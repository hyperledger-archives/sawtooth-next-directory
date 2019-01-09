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
""" Functions that are common to all providers.
"""
import time

from rbac.common.logs import get_logger
from rbac.providers.common.expected_errors import ExpectedError
from rbac.providers.common.db_queries import get_last_sync

LOGGER = get_logger(__name__)


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
                "Sync tracker table has not been initialized. Checking again in 1 second"
            )
            time.sleep(1)
            continue
        except Exception as err:
            LOGGER.warning(type(err).__name__)
            raise err
