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
"""Test the Sawtooth batch helper class"""

# pylint: disable=no-member

import logging
import pytest

from rbac.common import addresser
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import user_transaction_pb2
from rbac.common.sawtooth import batcher
from rbac.common.sawtooth.batcher import BATCHER_KEY_PAIR
from rbac.common.crypto.keys import Key
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.library
@pytest.mark.batch
class TestBatchClient(TestAssertions):
    """Test the Sawtooth batch helper class"""

    def get_test_inputs(self, message_type=RBACPayload.CREATE_USER):
        """Returns test data inputs for testing batcher functions"""
        if message_type == RBACPayload.CREATE_USER:
            signer = Key()
            message = user_transaction_pb2.CreateUser(name="foobar")
            message.user_id = signer.public_key
            inputs = [addresser.user.address(message.user_id)]
            outputs = inputs
            return message, message_type, inputs, outputs, signer

        raise Exception(
            "batcher test doesn't support message_type: {}".format(message_type)
        )

    def get_test_payload(self):
        """Returns a test data payload for testing batcher functions"""
        message, message_type, inputs, outputs, signer = self.get_test_inputs()
        return (
            batcher.make_payload(
                message=message,
                message_type=message_type,
                inputs=inputs,
                outputs=outputs,
            ),
            signer,
        )

    def test_get_test_inputs(self):
        """Verifies the test data inputs function returns the expected test data"""
        message, message_type, inputs, outputs, signer = self.get_test_inputs()
        self.assertIsInstance(signer, Key)
        self.assertEqual(message_type, RBACPayload.CREATE_USER)
        self.assertIsInstance(message, user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.name, str)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(len(outputs), 1)
        self.assertEqual(
            addresser.get_address_type(inputs[0]), addresser.AddressSpace.USER
        )
        self.assertEqual(
            addresser.get_address_type(outputs[0]), addresser.AddressSpace.USER
        )

    def test_make_payload(self):
        """Test the make payload batch function"""
        message, message_type, inputs, outputs, signer = self.get_test_inputs()
        payload = batcher.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )
        self.assertIsInstance(payload, RBACPayload)
        self.assertEqual(payload.message_type, message_type)
        self.assertEqual(payload.inputs, inputs)
        self.assertEqual(payload.outputs, outputs)
        self.assertIsInstance(signer, Key)
        self.assertValidPayload(
            payload=payload, message=message, message_type=message_type
        )

    def test_unmake_payload(self):
        """Test the unmake batch function"""
        message, message_type, inputs, outputs, signer = self.get_test_inputs()
        payload = batcher.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )
        messages = batcher.unmake(
            batch_object=payload, signer_public_key=signer.public_key
        )
        self.assertEqual(len(messages), 1)
        self.assertEqualMessage(message, messages[0])

    def test_get_test_payload(self):
        """Verifies the test data payload function returns the expected test data"""
        payload, signer = self.get_test_payload()
        self.assertIsInstance(payload, RBACPayload)
        self.assertIsInstance(signer, Key)

    def test_unmake(self):
        """Test the unmake batch function with a single message"""
        message, message_type, inputs, outputs, signer_keypair = self.get_test_inputs()
        payload = batcher.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )
        transaction, batch, batch_list, batch_request = batcher.make(
            payload=payload, signer_keypair=signer_keypair
        )
        messages = batcher.unmake(
            batch_object=payload, signer_public_key=signer_keypair.public_key
        )
        self.assertEqual(len(messages), 1)
        self.assertEqualMessage(message, messages[0])

        messages = batcher.unmake(
            batch_object=transaction, signer_public_key=signer_keypair.public_key
        )
        self.assertEqual(len(messages), 1)
        self.assertEqualMessage(message, messages[0])

        messages = batcher.unmake(
            batch_object=batch, signer_public_key=signer_keypair.public_key
        )
        self.assertEqual(len(messages), 1)
        self.assertEqualMessage(message, messages[0])

        messages = batcher.unmake(
            batch_object=batch_list, signer_public_key=signer_keypair.public_key
        )
        self.assertEqual(len(messages), 1)
        self.assertEqualMessage(message, messages[0])

        messages = batcher.unmake(
            batch_object=batch_request, signer_public_key=signer_keypair.public_key
        )
        self.assertEqual(len(messages), 1)
        self.assertEqualMessage(message, messages[0])

    def test_make_transaction_header(self):
        """Test the make transaction header batch function"""
        payload, signer = self.get_test_payload()

        header, signature = batcher.make_transaction_header(
            payload=payload, signer_keypair=signer
        )

        self.assertValidTransactionHeader(
            header=header,
            signature=signature,
            payload=payload,
            signer_public_key=signer.public_key,
        )

    def test_make_transaction(self):
        """Test the make transaction batch function"""
        payload, signer = self.get_test_payload()

        transaction = batcher.make_transaction(payload=payload, signer_keypair=signer)

        self.assertValidTransaction(
            transaction=transaction,
            payload=payload,
            signer_public_key=signer.public_key,
        )

    def test_make_batch(self):
        """Test the make batch batch function"""
        payload, signer = self.get_test_payload()

        transaction = batcher.make_transaction(payload=payload, signer_keypair=signer)

        batch = batcher.make_batch(transaction=transaction)

        self.assertValidBatch(
            batch=batch,
            payload=payload,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )

    def test_batch_to_list(self):
        """Test the make batch to list batch function"""
        payload, signer = self.get_test_payload()

        transaction = batcher.make_transaction(payload=payload, signer_keypair=signer)

        batch = batcher.make_batch(transaction=transaction)

        batch_list = batcher.batch_to_list(batch)

        self.assertValidBatchList(
            batch_list=batch_list,
            payload=payload,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )

    def test_make_batch_list(self):
        """Test the make batch list batch function"""
        payload, signer = self.get_test_payload()

        transaction = batcher.make_transaction(payload=payload, signer_keypair=signer)

        batch_list = batcher.make_batch_list(transaction=transaction)

        self.assertValidBatchList(
            batch_list=batch_list,
            payload=payload,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )

    def test_make_batch_request(self):
        """Test the make batch request batch function"""
        payload, signer = self.get_test_payload()

        transaction = batcher.make_transaction(payload=payload, signer_keypair=signer)

        batch_list = batcher.make_batch_list(transaction=transaction)

        batch_request = batcher.make_batch_request(batch_list=batch_list)

        self.assertValidBatchRequest(
            batch_request=batch_request,
            payload=payload,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )

    def test_make(self):
        """Test the make batch function"""
        payload, signer = self.get_test_payload()

        transaction, batch, batch_list, batch_request = batcher.make(
            payload=payload, signer_keypair=signer
        )
        self.assertValidTransaction(
            transaction=transaction,
            payload=payload,
            signer_public_key=signer.public_key,
        )
        self.assertValidBatch(
            batch=batch,
            payload=payload,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )
        self.assertValidBatchList(
            batch_list=batch_list,
            payload=payload,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )
        self.assertValidBatchRequest(
            batch_request=batch_request,
            payload=payload,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )
