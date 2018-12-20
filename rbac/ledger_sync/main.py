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
"""Starts all Ledger Sync processes
"""
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

from rbac.common.logs import get_logger
from rbac.ledger_sync.outbound.listener import listener as outbound
from rbac.ledger_sync.inbound.listener import listener as inbound

LOGGER = get_logger(__name__)
SCHEDULER = BlockingScheduler()


def main():
    """Starts all Ledger Sync processes
    """
    try:
        SCHEDULER.add_job(outbound)
        SCHEDULER.add_job(inbound)
        SCHEDULER.start()

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception("Exception occured in Ledger Sync!")
        LOGGER.exception(err)
        sys.exit(1)

    finally:
        LOGGER.info("Ledger Sync shut down")
