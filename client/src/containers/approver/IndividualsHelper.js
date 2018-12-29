/* Copyright 2018 Contributors to Hyperledger Sawtooth

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------- */


/**
 * Sync selections
 * @param {boolean} checked     Checkbox state
 * @param {string}  roleId      Role ID
 * @param {string}  proposalId  Proposal ID
 * @param {string}  userId      User ID
 * @generator
 */
export function * syncAll (checked, roleId, proposalId, userId) {
  const sync1 = syncFromCategory.call(this, checked, roleId);
  const sync2 = syncFromItem.call(this, checked, proposalId, userId);

  // Return updated roles / proposals selections
  const { roles, proposals, changedUsers } = roleId ?
    sync1.next().value :
    sync2.next().value;
  yield { roles, proposals };

  const sync3 = syncUsers.call(this, checked, changedUsers, proposals);

  // Return updated user selectinos
  const { users } = sync3.next().value;
  yield { users };
};


/**
 * Update selections on role checkbox selection
 * @param {boolean} checked    Checkbox state
 * @param {string} roleId      Role ID
 * @generator
 */
export function * syncFromCategory (checked, roleId) {
  const { openProposalsByRole} = this.props;
  let { selectedProposals: proposals, selectedRoles: roles } = this.state;
  const changedUsers = [];

  openProposalsByRole[roleId].forEach(proposal => {
    const index = proposals.indexOf(proposal.id);
    changedUsers.push(proposal.opener);
    checked ?
      (proposals = index === -1 ? [...proposals, proposal.id] : proposals) :
      index !== -1 && proposals.splice(index, 1);
  });

  roles = checked ?
    [...roles, roleId] :
    roles.indexOf(roleId) !== -1 ? roles.filter(a => a !== roleId) : roles;

  yield { roles, proposals, changedUsers };
}


/**
 * Update selections on proposal / user checkbox selection
 * @param {boolean} checked     Checkbox state
 * @param {string}  proposalId  Proposal ID
 * @param {string}  userId      User ID
 * @generator
 */
export function * syncFromItem (checked, proposalId, userId) {
  const { openProposalsByUser, openProposalFromId } = this.props;
  let { selectedProposals: proposals, selectedRoles: roles } = this.state;

  const scope = proposalId ? [openProposalFromId(proposalId)] :
    openProposalsByUser[userId];

  scope.forEach(proposal => {
    const indices = [
      roles.indexOf(proposal.object),
      proposals.indexOf(proposal.id),
    ];

    if (checked) {
      // Add to selected roles / proposals
      roles = [...roles, proposal.object];
      proposals = indices[1] === -1 ? [...proposals, proposal.id] : proposals;
    } else {
      indices[0] !== -1 && roles.splice(indices[0], 1);
      indices[1] !== -1 && proposals.splice(indices[1], 1);
    }
  });

  yield { roles, proposals, changedUsers: [userId] };
}


/**
 * Update selected users
 * @param {boolean} checked        Checkbox state
 * @param {array}   changedUsers   Changed users
 * @param {array}   proposals      Array of proposals
 * @generator
 */
export function * syncUsers (checked, changedUsers, proposals) {
  const { openProposalsByUser } = this.props;
  let { selectedUsers: users } = this.state;

  changedUsers.forEach(user => {
    const index = users.indexOf(user);

    if (checked) {
      users = (index === -1) ? [...users, user] : users;
    } else {
      const userProposals = openProposalsByUser[user]
        .filter(proposal => proposals
          .includes(proposal.id));

      // Remove user if and only if it has previously been
      // selected and it has no selected children
      index !== -1 && userProposals.length === 0 &&
        users.splice(index, 1);
    }
  });

  yield { users };
};
