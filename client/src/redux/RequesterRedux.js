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
  baseRequest:       null,
  baseSuccess:       ['base'],
  baseFailure:       ['error'],

  roleRequest:       ['id'],
  rolesRequest:      ['ids'],
  roleSuccess:       ['role'],
  roleFailure:       ['error'],

  packRequest:       ['id'],
  packsRequest:      ['ids'],
  packSuccess:       ['pack'],
  packFailure:       ['error'],

  allrolesRequest:   null,
  allrolesSuccess:   ['roles'],
  allrolesFailure:   ['error'],

  proposalRequest:   ['id'],
  proposalSuccess:   ['proposal'],
  proposalFailure:   ['error'],

  proposalsRequest:  ['ids'],

  roleAccessRequest:     ['id', 'userId', 'reason'],
  roleAccessSuccess:      null,
  roleAccessFailure:     null,

  packAccessRequest:     ['id', 'userId', 'reason'],
  packAccessSuccess:     null,
  packAccessFailure:     null,

  resetAll:          null,
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

  recommendedRoles: (state) =>
    state.requester.roles &&
    state.user.me &&
    state.requester.roles.filter(role =>
      role.packs && role.packs.length === 0 &&
      !state.user.me.proposals.find(proposal =>
        proposal.object_id === role.id
      )
    ),

  recommendedPacks: (state) => {
    if (!state.requester.roles || !state.user.me) return null;
    const recommended = Object.keys(
      utils.groupBy(state.requester.roles, 'packs')
    ).filter(packId =>
      packId.length > 0 && !packId.includes('undefined')
    );
    return recommended.join('') ? recommended : null;
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

  // Retrieve user requests (proposals)
  requests: (state) =>
    state.user.me &&
    state.requester.roles &&
    state.requester.requests &&
    state.requester.requests
      .filter(request => request.status === 'OPEN')
      .map(request => {
        return {
          ...request,
          ...state.requester.roles
            .find(role => role.id === request.object),
        };
      }),


  /**
   * Retrieve field ID from URL slug
   * @param   {object} state      Redux state
   * @param   {array}  collection Collection to search
   * @param   {string} slug       URL slug
   * @param   {string} field      ID to retrieve
   * @returns {string}
   */
  idFromSlug: (state, collection, slug, field) => {
    if (!collection) return null;

    let result = {};
    field = field || 'id';
    const entity = collection.find((item) =>
      utils.createSlug(item.name) === slug);

    switch (field) {
      case 'proposal_id':
        result = state.user.me && entity &&
        state.user.me.proposals.find((item) =>
          item.object_id === entity.id);
        break;
      default:
        result = entity;
        break;
    }
    return result && result[field];
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
  [Types.PROPOSAL_SUCCESS]: proposalSuccess,
  [Types.PROPOSAL_FAILURE]: failure,

  [Types.PROPOSALS_REQUEST]: request,

  [Types.ROLE_ACCESS_REQUEST]: request,
  [Types.ROLE_ACCESS_SUCCESS]: accessSuccess,
  [Types.ROLE_ACCESS_FAILURE]: failure,

  [Types.PACK_ACCESS_REQUEST]: request,
  [Types.PACK_ACCESS_SUCCESS]: accessSuccess,
  [Types.PACK_ACCESS_FAILURE]: failure,
});
