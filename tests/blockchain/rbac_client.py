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

from base64 import b64decode
from uuid import uuid4
from rbac.common import addresser
from rbac.common.protobuf import user_state_pb2
from rbac.transaction_creation.user_transaction_creation import create_user
from rbac.transaction_creation import (
    task_transaction_creation,
    role_transaction_creation,
    manager_transaction_creation,
)

from rbac.common.sawtooth.rest_client import RestClient

REST_ENDPOINT = "http://rest-api:8008"


class RbacClient(object):
    def __init__(self, url, key):
        if url is None:
            url = REST_ENDPOINT
        self._client = RestClient(base_url=url)
        self._key = key

    def return_state(self):
        items = []
        for item in self._client.list_state(subtree=addresser.NAMESPACE)["data"]:
            if addresser.address_is(item["address"]) == addresser.AddressSpace.USER:
                user_container = user_state_pb2.UserContainer()
                user_container.ParseFromString(b64decode(item["data"]))
                items.append((user_container, addresser.AddressSpace.USER))
        return items

    def create_user(self, key, name, username, user_id, manager_id=None):
        batch_list, signature = create_user(
            txn_key=key,
            batch_key=self._key,
            name=name,
            username=username,
            user_id=user_id,
            metadata=uuid4().hex,
            manager_id=manager_id,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def create_role(self, key, role_name, role_id, metadata, admins, owners):
        batch_list, signature = role_transaction_creation.create_role(
            txn_key=key,
            batch_key=self._key,
            role_name=role_name,
            role_id=role_id,
            metadata=metadata,
            admins=admins,
            owners=owners,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_update_manager(
        self, key, proposal_id, user_id, new_manager_id, reason, metadata
    ):

        batch_list, signature = manager_transaction_creation.propose_manager(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=new_manager_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_update_manager(self, key, proposal_id, reason, user_id, manager_id):
        batch_list, signature = manager_transaction_creation.confirm_manager(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            reason=reason,
            user_id=user_id,
            manager_id=manager_id,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_update_manager(self, key, proposal_id, reason, user_id, manager_id):
        batch_list, signature = manager_transaction_creation.reject_manager(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            reason=reason,
            user_id=user_id,
            manager_id=manager_id,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_admins(
        self, key, proposal_id, role_id, user_id, reason, metadata
    ):
        batch_list, signature = role_transaction_creation.propose_add_role_admins(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_admins(self, key, proposal_id, role_id, user_id, reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_admins(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
        )

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_admins(self, key, proposal_id, role_id, user_id, reason):

        batch_list, signature = role_transaction_creation.reject_add_role_admins(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_owners(
        self, key, proposal_id, role_id, user_id, reason, metadata
    ):
        batch_list, signature = role_transaction_creation.propose_add_role_owners(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_owners(self, key, proposal_id, role_id, user_id, reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_owners(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_owners(self, key, proposal_id, role_id, user_id, reason):
        batch_list, signature = role_transaction_creation.reject_add_role_owners(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_members(
        self, key, proposal_id, role_id, user_id, reason, metadata
    ):
        batch_list, signature = role_transaction_creation.propose_add_role_members(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_members(self, key, proposal_id, role_id, user_id, reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_members(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_members(self, key, proposal_id, role_id, user_id, reason):
        batch_list, signature = role_transaction_creation.reject_add_role_members(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_role_tasks(
        self, key, proposal_id, role_id, task_id, reason, metadata
    ):
        batch_list, signature = role_transaction_creation.propose_add_role_tasks(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            task_id=task_id,
            reason=reason,
            metadata=metadata,
        )

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_role_tasks(self, key, proposal_id, role_id, task_id, reason):
        batch_list, signature = role_transaction_creation.confirm_add_role_tasks(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            task_id=task_id,
            reason=reason,
        )

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_role_tasks(self, key, proposal_id, role_id, task_id, reason):
        batch_list, signature = role_transaction_creation.reject_add_role_tasks(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            role_id=role_id,
            task_id=task_id,
            reason=reason,
        )

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def create_task(self, key, task_id, task_name, admins, owners, metadata):

        batch_list, signature = task_transaction_creation.create_task(
            txn_key=key,
            batch_key=self._key,
            task_id=task_id,
            task_name=task_name,
            admins=admins,
            owners=owners,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_task_admins(
        self, key, proposal_id, task_id, user_id, reason, metadata
    ):
        batch_list, signature = task_transaction_creation.propose_add_task_admins(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_task_admins(self, key, proposal_id, task_id, user_id, reason):
        batch_list, signature = task_transaction_creation.confirm_add_task_admins(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_task_admins(self, key, proposal_id, task_id, user_id, reason):
        batch_list, signature = task_transaction_creation.reject_add_task_admins(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_add_task_owners(
        self, key, proposal_id, task_id, user_id, reason, metadata
    ):
        batch_list, signature = task_transaction_creation.propose_add_task_owner(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def confirm_add_task_owners(self, key, proposal_id, task_id, user_id, reason):
        batch_list, signature = task_transaction_creation.confirm_add_task_owners(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def reject_add_task_owners(self, key, proposal_id, task_id, user_id, reason):
        batch_list, signature = task_transaction_creation.reject_add_task_owners(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_delete_task_admins(
        self, key, proposal_id, task_id, user_id, reason, metadata
    ):
        batch_list, signature = task_transaction_creation.propose_remove_task_admins(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)

    def propose_delete_task_owners(
        self, key, proposal_id, task_id, user_id, reason, metadata
    ):

        batch_list, signature = task_transaction_creation.propose_remove_task_owners(
            txn_key=key,
            batch_key=self._key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)
