# Copyright 2017 Intel Corporation
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

from sawtooth_sdk.messaging.stream import Stream
from sawtooth_sdk.protobuf.state_delta_pb2 import StateDeltaSubscribeRequest
from sawtooth_sdk.protobuf.state_delta_pb2 import StateDeltaSubscribeResponse
from sawtooth_sdk.protobuf.state_delta_pb2 import StateDeltaEvent
from sawtooth_sdk.protobuf.state_delta_pb2 import StateDeltaUnsubscribeRequest
from sawtooth_sdk.protobuf.state_delta_pb2 import StateDeltaUnsubscribeResponse
from sawtooth_sdk.protobuf.validator_pb2 import Message


LOGGER = logging.getLogger(__name__)


class Subscriber(object):
    """Creates an object that can subscribe to state delta events using the
    Sawtooth SDK's Stream class. Handler functions can be added prior to
    subscribing, and each will be called on each delta event received.
    """
    def __init__(self, validator_url):
        LOGGER.info('Connecting to validator: %s', validator_url)
        self._stream = Stream(validator_url)
        self._delta_handlers = []
        self._is_active = False

    def add_handler(self, event_handler):
        """Adds a handler which will be passed state delta events when they
        occur. Note that this event is mutable.
        """
        self._delta_handlers.append(event_handler)

    def clear_handlers(self):
        """Clears any delta handlers.
        """
        self._delta_handlers = []

    def start(self):
        """Subscribes to state delta events, and then waits to receive deltas.
        Sends any events received to delta handlers.
        """
        self._stream.wait_for_ready()

        LOGGER.debug('Subscribing to state delta events')
        request = StateDeltaSubscribeRequest()
        response_future = self._stream.send(
            Message.STATE_DELTA_SUBSCRIBE_REQUEST,
            request.SerializeToString())
        response = StateDeltaSubscribeResponse()
        response.ParseFromString(response_future.result().content)

        if response.status != StateDeltaSubscribeResponse.OK:
            raise RuntimeError(
                'Subscription failed with status: {}'.format(
                    StateDeltaSubscribeResponse.Status.Name(response.status)))

        self._is_active = True

        LOGGER.debug('Successfully subscribed to state delta events')
        while self._is_active:
            message_future = self._stream.receive()

            event = StateDeltaEvent()
            event.ParseFromString(message_future.result().content)
            LOGGER.debug('Received deltas for block: %s', event.block_id)

            for handler in self._delta_handlers:
                handler(event)

    def stop(self):
        """Stops the Subscriber, unsubscribing from state delta events and
        closing the the stream's connection.
        """
        self._is_active = False

        LOGGER.debug('Unsubscribing from state delta events')
        request = StateDeltaUnsubscribeRequest()
        response_future = self._stream.send(
            Message.STATE_DELTA_UNSUBSCRIBE_REQUEST,
            request.SerializeToString())
        response = StateDeltaUnsubscribeResponse()
        response.ParseFromString(response_future.result().content)

        if response.status != StateDeltaUnsubscribeResponse.OK:
            LOGGER.warning(
                'Failed to unsubscribe with status: %s',
                StateDeltaUnsubscribeResponse.Status.Name(response.status))

        self._stream.close()
