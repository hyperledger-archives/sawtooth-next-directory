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
from hashlib import sha512

from tests.rbac.common.assertions import CommonAssertions

from sawtooth_rest_api.protobuf import transaction_pb2
from sawtooth_rest_api.protobuf import batch_pb2
from sawtooth_rest_api.protobuf import client_batch_submit_pb2

from rbac.common.crypto.keys import Key
from rbac.addressing import addresser
from rbac.addressing.addresser import AddressSpace
from rbac.transaction_creation.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.transaction_creation.protobuf import user_transaction_pb2

LOGGER = logging.getLogger(__name__)


class BatchAssertions(CommonAssertions):
    def __init__(self, *args, **kwargs):
        CommonAssertions.__init__(self, *args, **kwargs)

    def assertValidPayload(self, payload, message, message_type):
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
                "assertValidPayload doesn't yet support {}".format(message_type)
            )

    def assertValidInputs(self, inputs, outputs, message_type, message=None):
        if inputs is not None and not isinstance(inputs, list):
            inputs = list(inputs)
        if outputs is not None and not isinstance(outputs, list):
            outputs = list(outputs)

        if message_type == RBACPayload.CREATE_USER:
            self.assertIsInstance(inputs, list)
            self.assertIsInstance(outputs, list)
            self.assertEqual(len(inputs), 1)
            self.assertEqual(len(outputs), 1)
            self.assertEqual(addresser.address_is(inputs[0]), AddressSpace.USER)
            self.assertEqual(addresser.address_is(outputs[0]), AddressSpace.USER)
        else:
            raise Exception(
                "assertValidInputs doesn't yet support {}".format(message_type)
            )

    def assertValidTransactionHeader(
        self,
        header,
        signature,
        message,
        message_type,
        inputs,
        outputs,
        signer_public_key,
    ):
        if isinstance(header, bytes):
            decoded = transaction_pb2.TransactionHeader()
            decoded.ParseFromString(header)
            header = decoded

        payload = self.make_payload(message=message, message_type=message_type)

        self.assertIsInstance(header, transaction_pb2.TransactionHeader)
        self.assertEqual(header.family_name, addresser.FAMILY_NAME)
        self.assertEqual(header.family_version, addresser.FAMILY_VERSION)
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

        self.assertEqual(header.inputs, inputs)
        self.assertEqual(header.outputs, outputs)
        self.assertValidInputs(
            inputs=header.inputs,
            outputs=header.outputs,
            message_type=message_type,
            message=message,
        )

    def assertValidTransaction(
        self, transaction, message, message_type, inputs, outputs, signer_public_key
    ):
        if isinstance(transaction, bytes):
            decoded = transaction_pb2.Transaction()
            decoded.ParseFromString(transaction)
            transaction = decoded
        self.assertIsInstance(transaction, transaction_pb2.Transaction)

        self.assertValidTransactionHeader(
            header=transaction.header,
            signature=transaction.header_signature,
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer_public_key,
        )

    def assertValidBatch(
        self,
        batch,
        message,
        message_type,
        inputs,
        outputs,
        signer_public_key,
        batcher_public_key,
    ):
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
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer_public_key,
        )

    def assertValidBatchList(
        self,
        batch_list,
        message,
        message_type,
        inputs,
        outputs,
        signer_public_key,
        batcher_public_key,
    ):
        self.assertIsInstance(batch_list, batch_pb2.BatchList)
        # batch_list = list(batch_list)
        batch_count = 0
        for batch in batch_list.batches:
            batch_count += 1
            self.assertIsInstance(batch, batch_pb2.Batch)
            self.assertValidBatch(
                batch=batch,
                message=message,
                message_type=message_type,
                inputs=inputs,
                outputs=outputs,
                signer_public_key=signer_public_key,
                batcher_public_key=batcher_public_key,
            )
        self.assertEqual(batch_count, 1)

    def assertValidBatchRequest(
        self,
        batch_request,
        message,
        message_type,
        inputs,
        outputs,
        signer_public_key,
        batcher_public_key,
    ):
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
                message=message,
                message_type=message_type,
                inputs=inputs,
                outputs=outputs,
                signer_public_key=signer_public_key,
                batcher_public_key=batcher_public_key,
            )
        self.assertEqual(batch_count, 1)
        return
