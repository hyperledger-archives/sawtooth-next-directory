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
from uuid import uuid4
from sawtooth_rest_api.protobuf import batch_pb2
from sawtooth_rest_api.protobuf import client_batch_submit_pb2
from sawtooth_rest_api.protobuf import transaction_pb2
from rbac.addressing import addresser
from rbac.common.protobuf import rbac_payload_pb2
from rbac.app.config import BATCHER_KEY_PAIR

LOGGER = logging.getLogger(__name__)


class Batcher:
    @classmethod
    def make_payload(self, message, message_type):
        return rbac_payload_pb2.RBACPayload(
            content=message.SerializeToString(), message_type=message_type
        )

    @classmethod
    def make_transaction_header(
        self,
        payload,
        inputs,
        outputs,
        signer_keypair,
        batcher_public_key=BATCHER_KEY_PAIR.public_key,
    ):

        header = transaction_pb2.TransactionHeader(
            inputs=inputs,
            outputs=outputs,
            batcher_public_key=batcher_public_key,
            dependencies=[],
            family_name=addresser.FAMILY_NAME,
            family_version=addresser.FAMILY_VERSION,
            nonce=uuid4().hex,
            signer_public_key=signer_keypair.public_key,
            payload_sha512=sha512(payload.SerializeToString()).hexdigest(),
        )

        signature = signer_keypair.sign(header.SerializeToString())
        return header, signature

    @classmethod
    def make_transaction(
        self,
        message,
        message_type,
        inputs,
        outputs,
        signer_keypair,
        batcher_public_key=BATCHER_KEY_PAIR.public_key,
    ):

        payload = self.make_payload(message=message, message_type=message_type)

        header, signature = self.make_transaction_header(
            payload=payload,
            inputs=inputs,
            outputs=outputs,
            signer_keypair=signer_keypair,
            batcher_public_key=batcher_public_key,
        )

        return transaction_pb2.Transaction(
            payload=payload.SerializeToString(),
            header=header.SerializeToString(),
            header_signature=signature,
        )

    @classmethod
    def make_batch(self, transaction, batcher_keypair=BATCHER_KEY_PAIR):

        batch_header = batch_pb2.BatchHeader(
            signer_public_key=batcher_keypair.public_key,
            transaction_ids=[transaction.header_signature],
        ).SerializeToString()

        return batch_pb2.Batch(
            header=batch_header,
            header_signature=batcher_keypair.sign(batch_header),
            transactions=[transaction],
        )

    @classmethod
    def batch_to_list(self, batch):
        return batch_pb2.BatchList(batches=[batch])

    @classmethod
    def make_batch_list(self, transaction):
        return self.batch_to_list(self.make_batch(transaction=transaction))

    @classmethod
    def make_batch_request(self, batch_list):
        batch_request = client_batch_submit_pb2.ClientBatchSubmitRequest()
        batch_request.batches.extend(list(batch_list.batches))
        return batch_request

    @classmethod
    def get_batch_ids(self, batch_list):
        return list(batch.header_signature for batch in batch_list.batches)
