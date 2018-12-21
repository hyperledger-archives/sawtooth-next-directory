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

from uuid import uuid4
from rbac.common import rbac
from rbac.common.sawtooth import batcher

from rbac.common.sawtooth.rest_client import RestClient

REST_ENDPOINT = "http://rest-api:8008"


class RbacClient(object):
    def __init__(self, url, key):
        if url is None:
            url = REST_ENDPOINT
        self._client = RestClient(base_url=url)
        self._key = key

    def create_user(self, key, name, username, user_id, manager_id=None):
        batch_list = rbac.user.batch_list(
            signer_keypair=key,
            name=name,
            username=username,
            user_id=user_id,
            metadata=uuid4().hex,
            manager_id=manager_id,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def create_role(self, key, role_name, role_id, metadata, admins, owners):
        batch_list = rbac.role.batch_list(
            signer_keypair=key,
            name=role_name,
            role_id=role_id,
            metadata=metadata,
            admins=admins,
            owners=owners,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_update_manager(
        self, key, proposal_id, user_id, new_manager_id, reason, metadata
    ):

        batch_list = rbac.user.manager.propose.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=new_manager_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_update_manager(self, key, proposal_id, reason, user_id, manager_id):
        batch_list = rbac.user.manager.confirm.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            reason=reason,
            object_id=user_id,
            related_id=manager_id,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_update_manager(self, key, proposal_id, reason, user_id, manager_id):
        batch_list = rbac.user.manager.reject.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            reason=reason,
            object_id=user_id,
            related_id=manager_id,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_admins(
        self, key, proposal_id, role_id, user_id, reason, metadata
    ):
        batch_list = rbac.role.admin.propose.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_role_admins(self, key, proposal_id, role_id, user_id, reason):
        batch_list = rbac.role.admin.confirm.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_admins(self, key, proposal_id, role_id, user_id, reason):

        batch_list = rbac.role.admin.reject.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_owners(
        self, key, proposal_id, role_id, user_id, reason, metadata
    ):
        batch_list = rbac.role.owner.propose.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_role_owners(self, key, proposal_id, role_id, user_id, reason):
        batch_list = rbac.role.owner.confirm.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_owners(self, key, proposal_id, role_id, user_id, reason):
        batch_list = rbac.role.owner.reject.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_members(
        self, key, proposal_id, role_id, user_id, reason, metadata
    ):
        batch_list = rbac.role.member.propose.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_role_members(self, key, proposal_id, role_id, user_id, reason):
        batch_list = rbac.role.member.confirm.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_members(self, key, proposal_id, role_id, user_id, reason):
        batch_list = rbac.role.member.reject.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_tasks(
        self, key, proposal_id, role_id, task_id, reason, metadata
    ):
        batch_list = rbac.role.task.propose.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            role_id=role_id,
            task_id=task_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_role_tasks(self, key, proposal_id, role_id, task_id, reason):
        batch_list = rbac.role.task.confirm.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=task_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_tasks(self, key, proposal_id, role_id, task_id, reason):
        batch_list = rbac.role.task.reject.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=task_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def create_task(self, key, task_id, task_name, admins, owners, metadata):

        batch_list = rbac.task.batch_list(
            signer_keypair=key,
            task_id=task_id,
            name=task_name,
            admins=admins,
            owners=owners,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_task_admins(
        self, key, proposal_id, task_id, user_id, reason, metadata
    ):
        batch_list = rbac.task.admin.propose.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_task_admins(self, key, proposal_id, task_id, user_id, reason):
        batch_list = rbac.task.admin.confirm.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_task_admins(self, key, proposal_id, task_id, user_id, reason):
        batch_list = rbac.task.admin.reject.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_task_owners(
        self, key, proposal_id, task_id, user_id, reason, metadata
    ):
        batch_list = rbac.task.owner.propose.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_task_owners(self, key, proposal_id, task_id, user_id, reason):
        batch_list = rbac.task.owner.confirm.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_task_owners(self, key, proposal_id, task_id, user_id, reason):
        batch_list = rbac.task.owner.reject.batch_list(
            signer_keypair=key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=user_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)
