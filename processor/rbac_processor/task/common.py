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

from sawtooth_sdk.protobuf import state_context_pb2
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac_addressing import addresser

from rbac_processor.common import get_state_entry
from rbac_processor.common import get_prop_from_container
from rbac_processor.common import get_task_rel_from_container
from rbac_processor.common import get_user_from_container
from rbac_processor.common import is_in_task_rel_container
from rbac_processor.common import proposal_exists_and_open
from rbac_processor.common import return_task_rel_container
from rbac_processor.common import return_prop_container
from rbac_processor.common import return_user_container
from rbac_processor.common import validate_identifier_is_user
from rbac_processor.common import validate_identifier_is_task

from rbac_processor.protobuf import proposal_state_pb2
from rbac_processor.protobuf import task_state_pb2

from rbac_processor.state import get_state
from rbac_processor.state import set_state


def validate_task_rel_proposal(header, propose, rel_address, state):
    """Validates that the User exists, the Task exists, and the User is not
    in the Task's relationship specified by rel_address.

    Args:
        header (TransactionHeader): The transaction header.
        propose (ProposeAddTask_____): The Task relationship proposal.
        rel_address (str): The Task relationship address produced by the Task
            and the User.
        state (sawtooth_sdk.Context): The way to communicate to the validator
            the state gets and sets.

    Returns:
        (dict of addresses)
    """

    user_address = addresser.make_user_address(propose.user_id)
    task_address = addresser.make_task_attributes_address(propose.task_id)
    proposal_address = addresser.make_proposal_address(
        object_id=propose.task_id,
        related_id=propose.user_id)

    state_entries = get_state(state, [user_address,
                                      task_address,
                                      proposal_address,
                                      rel_address])
    validate_identifier_is_user(state_entries,
                                identifier=propose.user_id,
                                address=user_address)
    user_entry = get_state_entry(state_entries, user_address)
    user = get_user_from_container(
        return_user_container(user_entry),
        propose.user_id)

    if header.signer_public_key not in [user.user_id, user.manager_id]:
        raise InvalidTransaction(
            "Txn signer {} is not the user or the user's "
            "manager {}".format(header.signer_public_key,
                                [user.user_id, user.manager_id]))

    validate_identifier_is_task(state_entries,
                                identifier=propose.task_id,
                                address=task_address)

    try:
        task_admins_entry = get_state_entry(state_entries, rel_address)
        task_rel_container = return_task_rel_container(task_admins_entry)
        if is_in_task_rel_container(
                task_rel_container,
                propose.task_id,
                propose.user_id):
            raise InvalidTransaction(
                "User {} is already in the Role {} "
                "relationship".format(propose.user_id,
                                      propose.task_id))
    except KeyError:
        # The task rel container doesn't exist so no task relationship exists
        pass

    return state_entries


def validate_task_rel_del_proposal(header, propose, rel_address, state):
    """Validates that the User exists, the Task exists, and the User is in
    the Tasks's relationship specified by the rel_address.

    Args:
        header (TransactionHeader): The transaction header.
        propose (ProposeRemoveTask____): The Task Remove relationship proposal
        rel_address (str): The task relationship address.
        state (Context:: The way to communicate to the validator State gets
            and sets.

    Returns:
        (dict of addresses)
    """

    user_address = addresser.make_user_address(propose.user_id)
    task_address = addresser.make_task_attributes_address(propose.task_id)

    proposal_address = addresser.make_proposal_address(
        object_id=propose.task_id,
        related_id=propose.user_id)

    state_entries = get_state(state,
                              [user_address,
                               task_address,
                               proposal_address,
                               rel_address])

    validate_identifier_is_user(
        state_entries,
        identifier=propose.user_id,
        address=user_address)

    user_entry = get_state_entry(state_entries, user_address)

    user = get_user_from_container(
        return_user_container(user_entry),
        propose.user_id)

    if header.signer_public_key not in [user.user_id, user.manager_id]:
        raise InvalidTransaction(
            "Txn signer {} is not the user {} or the user's manager {}".format(
                header.signer_public_key,
                user.user_id,
                user.manager_id))

    validate_identifier_is_task(state_entries,
                                identifier=propose.task_id,
                                address=task_address)

    try:
        task_rel_entry = get_state_entry(state_entries, rel_address)
        task_rel_container = return_task_rel_container(task_rel_entry)
        if not is_in_task_rel_container(
                task_rel_container,
                propose.task_id,
                propose.user_id):
            raise InvalidTransaction("User {} isn't in the Task {} "
                                     "relationship".format(propose.user_id,
                                                           propose.task_id))
    except KeyError:
        raise InvalidTransaction(
            "User {} isn't in the Task {} relationship, "
            "since there isn't a container at the address".format(
                propose.user_id,
                propose.task_id))

    return state_entries


def validate_task_admin_or_owner(header,
                                 confirm,
                                 txn_signer_rel_address,
                                 state):
    """Validate a [ Confirm | Reject }_____Task[ Admin | Owner } transaction.

    Args:
        header (TransactionHeader): The transaction header protobuf class.:
        confirm: ConfirmAddTaskAdmin, RejectAddTaskAdmin, ...
        state (Context): The class responsible for gets and sets of state.

    Returns:
        (dict of addresses)
    """

    proposal_address = addresser.make_proposal_address(
        object_id=confirm.task_id,
        related_id=confirm.user_id)

    state_entries = get_state(
        state,
        [txn_signer_rel_address, proposal_address])

    if not proposal_exists_and_open(
            state_entries,
            proposal_address,
            confirm.proposal_id):
        raise InvalidTransaction("The proposal {} does not exist or "
                                 "is not open".format(confirm.proposal_id))
    try:
        entry = get_state_entry(state_entries, txn_signer_rel_address)
        task_rel_container = return_task_rel_container(entry)
    except KeyError:
        raise InvalidTransaction(
            "Signer {} does not have the Task permissions "
            "to close the proposal".format(header.signer_public_key))
    if not is_in_task_rel_container(
            task_rel_container,
            task_id=confirm.task_id,
            identifier=header.signer_public_key):
        raise InvalidTransaction("Signer {} does not have the Task "
                                 "permissions to close the "
                                 "proposal".format(header.signer_public_key))

    return state_entries


def handle_propose_state_set(state_entries,
                             header,
                             payload,
                             address,
                             proposal_type,
                             state,
                             related_type='user_id'):

    try:

        entry = get_state_entry(state_entries, address=address)
        proposal_container = return_prop_container(entry)
    except KeyError:
        proposal_container = proposal_state_pb2.ProposalsContainer()

    proposal = proposal_container.proposals.add()

    proposal.proposal_id = payload.proposal_id
    proposal.object_id = payload.task_id
    proposal.target_id = getattr(payload, related_type)
    proposal.proposal_type = proposal_type
    proposal.status = proposal_state_pb2.Proposal.OPEN
    proposal.opener = header.signer_public_key
    proposal.open_reason = payload.reason
    proposal.metadata = payload.metadata

    set_state(state, {
        address: proposal_container.SerializeToString()
    })


def handle_confirm_add(state_entries,
                       header,
                       confirm,
                       task_rel_address,
                       state):
    proposal_address = addresser.make_proposal_address(
        object_id=confirm.task_id,
        related_id=confirm.user_id)

    proposal_entry = get_state_entry(state_entries, proposal_address)
    proposal_container = return_prop_container(proposal_entry)
    proposal = get_prop_from_container(
        proposal_container,
        proposal_id=confirm.proposal_id)

    proposal.status = proposal_state_pb2.Proposal.CONFIRMED
    proposal.closer = header.signer_public_key
    proposal.close_reason = confirm.reason

    address_values = {
        proposal_address: proposal_container.SerializeToString()
    }

    try:
        task_rel_entry = get_state_entry(state_entries, task_rel_address)
        task_rel_container = return_task_rel_container(task_rel_entry)
    except KeyError:
        task_rel_container = task_state_pb2.TaskRelationshipContainer()

    try:
        task_rel = get_task_rel_from_container(
            container=task_rel_container,
            task_id=confirm.task_id,
            identifier=confirm.user_id)
    except KeyError:
        task_rel = task_rel_container.relationships.add()
        task_rel.task_id = confirm.task_id

    task_rel.identifiers.append(confirm.user_id)

    address_values[task_rel_address] = task_rel_container.SerializeToString()

    set_state(state, address_values)


def handle_reject(state_entries,
                  header,
                  reject,
                  state):
    proposal_address = addresser.make_proposal_address(
        object_id=reject.task_id,
        related_id=reject.user_id)

    proposal_entry = get_state_entry(state_entries, proposal_address)
    proposal_container = return_prop_container(proposal_entry)
    proposal = get_prop_from_container(
        proposal_container,
        proposal_id=reject.proposal_id)

    proposal.status = proposal_state_pb2.Proposal.REJECTED
    proposal.closer = header.signer_public_key
    proposal.close_reason = reject.reason

    address_values = { proposal_address: proposal_container.SerializeToString() }

    set_state(state, address_values)
