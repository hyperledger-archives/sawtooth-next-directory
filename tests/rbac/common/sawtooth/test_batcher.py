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
import pytest

from rbac.common.crypto.keys import Key
from rbac.app.config import BATCHER_KEY_PAIR
from rbac.addressing.addresser import make_user_address
from rbac.transaction_creation.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.transaction_creation.protobuf import user_transaction_pb2
from rbac.common.sawtooth.batcher import Batcher
from tests.rbac.common.sawtooth.batch_assertions import BatchAssertions


LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.batch
class TestBatchClient(BatchAssertions, Batcher):
    def get_test_inputs(self, message_type=RBACPayload.CREATE_USER):
        if message_type == RBACPayload.CREATE_USER:
            signer = Key()
            message = user_transaction_pb2.CreateUser(name="foobar")
            message.user_id = signer.public_key
            inputs = [make_user_address(signer.public_key)]
            outputs = inputs
            return message, message_type, inputs, outputs, signer
        else:
            raise Exception(
                "get_test_payload doesn't yet support {}".format(message_type)
            )

    def test_get_test_inputs(self):
        self.assertTrue(callable(make_user_address))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        self.assertValidInputs(
            inputs=inputs, outputs=outputs, message_type=message_type, message=message
        )
        self.assertIsInstance(signer, Key)

    def test_make_payload(self):
        self.assertTrue(callable(self.make_payload))
        test_type = RBACPayload.CREATE_USER
        message, message_type, _, _, _ = self.get_test_inputs(test_type)
        payload = self.make_payload(message=message, message_type=message_type)
        self.assertIsInstance(payload, RBACPayload)
        self.assertEqual(message_type, test_type)
        self.assertValidPayload(payload, message, message_type)

    def test_make_transaction_header(self):
        self.assertTrue(callable(self.make_transaction_header))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        header, signature = self.make_transaction_header(
            payload=self.make_payload(message=message, message_type=message_type),
            inputs=inputs,
            outputs=outputs,
            signer_keypair=signer,
        )

        self.assertValidTransactionHeader(
            header=header,
            signature=signature,
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer.public_key,
        )

    def test_make_transaction(self):
        self.assertTrue(callable(self.make_transaction))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        transaction = self.make_transaction(
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_keypair=signer,
        )

        self.assertValidTransaction(
            transaction=transaction,
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer.public_key,
        )

    def test_make_batch(self):
        self.assertTrue(callable(self.make_batch))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        transaction = self.make_transaction(
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_keypair=signer,
        )

        batch = self.make_batch(transaction=transaction)

        self.assertValidBatch(
            batch=batch,
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )

    def test_batch_to_list(self):
        self.assertTrue(callable(self.batch_to_list))
        self.assertTrue(callable(self.make_batch))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        transaction = self.make_transaction(
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_keypair=signer,
        )

        batch = self.make_batch(transaction=transaction)

        batch_list = self.batch_to_list(batch)

        self.assertValidBatchList(
            batch_list=batch_list,
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )

    def test_make_batch_list(self):
        self.assertTrue(callable(self.make_batch_list))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        transaction = self.make_transaction(
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_keypair=signer,
        )

        batch_list = self.make_batch_list(transaction=transaction)

        self.assertValidBatchList(
            batch_list=batch_list,
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )

    def test_make_batch_request(self):
        self.assertTrue(callable(self.make_batch_request))
        message, message_type, inputs, outputs, signer = self.get_test_inputs()

        transaction = self.make_transaction(
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_keypair=signer,
        )

        batch_list = self.make_batch_list(transaction=transaction)

        batch_request = self.make_batch_request(batch_list=batch_list)

        self.assertValidBatchRequest(
            batch_request=batch_request,
            message=message,
            message_type=message_type,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer.public_key,
            batcher_public_key=BATCHER_KEY_PAIR.public_key,
        )
