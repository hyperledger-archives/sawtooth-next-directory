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

from rbac_processor.common import validate_role_task_proposal
from rbac_processor.role.common import validate_role_task
from rbac_processor.role.common import handle_confirm_add
from rbac_processor.role.common import handle_reject
from rbac_processor.role.common import handle_propose_state_set


from rbac_processor.protobuf import proposal_state_pb2
from rbac_processor.protobuf import role_transaction_pb2


def apply_propose(header, payload, state):
    propose = role_transaction_pb2.ProposeAddRoleTask()
    propose.ParseFromString(payload.content)

    state_entries = validate_role_task_proposal(header, propose, state)

    proposal_address = addresser.make_proposal_address(
        propose.role_id,
        propose.task_id)

    handle_propose_state_set(
        state_entries=state_entries,
        header=header,
        payload=propose,
        address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.ADD_ROLE_TASKS,
        state=state,
        related_type='task_id')


def apply_propose_remove(header, payload, state):
    propose = role_transaction_pb2.ProposeRemoveRoleTask()
    propose.ParseFromString(payload.content)

    state_entries = validate_role_task_proposal(header, propose, state)

    proposal_address = addresser.make_proposal_address(
        propose.role_id,
        propose.task_id)

    handle_propose_state_set(
        state_entries=state_entries,
        header=header,
        payload=propose,
        address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.REMOVE_ROLE_TASKS,
        state=state,
        related_type='task_id')


def apply_confirm(header, payload, state):
    confirm = role_transaction_pb2.ConfirmAddRoleTask()
    confirm.ParseFromString(payload.content)

    txn_signer_task_owner_address = addresser.make_task_owners_address(
        confirm.task_id,
        header.signer_public_key)

    role_rel_address = addresser.make_role_tasks_address(
        role_id=confirm.role_id,
        task_id=confirm.task_id)

    state_entries = validate_role_task(
        header,
        confirm,
        txn_signer_rel_address=txn_signer_task_owner_address,
        state=state)

    handle_confirm_add(
        state_entries=state_entries,
        header=header,
        confirm=confirm,
        role_rel_address=role_rel_address,
        state=state,
        rel_type='task_id')


def apply_reject(header, payload, state):
    reject = role_transaction_pb2.RejectAddRoleTask()
    reject.ParseFromString(payload.content)

    txn_signer_task_owner_address = addresser.make_task_owners_address(
        reject.task_id,
        header.signer_public_key)

    state_entries = validate_role_task(
        header,
        reject,
        txn_signer_rel_address=txn_signer_task_owner_address,
        state=state)

    handle_reject(
        state_entries=state_entries,
        header=header,
        reject=reject,
        state=state,
        rel_type='task_id')
