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

from rbac.common.sawtooth.client_sync import ClientSync
from rbac.common.crypto.keys import Key
from rbac.common.sawtooth.batcher import Batcher
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload


class BaseManager:
    def __init__(self):
        """Objects and methods shared across *_manager libraries"""
        self.batch = Batcher()
        self.client = ClientSync()

    def send(self, signer_keypair, object_id, payload, do_send=True, do_get=False):
        """Sends a payload to the transaction processor"""
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")
        if not isinstance(payload, RBACPayload):
            raise TypeError("Expected payload to be an RBACPayload")

        transaction, batch, batch_list, batch_request = self.batch.make(
            payload=payload, signer_keypair=signer_keypair
        )

        if not do_send:
            return None, None, transaction, batch, batch_list, batch_request

        status = self.client.send_batches_get_status(batch_list=batch_list)
        if not do_get:
            return None, status, transaction, batch, batch_list, batch_request

        got = self.get(object_id=object_id)
        return got, status, transaction, batch, batch_list, batch_request
