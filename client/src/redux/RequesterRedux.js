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
import * as utils from '../services/Utils';


//
// Actions
//
//
//
//
const { Types, Creators } = createActions({
  baseRequest:          null,
  baseSuccess:          ['base'],
  baseFailure:          ['error'],

  roleRequest:          ['id'],
  rolesRequest:         ['ids'],
  roleSuccess:          ['role'],
  roleFailure:          ['error'],

  packRequest:          ['id'],
  packsRequest:         ['ids'],
  packSuccess:          ['pack'],
  packFailure:          ['error'],

  allrolesRequest:      null,
  allrolesSuccess:      ['roles'],
  allrolesFailure:      ['error'],

  proposalRequest:      ['id'],
  proposalSuccess:      ['proposal'],
  proposalFailure:      ['error'],

  proposalsRequest:     ['ids'],

  roleAccessRequest:    ['id', 'userId', 'reason'],
  roleAccessSuccess:    null,
  roleAccessFailure:    null,

  packAccessRequest:    ['id', 'userId', 'reason'],
  packAccessSuccess:    null,
  packAccessFailure:    null,

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
  packs:            null,
  requests:         null,
  roles:            null,
});

//
// Selectors
//
//
//
//
export const RequesterSelectors = {
  roles: (state) => state.requester.roles,
  packs: (state) => state.requester.packs,


  // Retrieve recommended roles
  recommendedRoles: (state) =>
    state.requester.roles &&
    state.user.me &&
    state.requester.roles.filter(role =>
      role.packs && role.packs.length === 0 &&
      !state.user.me.proposals.find(proposal =>
        proposal.object_id === role.id
      )
    ),
  // Retrieve recommended packs
  recommendedPacks: (state) => {
    if (!state.requester.roles || !state.user.me) return null;
    const roles = state.requester.roles.filter(
        item => !state.user.me.proposals.find(e => e.object_id === item.id)
      ),
      recommend = Object.keys(utils.groupBy(roles, 'packs')).filter(item => {
        const cond1 = 0 === item.length && item.includes('undefined'),
          cond2 =
            RequesterSelectors.requests(state) &&
            RequesterSelectors.requests(state).find(obj => obj.id === item),
          cond3 =
            RequesterSelectors.mine(state) &&
            RequesterSelectors.mine(state).find(obj => obj.id === item);
        return !(cond3 || cond2 || cond1);
      });
    return recommend.join('') ? recommend : null;
  },


  // Retrieve role by ID
  roleFromId: (state, id) =>
    state.requester.roles &&
    state.requester.roles.find(role =>
      role.id === id
    ),
  // Retrieve proposal by ID
  packFromId: (state, id) =>
    state.requester.packs &&
    state.requester.packs.find(pack =>
      pack.id === id
    ),
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
      ids.includes(request.id)
    ),


  // Retrieve user requests (proposals)
  requests: (state) => {
    if (
      !state.requester.requests ||
      !state.user.me ||
      !state.requester.roles ||
      !state.requester.packs
    )
      return null;

    let open = [];
    state.requester.requests
      .filter(request => request.status === 'OPEN')
      .forEach(request => {
        const merge = { ...request, ...state.requester.roles
          .find(role => role.id === request.object),
        };
        if (merge && merge.packs && merge.packs.length > 0) {
          open.push(state.requester.packs.find(pack =>
            pack.id === merge.packs[0]
          ));
        } else {
          open.push(merge);
        }
      });

    return [...new Set(open)];
  },


  // Retrieve and group my packs / roles
  mine: (state) => {
    if (
      !state.requester.requests ||
      !state.user.me ||
      !state.requester.roles ||
      !state.requester.packs
    )
      return null;

    let confirmed = [];
    let unconfirmed = [];

    // Iterating over open proposals, constructing an object
    // for each request with info about its corresponding role
    state.requester.requests.forEach(request => {
      const merge = { ...request, ...state.requester.roles
        .find(role => role.id === request.object),
      };
      if (merge && merge.packs && merge.packs.length > 0) {
        let pack = state.requester.packs.find(pack =>
          pack.id === merge.packs[0]
        );
        merge.status !== 'CONFIRMED' && unconfirmed.push(pack.id);
        confirmed.push(pack);
      } else {
        merge.status === 'CONFIRMED' && confirmed.push(merge);
      }
    });

    // Create a new array of the form [{ pack }, {role}, ...],
    // removing duplicates and unconfirmed proposals
    let unique = [...new Set(confirmed)];
    return unique.filter(item => !unconfirmed.includes(item.id));
  },


  /**
   * Find the proposal ID(s) of a resource in the store provided
   * the URL slug of the resource
   * @param   {object} state      Redux state
   * @param   {array}  collection Redux entity
   * @param   {string} slug       URL slug
   * @param   {string} type       Entity group type (e.g., role)
   * @returns {string|array}
   */
  proposalIdFromSlug: (state, collection, slug, type) => {
    if (!collection || !state.user.me) return null;
    let result = null;
    const entity = collection.find((item) =>
      utils.createSlug(item.name) === slug);

    if (type === 'pack') {
      result = entity && state.user.me.proposals
        .filter(item => entity.roles.includes(item.object_id))
        .map(item => item.proposal_id);
    }
    if (type === 'role') {
      const proposal = entity && state.user.me.proposals
        .find(item => item.object_id === entity.id);
      result = proposal && proposal.proposal_id;
    }

    return result;
  },


  /**
   * Find the ID of a resource in the store provided
   * the URL slug of the resource
   * @param   {object} state      Redux state
   * @param   {array}  collection Redux entity
   * @param   {string} slug       URL slug
   * @returns {string}
   */
  idFromSlug: (state, collection, slug) => {
    if (!collection) return null;
    const result = collection.find((item) =>
      utils.createSlug(item.name) === slug);
    return result && result.id;
  },
};


//
// Reducers
// General
//
//
//
export const request = (state) => {
  return state.merge({ fetching: true });
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
export const roleSuccess = (state, { role }) => {
  return state.merge({
    fetching: false,
    roles: utils.merge(state.roles || [], [role]),
  });
};

export const packSuccess = (state, { pack }) => {
  return state.merge({
    fetching: false,
    packs: utils.merge(state.packs || [], [pack]),
  });
};

export const allrolesSuccess = (state, { roles }) => {
  return state.merge({
    fetching: false,
    roles: roles,
  });
};

export const proposalSuccess = (state, { proposal }) => {
  return state.merge({
    fetching: false,
    requests: utils.merge(state.requests || [], [proposal]),
  });
};

export const baseSuccess = (state, { base }) => {
  return state.merge({
    fetching: false,
    roles: utils.merge(state.roles || [], base[0].data.data || []),
    packs: utils.merge(state.packs || [], base[1].data.data || []),
  });
};

export const accessSuccess = (state) => {
  return state.merge({ fetching: false });
};

//
// Hooks
//
//
//
//
export const reducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]: resetAll,

  [Types.BASE_REQUEST]: request,
  [Types.BASE_SUCCESS]: baseSuccess,
  [Types.BASE_FAILURE]: failure,

  [Types.ROLE_REQUEST]: request,
  [Types.ROLES_REQUEST]: request,
  [Types.ROLE_SUCCESS]: roleSuccess,
  [Types.ROLE_FAILURE]: failure,

  [Types.PACK_REQUEST]: request,
  [Types.PACKS_REQUEST]: request,
  [Types.PACK_SUCCESS]: packSuccess,
  [Types.PACK_FAILURE]: failure,

  [Types.ALLROLES_REQUEST]: request,
  [Types.ALLROLES_SUCCESS]: allrolesSuccess,
  [Types.ALLROLES_FAILURE]: failure,

  [Types.PROPOSAL_REQUEST]: request,
  [Types.PROPOSALS_REQUEST]: request,
  [Types.PROPOSAL_SUCCESS]: proposalSuccess,
  [Types.PROPOSAL_FAILURE]: failure,

  [Types.ROLE_ACCESS_REQUEST]: request,
  [Types.ROLE_ACCESS_SUCCESS]: accessSuccess,
  [Types.ROLE_ACCESS_FAILURE]: failure,

  [Types.PACK_ACCESS_REQUEST]: request,
  [Types.PACK_ACCESS_SUCCESS]: accessSuccess,
  [Types.PACK_ACCESS_FAILURE]: failure,
});
