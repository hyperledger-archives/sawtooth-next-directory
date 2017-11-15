# Copyright 2017 Intel Corporation
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

from rbac_addressing import addresser

from rbac_transaction_creation.common import make_header_and_batch

from rbac_transaction_creation.protobuf import rbac_payload_pb2
from rbac_transaction_creation.protobuf import task_transaction_pb2


def create_task(txn_key,
                batch_key,
                task_id,
                task_name,
                admins,
                owners,
                metadata):

    create_payload = task_transaction_pb2.CreateTask(
        task_id=task_id,
        name=task_name)

    create_payload.admins.extend(admins)

    inputs = [addresser.make_task_attributes_address(task_id=task_id),
              addresser.make_sysadmin_members_address(txn_key.public_key)]

    inputs.extend([addresser.make_user_address(user_id=u) for u in admins])
    inputs.extend([addresser.make_task_admins_address(task_id, u)
                   for u in admins])

    outputs = [addresser.make_task_attributes_address(task_id=task_id)]

    outputs.extend([addresser.make_task_admins_address(task_id, u)
                    for u in admins])

    if owners:
        create_payload.owners.extend(owners)
        inputs.extend([addresser.make_user_address(user_id=u)
                       for u in owners])
        inputs.extend([addresser.make_task_owners_address(task_id, u)
                       for u in owners])
        outputs.extend([addresser.make_task_owners_address(task_id, u)
                        for u in owners])

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=create_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CREATE_TASK)

    return make_header_and_batch(
        rbac_payload,
        inputs,
        outputs,
        txn_key,
        batch_key)
