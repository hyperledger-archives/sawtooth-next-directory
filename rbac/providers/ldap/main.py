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

import logging
import sys

from tornado import ioloop

from rbac.providers.ldap.outbound_queue_listener import export_feed_change_to_ldap

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def start_listener():

    try:
        LOGGER.debug("Starting outbound queue listener")
        # TODO: This only processes feed change data. We also need to process pre-existing records keeping in mind
        # the risk of horizontal scaling (multinode) race conditions
        ioloop.IOLoop.current().run_sync(export_feed_change_to_ldap)

    except KeyboardInterrupt:
        pass
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.error("Encountered an error running the outbound queue listener")
        LOGGER.exception(err)
        sys.exit(1)
