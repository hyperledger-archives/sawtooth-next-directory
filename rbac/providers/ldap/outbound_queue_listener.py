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
import websocket

LOGGER = logging.getLogger(__name__)


class OutboundQueueListener(object):
    """Receives updates from rethinkdb via a websocket connection
    """

    def on_open(self):
        pass

    def on_message(self, message):
        print("Received '%s'" % message)

    def on_error(self, error):
        print('OutboundQueueListener encountered an error.')
        print(error)

    def on_close(self):
        self.web_socket_app.close()
        print("Closed connection")

    def __init__(self):
        websocket.enableTrace(True)
        self.web_socket_app = websocket.WebSocketApp("ws://localhost:9090/websocket",
                                                     on_message=self.on_message,
                                                     on_error=self.on_error,
                                                     on_close=self.on_close)
        self.web_socket_app.on_open = self.on_open
        self.web_socket_app.run_forever()
