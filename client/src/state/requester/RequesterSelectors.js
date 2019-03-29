/* Copyright 2019 Contributors to Hyperledger Sawtooth

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


import * as utils from 'services/Utils';
import { ApproverSelectors } from 'state';


export const RequesterSelectors = {
  rolesTotalCount: (state) =>
    state.requester.rolesTotalCount,


  packsTotalCount: (state) =>
    state.requester.packsTotalCount,


  roles: (state) => utils.merge(
    state.requester.roles || [],
    state.approver.createdRoles || [],
  ),


  packs: (state) => utils.merge(
    state.requester.packs || [],
    state.approver.createdPacks || [],
  ),


  browseData: (state) => {
    const formatted = [[], [], [], []];
    const data = [
      ...state.requester.packs || [],
      ...state.requester.roles || [],
    ];
    const sorted = utils.sort(data, 'name');
    sorted.forEach((item, index) => {
      formatted[index % 4].push(item);
    });
    return formatted;
  },


  // Retrieve recommended roles
  recommendedRoles: (state) =>
    state.requester.recommended &&
    state.user.me &&
    state.requester.recommended.filter(role =>
      role.packs && role.packs.length === 0 &&
      role.members.length > 0 &&
      ![...state.user.me.proposals,
        ...(state.requester.requests || []),
      ]
        .find(proposal =>
          proposal.object_id === role.id ||
          proposal.object === role.id
        ) &&
      !state.user.me.memberOf.includes(role.id) &&
      !state.user.me.ownerOf.roles.includes(role.id)
    ).slice(0, 3),


  // Retrieve recommended packs
  recommendedPacks: (state) => {
    if (!state.requester.recommended || !state.user.me) return null;

    const roles = state.requester.recommended.filter(
      item => !state.user.me.proposals.find(
        e => e.object_id === item.id
      )
    );
    const recommend = Object.keys(utils.groupBy(roles, 'packs'))
      .filter(item => {
        const cond1 = !item ||
                      (0 === item.length && item.includes('undefined'));

        // User cannot have previously requested access
        const cond2 = RequesterSelectors.requests(state) &&
                      RequesterSelectors.requests(state).find(
                        obj => obj.id === item
                      );

        // User cannot be a member
        const cond3 = RequesterSelectors.memberOf(state) &&
                      RequesterSelectors.memberOf(state).find(
                        obj => obj.id === item
                      );

        // User cannot be an owner
        const cond4 = state.user.me.ownerOf.packs.includes(item);
        return !(cond4 || cond3 || cond2 || cond1);
      });

    return recommend.join('') ? [...new Set(
      recommend.join(',').replace(/,+/g, ',').split(',')
    )] : null;
  },


  // Retrieve role by ID
  roleFromId: (state, id) =>
    [
      ...state.requester.roles || [],
      ...state.approver.createdRoles || [],
    ]
      .find(role => role.id === id),


  // Retrieve pack by ID
  packFromId: (state, id) =>
    [
      ...state.requester.packs || [],
      ...state.approver.createdPacks || [],
    ]
      .find(pack => pack.id === id),


  // Retrieve proposal by ID
  proposalFromId: (state, id) =>
    state.requester.requests &&
    state.requester.requests.find(request =>
      request.id === id
    ),


  // Retrieve proposals by IDs
  proposalsFromIds: (state, ids) =>
    state.requester.requests &&
    state.requester.requests.filter(request =>
      ids && ids.includes(request.id)
    ),


  // Retrieve user requests (proposals)
  requests: (state) => {
    if (!state.requester.requests ||
        !state.requester.roles)
      return null;

    const requests = [];
    state.requester.requests
      .filter(
        request => request.status !== 'CONFIRMED'
      )
      .forEach(request => {
        const role = {
          ...state.requester.roles.find(
            role => role.id === request.object
          ),
        };
        delete role.metadata;
        const merged = { ...request, ...role };

        if (merged.pack_id) {
          const pack = state.requester.packs &&
            state.requester.packs.find(
              pack => pack.id === merged.pack_id
            );
          pack && requests.push(pack);
        } else {
          requests.push(merged);
        }
      });

    return [...new Set(requests)];
  },


  // Retrieve a unique set of packs and roles a user
  // is member of grouped like the following:
  // [{ pack }, { role }, { pack } ...]
  memberOf: (state) => {
    if (!state.user.me) return null;
    let memberOf = [];

    for (const roleId of state.user.me.memberOf) {
      const request = state.user.me.proposals.find(
        item => item.object_id === roleId
      );

      if (request){
        if (state.requester.roles) {
          const role = state.requester.roles.find(
            role => role.id === roleId
          );
          role && memberOf.push(role);
        }
      }
    }

    memberOf = memberOf.filter(item => {
      if (item.roles) {
        if (!state.requester.requests) return false;
        const isOpen = state.requester.requests.find(
          request => item.roles.includes(request.object) &&
            request.status !== 'CONFIRMED'
        );
        return !isOpen;
      }
      return true;
    });

    return [...new Set(memberOf)];
  },

  memberOfPacks: (state) => {
    if (!state.user.me) return null;
    let memberOfPacks = [];

    for (const roleId of state.user.me.memberOf) {
      const request = state.user.me.proposals.find(
        item => item.object_id === roleId
      );

      if (request && request.pack_id) {
        if (state.requester.packs){
          const pack = state.requester.packs.find(
            pack => pack.id === request.pack_id
          );
          pack && memberOfPacks.push(pack);
        }
        continue;
      }
    }

    memberOfPacks = memberOfPacks.filter(item => {
      if (item.roles) {
        if (!state.requester.requests) return false;
        const isOpen = state.requester.requests.find(
          request => item.roles.includes(request.object) &&
            request.status !== 'CONFIRMED'
        );
        return !isOpen;
      }
      return true;
    });

    return [...new Set(memberOfPacks)];

  },

  ownerOf: (state) =>
    [...new Set([
      ...(ApproverSelectors.ownedPacks(state) || []),
      ...(ApproverSelectors.ownedRoles(state) || []),
    ])],


  /**
   * Find the proposal ID of a role
   * @param   {object} state      Redux state
   * @param   {string} id         Role ID
   * @returns {string}
   */
  roleProposalId: (state, id) => {
    if (!state.requester.requests) return null;
    const proposal = state.requester.requests
      .find(item => item.object === id);
    return proposal && proposal.id;
  },


  /**
   * Find the proposal IDs of a pack
   * @param   {object} state      Redux state
   * @param   {string} id         Pack ID
   * @returns {array}
   */
  packProposalIds: (state, id) =>
    state.requester.requests &&
    state.requester.requests.filter(
      item => item.pack_id === id
    ).map(item => item.id),
};
