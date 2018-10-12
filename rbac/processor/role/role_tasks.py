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

from rbac.addressing import addresser
from rbac.processor import proposal_validator, state_change
from rbac.processor.protobuf import proposal_state_pb2
from rbac.processor.protobuf import role_transaction_pb2
from rbac.processor.role import role_validator


def apply_propose(header, payload, state):
    propose = role_transaction_pb2.ProposeAddRoleTask()
    propose.ParseFromString(payload.content)

    state_entries = proposal_validator.validate_role_task_proposal(
        header, propose, state
    )

    proposal_address = addresser.make_proposal_address(propose.role_id, propose.task_id)

    state_change.propose_role_action(
        state_entries=state_entries,
        header=header,
        payload=propose,
        address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.ADD_ROLE_TASKS,
        state=state,
        related_type="task_id",
    )


def apply_propose_remove(header, payload, state):
    propose = role_transaction_pb2.ProposeRemoveRoleTask()
    propose.ParseFromString(payload.content)

    state_entries = proposal_validator.validate_role_task_proposal(
        header, propose, state
    )

    proposal_address = addresser.make_proposal_address(propose.role_id, propose.task_id)

    state_change.propose_role_action(
        state_entries=state_entries,
        header=header,
        payload=propose,
        address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.REMOVE_ROLE_TASKS,
        state=state,
        related_type="task_id",
    )


def apply_confirm(header, payload, state):
    confirm = role_transaction_pb2.ConfirmAddRoleTask()
    confirm.ParseFromString(payload.content)

    txn_signer_task_owner_address = addresser.make_task_owners_address(
        confirm.task_id, header.signer_public_key
    )

    role_rel_address = addresser.make_role_tasks_address(
        role_id=confirm.role_id, task_id=confirm.task_id
    )

    state_entries = role_validator.validate_role_task(
        header,
        confirm,
        txn_signer_rel_address=txn_signer_task_owner_address,
        state=state,
    )

    state_change.confirm_role_action(
        state_entries=state_entries,
        header=header,
        confirm=confirm,
        role_rel_address=role_rel_address,
        state=state,
        rel_type="task_id",
    )


def apply_reject(header, payload, state):
    reject = role_transaction_pb2.RejectAddRoleTask()
    reject.ParseFromString(payload.content)

    txn_signer_task_owner_address = addresser.make_task_owners_address(
        reject.task_id, header.signer_public_key
    )

    state_entries = role_validator.validate_role_task(
        header,
        reject,
        txn_signer_rel_address=txn_signer_task_owner_address,
        state=state,
    )

    state_change.reject_role_action(
        state_entries=state_entries,
        header=header,
        reject=reject,
        state=state,
        rel_type="task_id",
    )


def apply_confirm_remove(header, payload, state):
    raise RuntimeError(
        "apply_confirm_remove not implemented! Args: {0},{1},{2}".format(
            header, payload, state
        )
    )


def apply_reject_remove(header, payload, state):
    raise RuntimeError(
        "apply_reject_remove not implemented! Args: {0},{1},{2}".format(
            header, payload, state
        )
    )
