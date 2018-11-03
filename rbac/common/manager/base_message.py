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
from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.crypto.keys import PUBLIC_KEY_PATTERN
from rbac.common.sawtooth.batcher import Batcher
from rbac.common.sawtooth.state_client import StateClient
from rbac.common.sawtooth.client_sync import ClientSync


LOGGER = logging.getLogger(__name__)


class BaseMessage:
    def __init__(self):
        """Objects and methods shared across message libraries"""
        self.batch = Batcher()
        self.client = ClientSync()
        self.state = StateClient()

    def getattr(self, item, attribute):
        """A version of getattr that will return None if attributes
        is not found on the item"""
        if hasattr(item, attribute):
            return getattr(item, attribute)
        return None

    @property
    def name(self):
        raise NotImplementedError("Class must implement this property")

    @property
    def names(self):
        return self.name + "s"

    @property
    def message_type(self):
        raise NotImplementedError("Class must implement this method")

    @property
    def message_proto(self):
        raise NotImplementedError("Class must implement this method")

    @property
    def container_proto(self):
        raise NotImplementedError("Class must implement this method")

    @property
    def state_proto(self):
        raise NotImplementedError("Class must implement this method")

    @property
    def message_fields_not_in_state(self):
        """Fields that are on the message but not stored on the state object"""
        return []

    def address(self, object_id, target_id):
        raise NotImplementedError("Class must implement this method")

    def make(self, object_id):
        raise NotImplementedError("Class must implement this method")

    def make_addresses(self, message, signer_keypair):
        raise NotImplementedError("Class must implement this method")

    def base_validate(self, message, signer=None):
        if not isinstance(message, self.message_proto):
            raise TypeError("Expected message to be {}".format(self.message_proto))
        if (
            signer is not None
            and not isinstance(signer, Key)
            and not (isinstance(signer, str) and PUBLIC_KEY_PATTERN.match(signer))
        ):
            raise TypeError("Expected signer to be a keypair or a public key")
        if isinstance(signer, Key):
            signer = signer.public_key
        return signer

    def base_validate_state(self, state, message, signer):
        if signer is None:
            raise ValueError("Signer is required")
        if not isinstance(signer, str) and PUBLIC_KEY_PATTERN.match(signer):
            raise TypeError("Expected signer to be a public key")
        if state is None:
            raise ValueError("State is required")

    def validate(self, message, signer=None):
        signer = self.base_validate(message=message, signer=signer)

    def make_payload(self, message, signer_keypair=None):
        """Make a payload for the given message type"""
        self.validate(message=message, signer=signer_keypair)

        message_type = self.message_type
        inputs, outputs = self.make_addresses(
            message=message, signer_keypair=signer_keypair
        )
        return self.batch.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )

    def create(self, signer_keypair, message, object_id=None, target_id=None):
        """Send a message to the blockchain"""
        self.validate(message=message, signer=signer_keypair)

        return self.send(
            signer_keypair=signer_keypair,
            payload=self.make_payload(message=message, signer_keypair=signer_keypair),
            object_id=object_id,
            target_id=target_id,
        )

    def send(self, signer_keypair, payload, object_id=None, target_id=None):
        """Sends a payload to the transaction processor"""
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")
        if not isinstance(payload, protobuf.rbac_payload_pb2.RBACPayload):
            raise TypeError("Expected payload to be an RBACPayload")

        _, _, batch_list, _ = self.batch.make(
            payload=payload, signer_keypair=signer_keypair
        )
        got = None

        status = self.client.send_batches_get_status(batch_list=batch_list)

        if object_id is not None:
            got = self.get(object_id=object_id, target_id=target_id)

        return got, status

    def _find_in_container(self, container, address, object_id, target_id=None):
        items = list(getattr(container, self.names))
        if len(items) == 0:
            return None
        elif len(items) > 1:
            LOGGER.warning(
                "%s container for %s target %s has more than one record at address %s",
                self.name,
                object_id,
                target_id,
                address,
            )
        for item in items:
            if (
                self.getattr(item, "object_id") == object_id
                and self.getattr(item, "target_id") == target_id
            ):
                return item
            if self.getattr(item, self.name + "_id") == object_id and target_id is None:
                return item
        LOGGER.warning(
            "%s not found in container for %s target %s at address %s",
            self.name,
            object_id,
            target_id,
            address,
        )
        return None

    def get(self, object_id, target_id=None):
        """Gets an address from the blockchain from the API"""
        address = self.address(object_id=object_id, target_id=target_id)
        container = self.container_proto()
        container.ParseFromString(self.client.get_address(address=address))
        return self._find_in_container(
            container=container,
            address=address,
            object_id=object_id,
            target_id=target_id,
        )

    def get_state(self, state, object_id, target_id=None):
        """Gets an address from the blockchain state from the state object"""
        address = self.address(object_id=object_id, target_id=target_id)
        container = self.container_proto()

        results = self.state.get_address(state=state, address=address)
        if len(list(results)) == 0:
            return None

        container.ParseFromString(results[0].data)
        return self._find_in_container(
            container=container,
            address=address,
            object_id=object_id,
            target_id=target_id,
        )

    def exists_state(self, state, object_id, target_id=None):
        """Checks an object exists in the blockchain"""
        got = self.get_state(state=state, object_id=object_id, target_id=target_id)
        return bool(got is not None)
