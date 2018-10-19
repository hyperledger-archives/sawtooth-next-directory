# Copyright contributors to Hyperledger Sawtooth
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
from rbac.addressing import addresser
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import role_transaction_pb2
from rbac.common.protobuf import role_state_pb2
from rbac.common.sawtooth.client_sync import ClientSync
from rbac.common.sawtooth.batcher import Batcher

LOGGER = logging.getLogger(__name__)


class RoleManager:
    def __init__(self):
        self.batch = Batcher()
        self.client = ClientSync()

    def make(self, role_id, name, metadata=None, admins=None, owners=None):
        return role_transaction_pb2.CreateRole(
            role_id=role_id, name=name, metadata=metadata, admins=admins, owners=owners
        )

    def create(self, signer_keypair, role, do_batch=True, do_send=True, do_get=False):
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")
        if not isinstance(role, role_transaction_pb2.CreateRole):
            raise TypeError(
                "Expected role to be a role_transaction_pb2.CreateRole, use make first"
            )

        inputs = [
            addresser.make_sysadmin_members_address(signer_keypair.public_key),
            addresser.make_role_attributes_address(role.role_id),
        ]
        inputs.extend([addresser.make_user_address(u) for u in role.admins])
        inputs.extend([addresser.make_user_address(u) for u in role.owners])
        inputs.extend(
            [
                addresser.make_role_admins_address(role_id=role.role_id, user_id=a)
                for a in role.admins
            ]
        )
        inputs.extend(
            [
                addresser.make_role_owners_address(role_id=role.role_id, user_id=o)
                for o in role.owners
            ]
        )

        transaction = self.batch.make_transaction(
            message=role,
            message_type=RBACPayload.CREATE_ROLE,
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

        return self.get(role_id=role.role_id)

    def get(self, role_id):
        container = role_state_pb2.RoleAttributesContainer()
        address = addresser.make_role_attributes_address(role_id=role_id)
        container.ParseFromString(self.client.get_address(address=address))
        items = list(container.role_attributes)
        if len(items) == 0:
            return None
        elif len(items) > 1:
            LOGGER.warning(
                "role container for %s at address %s has more than one role record",
                role_id,
                address,
            )
        return items[0]

    def check_owner(self, role_id, user_id):
        container = role_state_pb2.RoleRelationshipContainer()
        address = addresser.make_role_owners_address(role_id=role_id, user_id=user_id)
        container.ParseFromString(self.client.get_address(address=address))
        items = list(container.relationships)
        if len(items) == 0:
            return False
        elif len(items) > 1:
            LOGGER.warning(
                "role %s owners container for user %s at address %s has more than one record",
                role_id,
                user_id,
                address,
            )
        item = items[0]
        identifiers = list(item.identifiers)
        if len(identifiers) == 0:
            LOGGER.warning(
                "role %s owners container for user %s at address %s has no identifiers",
                role_id,
                user_id,
                address,
            )
            return False
        if len(identifiers) > 1:
            LOGGER.warning(
                "role %s owners container for user %s at address %s has more than one identifier",
                role_id,
                user_id,
                address,
            )
        return bool(user_id in item.identifiers)

    def check_admin(self, role_id, user_id):
        container = role_state_pb2.RoleRelationshipContainer()
        address = addresser.make_role_admins_address(role_id=role_id, user_id=user_id)
        container.ParseFromString(self.client.get_address(address=address))
        items = list(container.relationships)
        if len(items) == 0:
            return False
        elif len(items) > 1:
            LOGGER.warning(
                "role %s admins container for user %s at address %s has more than one record",
                role_id,
                user_id,
                address,
            )
        item = items[0]
        identifiers = list(item.identifiers)
        if len(identifiers) == 0:
            LOGGER.warning(
                "role %s admins container for user %s at address %s has no identifiers",
                role_id,
                user_id,
                address,
            )
            return False
        if len(identifiers) > 1:
            LOGGER.warning(
                "role %s admins container for user %s at address %s has more than one identifier",
                role_id,
                user_id,
                address,
            )
        return bool(user_id in item.identifiers)
