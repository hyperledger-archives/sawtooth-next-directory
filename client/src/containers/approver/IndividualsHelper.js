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
 *
 * Sync selections by proposal generator
 *
 *
 *
 */
export function * selectRoles (checked, collection, proposals, roles) {
  collection.forEach(proposal => {
    const indices = [
      roles.indexOf(proposal.object),
      proposals.indexOf(proposal.id),
    ];

    if (checked) {
      roles = indices[0] === -1 ? [...roles, proposal.object] : roles;
      proposals = indices[1] === -1 ? [...proposals, proposal.id] : proposals;
    } else {
      indices[0] !== -1 && roles.splice(indices[0], 1);
      indices[1] !== -1 && proposals.splice(indices[1], 1);
    }
  });

  yield { roles, proposals };
};


/**
 *
 * Sync selections by user generator
 *
 *
 *
 */
export function * selectUser (checked, userId, proposals, users) {
  const index = users.indexOf(userId);

  if (checked) {
    users = (index === -1) ? [...users, userId] : users;
  } else {
    const userProposals = proposals.filter(proposal => {
      return proposal.opener === userId;
    });

    // Remove user if and only if it has previously been
    // selected and it has no selected children
    index !== -1 && userProposals.length === 0 &&
      users.splice(index, 1);
  }

  yield { users };
};
