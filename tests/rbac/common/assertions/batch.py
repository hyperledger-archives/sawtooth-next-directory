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
"""Batch assertion helpers"""
# pylint: disable=no-member,invalid-name

import logging
import json
from hashlib import sha512
from google.protobuf import json_format

from sawtooth_sdk.protobuf import transaction_pb2
from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import client_batch_submit_pb2

from rbac.common.crypto.keys import Key
from rbac.common import addresser
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import user_transaction_pb2
from rbac.common.sawtooth.rbac_payload import unmake_payload
from tests.rbac.common.assertions.address import AddressAssertions

LOGGER = logging.getLogger(__name__)


class BatchAssertions(AddressAssertions):
    """Address assertion helpers"""

    def assertEqualMessage(self, message1, message2, ignored_fields=None):
        """A shallow comparison of the the json representation
        of two messages"""
        self.assertIsNotNone(message1)
        self.assertIsNotNone(message2)
        message1 = json.loads(json_format.MessageToJson(message1))
        message2 = json.loads(json_format.MessageToJson(message2))
        for prop in message1:
            if ignored_fields is None or prop not in ignored_fields:
                self.assertEqual(message1[prop], message2[prop])
        for prop in message2:
            if ignored_fields is None or prop not in ignored_fields:
                self.assertEqual(message2[prop], message1[prop])

    def assertEqualPayload(self, payload1, payload2):
        """Check that two payloads are the equivalent"""
        message1, message_payload1 = unmake_payload(payload1)
        message2, message_payload2 = unmake_payload(payload2)
        self.assertEqual(message_payload1.message_type, message_payload2.message_type)
        self.assertEqual(message_payload1.inputs, message_payload2.inputs)
        self.assertEqual(message_payload1.outputs, message_payload2.outputs)
        self.assertEqualMessage(message1, message2)
        self.assertEqual(
            message_payload1.signer.user_id, message_payload2.signer.user_id
        )
        self.assertEqual(
            message_payload1.signer.public_key, message_payload2.signer.public_key
        )

    # override this for in each *_manager_test for appropriate message_type inputs/outputs
    def assertValidPayload(self, payload, message, message_type):
        """Check a payload the valid representation of a message given its type"""
        if isinstance(payload, bytes):
            decoded = RBACPayload()
            decoded.ParseFromString(payload)
            payload = decoded
        self.assertIsInstance(payload, RBACPayload)
        if message_type == RBACPayload.CREATE_USER:
            self.assertIsInstance(message, user_transaction_pb2.CreateUser)
            self.assertEqual(message_type, RBACPayload.CREATE_USER)
            decoded = user_transaction_pb2.CreateUser()
            decoded.ParseFromString(payload.content)
            self.assertEqual(decoded, message)
            self.assertEqual(decoded.name, message.name)
        else:
            raise Exception(
                "BatchAssertions.assertValidPayload doesn't support message_type {}".format(
                    message_type
                )
            )

    def assertValidInputs(self, inputs, outputs, message_type):
        """Check the inputs and outputs match the expected message type"""
        if inputs is not None and not isinstance(inputs, list):
            inputs = list(inputs)
        if outputs is not None and not isinstance(outputs, list):
            outputs = list(outputs)

        if message_type == RBACPayload.CREATE_USER:
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
        else:
            raise Exception(
                "BatchAssertions.assertValidInputs doesn't support message_type {}".format(
                    message_type
                )
            )

    def assertValidTransactionHeader(
        self, header, signature, payload, signer_public_key
    ):
        """Check a transaction header is valid given a payload"""
        if isinstance(header, bytes):
            decoded = transaction_pb2.TransactionHeader()
            decoded.ParseFromString(header)
            header = decoded

        self.assertIsInstance(header, transaction_pb2.TransactionHeader)
        self.assertEqual(header.family_name, addresser.family.name)
        self.assertEqual(header.family_version, addresser.family.version)
        self.assertIsInstance(header.nonce, str)
        self.assertEqual(len(header.nonce), 32)
        self.assertEqual(header.signer_public_key, signer_public_key)
        self.assertEqual(
            header.payload_sha512, sha512(payload.SerializeToString()).hexdigest()
        )
        signer = Key(public_key=signer_public_key)
        self.assertTrue(
            signer.verify(signature=signature, message=header.SerializeToString())
        )
        other_key = Key()
        self.assertFalse(
            other_key.verify(signature=signature, message=header.SerializeToString())
        )

        self.assertEqual(header.inputs, payload.inputs)
        self.assertEqual(header.outputs, payload.outputs)

    def assertValidTransaction(self, transaction, payload, signer_public_key):
        """Check a transaction is valid given a payload"""
        if isinstance(transaction, bytes):
            decoded = transaction_pb2.Transaction()
            decoded.ParseFromString(transaction)
            transaction = decoded
        self.assertIsInstance(transaction, transaction_pb2.Transaction)
        self.assertValidTransactionHeader(
            header=transaction.header,
            signature=transaction.header_signature,
            payload=payload,
            signer_public_key=signer_public_key,
        )
        self.assertEqualPayload(payload1=transaction.payload, payload2=payload)
        message, message_payload = unmake_payload(payload)
        self.assertValidPayload(
            payload=transaction.payload,
            message=message,
            message_type=message_payload.message_type,
        )

    def assertValidBatch(self, batch, payload, signer_public_key, batcher_public_key):
        """Check a batch is valid given a payload"""
        self.assertIsInstance(batch, batch_pb2.Batch)
        batch_header = batch_pb2.BatchHeader()
        batch_header.ParseFromString(batch.header)
        self.assertIsInstance(batch_header, batch_pb2.BatchHeader)
        self.assertEqual(batch_header.signer_public_key, batcher_public_key)
        batcher_keypair = Key(public_key=batcher_public_key)
        self.assertTrue(
            batcher_keypair.verify(
                signature=batch.header_signature,
                message=batch_header.SerializeToString(),
            )
        )
        other_key = Key()
        self.assertFalse(
            other_key.verify(
                signature=batch.header_signature,
                message=batch_header.SerializeToString(),
            )
        )

        transactions = list(batch.transactions)
        self.assertEqual(len(transactions), 1)

        self.assertValidTransaction(
            transaction=transactions[0],
            payload=payload,
            signer_public_key=signer_public_key,
        )

    def assertValidBatchList(
        self, batch_list, payload, signer_public_key, batcher_public_key
    ):
        """Check a batch list is valid given a payload"""
        self.assertIsInstance(batch_list, batch_pb2.BatchList)
        # batch_list = list(batch_list)
        batch_count = 0
        for batch in batch_list.batches:
            batch_count += 1
            self.assertIsInstance(batch, batch_pb2.Batch)
            self.assertValidBatch(
                batch=batch,
                payload=payload,
                signer_public_key=signer_public_key,
                batcher_public_key=batcher_public_key,
            )
        self.assertEqual(batch_count, 1)

    def assertValidBatchRequest(
        self, batch_request, payload, signer_public_key, batcher_public_key
    ):
        """Check a batch request is valid given a payload"""
        self.assertIsInstance(
            batch_request, client_batch_submit_pb2.ClientBatchSubmitRequest
        )
        batches = list(batch_request.batches)
        batch_count = 0
        for batch in batches:
            batch_count += 1
            self.assertIsInstance(batch, batch_pb2.Batch)
            self.assertValidBatch(
                batch=batch,
                payload=payload,
                signer_public_key=signer_public_key,
                batcher_public_key=batcher_public_key,
            )
        self.assertEqual(batch_count, 1)

    def assertSingleStatus(self, status):
        """Check a single successful status result"""
        self.assertIsInstance(status, list)
        self.assertEqual(len(status), 1)
        status = status[0]
        self.assertIsInstance(status["invalid_transactions"], list)
        self.assertIsInstance(status["status"], str)
        return status["status"], status["invalid_transactions"]

    def assertStatusSuccess(self, status):
        """Check a status result is successful"""
        state, invalid = self.assertSingleStatus(status)
        self.assertEqual(
            state, "COMMITTED", "Expected COMMITTED, got {}\n{}".format(state, status)
        )
        self.assertEqual(len(invalid), 0)
        return state, invalid

    def assertStatusInvalid(self, status):
        """Check a status result is successful"""
        state, invalid = self.assertSingleStatus(status)
        self.assertEqual(state, "INVALID")
        self.assertEqual(len(invalid), 1)
        return state, invalid
