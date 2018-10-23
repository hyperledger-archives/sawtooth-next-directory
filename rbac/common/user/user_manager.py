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
from rbac.common.crypto.keys import Key
from rbac.addressing.addresser import make_user_address
from rbac.common.sawtooth.client_sync import ClientSync
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import user_transaction_pb2
from rbac.common.protobuf import user_state_pb2
from rbac.common.sawtooth.batcher import Batcher

LOGGER = logging.getLogger(__name__)


class UserManager:
    def __init__(self):
        self.batch = Batcher()
        self.client = ClientSync()

    def make(
        self, user_id, name, user_name=None, email=None, metadata=None, manager_id=None
    ):
        return user_state_pb2.User(
            user_id=user_id,
            name=name,
            # user_name=user_name,
            # email=email,
            metadata=metadata,
            manager_id=manager_id,
        )

    def make_with_key(
        self,
        name,
        user_id=None,
        user_name=None,
        email=None,
        metadata=None,
        manager_id=None,
    ):
        keypair = Key()
        if user_id is None:
            user_id = keypair.public_key
        user = self.make(
            user_id=user_id,
            name=name,
            user_name=user_name,
            email=email,
            metadata=metadata,
            manager_id=manager_id,
        )
        return user, keypair

    def create(self, signer_keypair, user, do_batch=True, do_send=True, do_get=False):
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")
        if not isinstance(user, user_state_pb2.User):
            raise TypeError("Expected user to be a user_state_pb2.User, use make first")

        message = user_transaction_pb2.CreateUser(
            user_id=user.user_id,
            # user_name=user_name,
            name=user.name,
            metadata=user.metadata,
        )
        inputs = [make_user_address(user_id=user.user_id)]

        if user.manager_id:
            message.manager_id = user.manager_id
            inputs.append(make_user_address(user_id=user.manager_id))

        transaction = self.batch.make_transaction(
            message=message,
            message_type=RBACPayload.CREATE_USER,
            inputs=inputs,
            outputs=inputs,
            signer_keypair=signer_keypair,
        )

        if not do_batch:
            return transaction

        batch = self.batch.make_batch(transaction=transaction)
        if not do_send:
            return batch

        batch_list = self.batch.batch_to_list(batch)
        status = self.client.send_batches_get_status(batch_list=batch_list)
        if not do_get:
            return status

        return self.get(user_id=user.user_id)

    def get(self, user_id):
        address = make_user_address(user_id=user_id)
        user_container = user_state_pb2.UserContainer()
        user_container.ParseFromString(self.client.get_address(address=address))
        users = list(user_container.users)
        if len(users) == 0:
            return None
        elif len(users) > 1:
            LOGGER.warning(
                "user container at address %s has more than one record, looking for %s",
                address,
                user_id,
            )
        for user in users:
            if user.user_id == user_id:
                return user
        LOGGER.warning("user %s not found in container address %s", user_id, address)
        return None
