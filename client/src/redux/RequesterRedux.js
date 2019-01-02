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


import { createReducer, createActions } from 'reduxsauce';
import Immutable from 'seamless-immutable';
import * as utils from 'services/Utils';


//
// Actions
//
//
//
//
const { Types, Creators } = createActions({
  allPacksRequest:      ['start', 'limit'],
  allPacksSuccess:      ['packs', 'packsTotalCount'],
  allPacksFailure:      ['error'],

  allRolesRequest:      ['start', 'limit'],
  allRolesSuccess:      ['roles', 'rolesTotalCount'],
  allRolesFailure:      ['error'],

  roleRequest:          ['id'],
  rolesRequest:         ['ids'],
  roleSuccess:          ['role'],
  roleFailure:          ['error'],

  baseRequest:          null,
  baseSuccess:          ['base'],
  baseFailure:          ['error'],

  packRequest:          ['id'],
  packsRequest:         ['ids'],
  packSuccess:          ['pack'],
  packFailure:          ['error'],

  proposalRequest:      ['id'],
  proposalSuccess:      ['proposal'],
  proposalFailure:      ['error'],
  proposalsRequest:     ['ids'],

  packAccessRequest:    ['id', 'userId', 'reason'],
  packAccessSuccess:    null,
  packAccessFailure:    null,

  roleAccessRequest:    ['id', 'userId', 'reason'],
  roleAccessSuccess:    null,
  roleAccessFailure:    null,

  resetAll:             null,
});


export const RequesterTypes = Types;
export default Creators;

//
// State
//
//
//
//
export const INITIAL_STATE = Immutable({
  activeProposal:   null,
  activeRole:       null,
  error:            null,
  fetching:         null,
  fetchingAllRoles: null,
  fetchingAllPacks: null,
  packs:            null,
  recommended:      null,
  requests:         null,
  roles:            null,
  rolesTotalCount:  null,
  packsTotalCount:  null,
});

//
// Selectors
//
//
//
//
export const RequesterSelectors = {
  rolesTotalCount: (state) => state.requester.rolesTotalCount,
  packsTotalCount: (state) => state.requester.packsTotalCount,
  roles: (state) => [
    ...state.requester.roles || [],
    ...state.approver.createdRoles || [],
  ],
  packs: (state) => [
    ...state.requester.packs || [],
    ...state.approver.createdPacks || [],
  ],


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
      !state.user.me.proposals.find(proposal =>
        proposal.object_id === role.id
      )
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

        const cond2 = RequesterSelectors.requests(state) &&
                      RequesterSelectors.requests(state).find(
                        obj => obj.id === item
                      );
        const cond3 = RequesterSelectors.mine(state) &&
                      RequesterSelectors.mine(state).find(
                        obj => obj.id === item
                      );
        return !(cond3 || cond2 || cond1);
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

        if (merged.metadata && merged.metadata.length) {
          const metadata = JSON.parse(merged.metadata);
          state.requester.packs && requests.push(
            state.requester.packs.find(
              pack => pack.id === metadata.pack_id
            )
          );
        } else {
          requests.push(merged);
        }
      });

    return [...new Set(requests)];
  },


  // Retrieve a unique set of packs and roles a user
  // is member of grouped like the following:
  // [{ pack }, { role }, { pack } ...]
  mine: (state) => {
    if (!state.user.me) return null;
    const mine = [];

    for (const roleId of state.user.me.memberOf) {
      const request = state.user.me.proposals.find(
        item => item.object_id === roleId
      );

      if (request) {
        const metadata = request.metadata &&
          request.metadata.length &&
          JSON.parse(request.metadata);
        if (metadata) {
          if (state.requester.packs) {
            const pack = state.requester.packs.find(
              pack => pack.id === metadata.pack_id
            );
            pack && mine.push(pack);
          }
          continue;
        }
      }
      if (state.requester.roles) {
        const role = state.requester.roles.find(
          role => role.id === roleId
        );
        role && mine.push(role);
      }
    }

    return [...new Set(mine)];
  },


  /**
   * Find the proposal ID of a role
   * @param   {object} state      Redux state
   * @param   {string} id         Object ID
   * @returns {string}
   */
  roleProposalId: (state, id) => {
    if (!state.user.me) return null;
    let result = null;
    const proposal = state.user.me.proposals
      .find(item => item.object_id === id);
    result = proposal && proposal.proposal_id;

    return result;
  },

  /**
   * Find the proposal IDs of a pack
   * @param   {object} state      Redux state
   * @param   {string} id         Pack ID
   * @returns {array}
   */
  packProposalIds: (state, id) => {
    if (!state.user.me) return null;
    return state.user.me.proposals.filter(
      item => {
        const metadata = item.metadata &&
          item.metadata.length &&
          JSON.parse(item.metadata);
        return metadata && metadata.pack_id === id;
      }
    ).map(item => item.proposal_id);
  },
};

//
// Reducers
// General
//
//
//
export const request = {
  allRoles:   (state) => state.merge({ fetchingAllRoles: true }),
  allPacks:   (state) => state.merge({ fetchingAllPacks: true }),
  temp:       (state) => state.merge({ fetching: true }),
};

export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
};
export const resetAll = () => {
  return INITIAL_STATE;
};

//
// Reducers
// Success
//
//
//
export const success = {
  access: (state) =>
    state.merge({
      fetching: false,
    }),
  allRoles: (state, { roles, rolesTotalCount }) =>
    state.merge({
      fetchingAllRoles: false,
      rolesTotalCount,
      roles: utils.merge(
        state.roles || [], roles || []
      ),
    }),
  allPacks: (state, { packs, packsTotalCount }) =>
    state.merge({
      fetchingAllPacks: false,
      packsTotalCount,
      packs: utils.merge(
        state.packs || [], packs || []
      ),
    }),
  base: (state, { base }) =>
    state.merge({
      fetching: false,
      recommended: utils.merge(
        state.recommended || [], base[0].data.data || []
      ),
      roles: utils.merge(
        state.roles || [], base[0].data.data || []
      ),
    }),
  pack: (state, { pack }) =>
    state.merge({
      fetching: false,
      packs: utils.merge(
        state.packs || [], [pack]
      ),
    }),
  proposal: (state, { proposal }) =>
    state.merge({
      fetching: false,
      requests: utils.merge(
        state.requests || [], [proposal]
      ),
    }),
  role: (state, { role }) => {
    return state.merge({
      fetching: false,
      roles: utils.merge(
        state.roles || [], [role]
      ),
    });
  },
};

//
// Hooks
//
//
//
//
export const reducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]:              resetAll,
  [Types.BASE_REQUEST]:           request.temp,
  [Types.BASE_SUCCESS]:           success.base,
  [Types.BASE_FAILURE]:           failure,

  // Roles
  [Types.ALL_ROLES_REQUEST]:      request.allRoles,
  [Types.ALL_ROLES_SUCCESS]:      success.allRoles,
  [Types.ALL_ROLES_FAILURE]:      failure,
  [Types.ROLES_REQUEST]:          request.temp,
  [Types.ROLE_REQUEST]:           request.temp,
  [Types.ROLE_SUCCESS]:           success.role,
  [Types.ROLE_FAILURE]:           failure,
  [Types.ROLE_ACCESS_REQUEST]:    request.temp,
  [Types.ROLE_ACCESS_SUCCESS]:    success.access,
  [Types.ROLE_ACCESS_FAILURE]:    failure,

  // Packs
  [Types.ALL_PACKS_REQUEST]:      request.allPacks,
  [Types.ALL_PACKS_SUCCESS]:      success.allPacks,
  [Types.ALL_PACKS_FAILURE]:      failure,
  [Types.PACKS_REQUEST]:          request.temp,
  [Types.PACK_REQUEST]:           request.temp,
  [Types.PACK_SUCCESS]:           success.pack,
  [Types.PACK_FAILURE]:           failure,
  [Types.PACK_ACCESS_REQUEST]:    request.temp,
  [Types.PACK_ACCESS_SUCCESS]:    success.access,
  [Types.PACK_ACCESS_FAILURE]:    failure,

  // Proposals
  [Types.PROPOSALS_REQUEST]:      request.temp,
  [Types.PROPOSAL_REQUEST]:       request.temp,
  [Types.PROPOSAL_SUCCESS]:       success.proposal,
  [Types.PROPOSAL_FAILURE]:       failure,
});
