# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Test suite for the sawtooth REST client."""

from uuid import uuid4
from rbac.common.user import User
from rbac.common.role import Role
from rbac.common.task import Task
from rbac.common.sawtooth import batcher

from rbac.common.sawtooth.rest_client import RestClient

REST_ENDPOINT = "http://rest-api:8008"


class RbacClient(object):
    """RBAC Client test class."""

    def __init__(self, url, key):
        if url is None:
            url = REST_ENDPOINT
        self._client = RestClient(base_url=url)
        self._key = key

    def create_user(self, key, name, username, next_id, manager_id=None):
        """Create a new user."""
        batch_list = User().batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            name=name,
            username=username,
            next_id=next_id,
            metadata=uuid4().hex,
            manager_id=manager_id,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def create_role(self, key, role_name, role_id, metadata, admins, owners):
        """Create a new role."""
        batch_list = Role().batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
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
        self, key, proposal_id, next_id, new_manager_id, reason, metadata
    ):
        """Propose an update of user's manager."""
        batch_list = User().manager.propose.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            next_id=next_id,
            new_manager_id=new_manager_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_update_manager(self, key, proposal_id, reason, next_id, manager_id):
        """Confirm the update of a user's manager."""
        batch_list = User().manager.confirm.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            reason=reason,
            object_id=next_id,
            related_id=manager_id,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_update_manager(self, key, proposal_id, reason, next_id, manager_id):
        """Reject the update of a user's manager."""
        batch_list = User().manager.reject.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            reason=reason,
            object_id=next_id,
            related_id=manager_id,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_admins(
        self, key, proposal_id, role_id, next_id, reason, metadata
    ):
        """Propose adding admin to role."""
        batch_list = Role().admin.propose.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            role_id=role_id,
            next_id=next_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_role_admins(self, key, proposal_id, role_id, next_id, reason):
        """Confirm addition of admin to role."""
        batch_list = Role().admin.confirm.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_admins(self, key, proposal_id, role_id, next_id, reason):
        """Reject addition of admin to role."""
        batch_list = Role().admin.reject.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_owners(
        self, key, proposal_id, role_id, next_id, reason, metadata
    ):
        """Propose adding owner to role."""
        batch_list = Role().owner.propose.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            role_id=role_id,
            next_id=next_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_role_owners(self, key, proposal_id, role_id, next_id, reason):
        """Confirm addition of owner to role."""
        batch_list = Role().owner.confirm.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_owners(self, key, proposal_id, role_id, next_id, reason):
        """Reject addition of role owner."""
        batch_list = Role().owner.reject.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_members(
        self, key, proposal_id, role_id, next_id, reason, metadata
    ):
        """Propose adding role member."""
        batch_list = Role().member.propose.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            role_id=role_id,
            next_id=next_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_role_members(self, key, proposal_id, role_id, next_id, reason):
        """Confirm addition of role member."""
        batch_list = Role().member.confirm.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_members(self, key, proposal_id, role_id, next_id, reason):
        """Reject addition of role member."""
        batch_list = Role().member.reject.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_role_tasks(
        self, key, proposal_id, role_id, task_id, reason, metadata
    ):
        """Propose adding task to role."""
        batch_list = Role().task.propose.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
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
        """Confirm addition of task to role."""
        batch_list = Role().task.confirm.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=task_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_role_tasks(self, key, proposal_id, role_id, task_id, reason):
        """Reject addition of task to role."""
        batch_list = Role().task.reject.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=role_id,
            related_id=task_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def create_task(self, key, task_id, task_name, admins, owners, metadata):
        """Create a new task."""
        batch_list = Task().batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
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
        self, key, proposal_id, task_id, next_id, reason, metadata
    ):
        """Propose adding a task admin."""
        batch_list = Task().admin.propose.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            task_id=task_id,
            next_id=next_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_task_admins(self, key, proposal_id, task_id, next_id, reason):
        """Confirm addition of task admin."""
        batch_list = Task().admin.confirm.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_task_admins(self, key, proposal_id, task_id, next_id, reason):
        """Reject addition of task admin."""
        batch_list = Task().admin.reject.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def propose_add_task_owners(
        self, key, proposal_id, task_id, next_id, reason, metadata
    ):
        """Propose adding a task owner."""
        batch_list = Task().owner.propose.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            task_id=task_id,
            next_id=next_id,
            reason=reason,
            metadata=metadata,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def confirm_add_task_owners(self, key, proposal_id, task_id, next_id, reason):
        """Confirm addition of task owner."""
        batch_list = Task().owner.confirm.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)

    def reject_add_task_owners(self, key, proposal_id, task_id, next_id, reason):
        """Reject addition of task owner."""
        batch_list = Task().owner.reject.batch_list(
            signer_keypair=key,
            signer_user_id=key.public_key,
            proposal_id=proposal_id,
            object_id=task_id,
            related_id=next_id,
            reason=reason,
        )
        batch_ids = batcher.get_batch_ids(batch_list=batch_list)
        self._client.send_batches(batch_list)
        return self._client.get_statuses(batch_ids, wait=10)
