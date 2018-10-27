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

from rbac.providers.ldap.outbound_queue_listener import print_feed_change_data

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def start_listener():

    try:
        LOGGER.debug("Starting outbound queue listener")
        # ioloop.IOLoop.current().add_callback(outbound_queue_listener.print_feed_change_data(connection_args=opts))
        ioloop.IOLoop.current().run_sync(print_feed_change_data)

    except KeyboardInterrupt:
        pass
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(err)
        sys.exit(1)
