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

from sawtooth_sdk.messaging.stream import Stream
from sawtooth_sdk.protobuf import client_event_pb2
from sawtooth_sdk.protobuf import events_pb2
from sawtooth_sdk.protobuf import transaction_receipt_pb2
from sawtooth_sdk.protobuf.validator_pb2 import Message

from rbac.common import addresser


LOGGER = logging.getLogger(__name__)


class Subscriber(object):
    """Creates an object that can subscribe to state delta events using the
    Sawtooth SDK's Stream class. Handler functions can be added prior to
    subscribing, and each will be called on each delta event received.
    """

    def __init__(self, validator_url):
        LOGGER.info("Connecting to validator: %s", validator_url)
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

    def start(self, known_ids=None):
        """Subscribes to state delta events, and then waits to receive deltas.
        Sends any events received to delta handlers.
        """
        self._stream.wait_for_ready()

        LOGGER.debug("Subscribing to client state events")
        request = client_event_pb2.ClientEventsSubscribeRequest(
            last_known_block_ids=known_ids,
            subscriptions=[
                events_pb2.EventSubscription(event_type="sawtooth/block-commit"),
                events_pb2.EventSubscription(
                    event_type="sawtooth/state-delta",
                    filters=[
                        events_pb2.EventFilter(
                            key="address",
                            match_string="^" + addresser.family.namespace + ".*",
                            filter_type=events_pb2.EventFilter.REGEX_ANY,
                        )
                    ],
                ),
            ],
        )

        response_future = self._stream.send(
            Message.CLIENT_EVENTS_SUBSCRIBE_REQUEST, request.SerializeToString()
        )
        response = client_event_pb2.ClientEventsSubscribeResponse()
        response.ParseFromString(response_future.result().content)

        # Forked all the way back to genesis, restart with no known_ids
        if (
            known_ids
            and response.status
            == client_event_pb2.ClientEventsSubscribeResponse.UNKNOWN_BLOCK
        ):
            return self.start()

        if response.status != client_event_pb2.ClientEventsSubscribeResponse.OK:
            raise RuntimeError(
                "Subscription failed with status: {}".format(
                    client_event_pb2.ClientEventsSubscribeResponse.Status.Name(
                        response.status
                    )
                )
            )

        self._is_active = True

        LOGGER.debug("Successfully subscribed to state delta events")
        while self._is_active:
            message_future = self._stream.receive()
            msg = message_future.result()

            if msg.message_type == Message.CLIENT_EVENTS:
                event_list = events_pb2.EventList()
                event_list.ParseFromString(msg.content)
                events = list(event_list.events)
                event = StateDeltaEvent(events)

                delta_count = len(event.state_changes)
                if delta_count > 0:
                    for handler in self._delta_handlers:
                        handler(event)

    def stop(self):
        """Stops the Subscriber, unsubscribing from state delta events and
        closing the the stream's connection.
        """
        self._is_active = False

        LOGGER.debug("Unsubscribing from client events")
        request = client_event_pb2.ClientEventsUnsubscribeResponse()
        response_future = self._stream.send(
            Message.CLIENT_EVENTS_UNSUBSCRIBE_REQUEST, request.SerializeToString()
        )
        response = client_event_pb2.ClientEventsUnsubscribeResponse()
        response.ParseFromString(response_future.result().content)

        if response.status != client_event_pb2.ClientEventsUnsubscribeResponse.OK:
            LOGGER.warning(
                "Failed to unsubscribe with status: %s",
                client_event_pb2.ClientEventsUnsubscribeResponse.Status.Name(
                    response.status
                ),
            )

        self._stream.close()


class StateDeltaEvent:
    def __init__(self, event_list):
        """
        Convert an event list into an object that is similar to the previous
        state delta event for compatibility.
        Raises
            KeyError
                An event was missing from the event list or an attribute was
                missing from an event.
        """
        block_commit = self._get_event("sawtooth/block-commit", event_list)
        self.block_id = self._get_attr(block_commit, "block_id")
        self.block_num = self._get_attr(block_commit, "block_num")
        self.previous_block_id = self._get_attr(block_commit, "previous_block_id")
        self.state_root_hash = self._get_attr(block_commit, "state_root_hash")

        try:
            state_delta = self._get_event("sawtooth/state-delta", event_list)
            state_change_list = transaction_receipt_pb2.StateChangeList()
            state_change_list.ParseFromString(state_delta.data)
            self.state_changes = state_change_list.state_changes
        except KeyError:
            self.state_changes = []

    @staticmethod
    def _get_attr(event, key):
        attrs = list(filter(lambda attr: attr.key == key, event.attributes))
        if attrs:
            return attrs[0].value
        raise KeyError("Key '%s' not found in event attributes" % key)

    @staticmethod
    def _get_event(event_type, event_list):
        events = list(filter(lambda event: event.event_type == event_type, event_list))
        if events:
            return events[0]
        raise KeyError("Event type '%s' not found" % event_type)
