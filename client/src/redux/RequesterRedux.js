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


/**
 *
 * Actions
 *
 * @property request  Initiating action
 * @property success  Action called on execution success
 * @property failure  Action called on execution failure
 *
 */
const { Types, Creators } = createActions({
  baseRequest:       null,
  baseSuccess:       ['base'],
  baseFailure:       ['error'],

  roleRequest:       ['id'],
  roleSuccess:       ['role'],
  roleFailure:       ['error'],

  rolesRequest:      ['ids'],

  proposalRequest:   ['id'],
  proposalSuccess:   ['proposal'],
  proposalFailure:   ['error'],

  proposalsRequest:  ['ids'],

  accessRequest:     ['id', 'userId', 'reason'],
  accessSuccess:     null,
  accessFailure:     null,

  resetAll:          null,
});


export const RequesterTypes = Types;
export default Creators;


/**
 *
 * State
 *
 * @property recommended
 * @property requests
 * @property fetching
 * @property activeRole
 * @property error
 *
 * @todo Consider normalizing recommended, requests, and packs
 * into one roles entity, queried by selector
 *
 */
export const INITIAL_STATE = Immutable({
  activeProposal:   null,
  activeRole:       null,
  error:            null,
  fetching:         null,
  recommended:      null,
  requests:         null,
  roles:            null,
});


/**
 *
 * Selectors
 *
 *
 */
export const RequesterSelectors = {

  roles: (state) => state.requester.roles,
  recommended: (state) =>
    state.requester.roles &&
    state.user.me &&
    state.requester.roles.filter(role =>
      !state.user.me.proposals.find(proposal =>
        proposal['object_id'] === role.id
      )
  ),

  // Retrieve role by ID
  roleFromId: (state, id) =>
    state.requester.roles &&
    state.requester.roles.find(role =>
      role.id === id
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
            .find(role => role.id === request['object'])
        }
      }
  ),

  /**
   *
   * Retrieve field ID from URL slug
   *
   * @param state       Redux state object
   * @param collection  Collection to search
   * @param slug        ID from URL
   * @param field       ID to retrieve
   *
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
          item['object_id'] === entity.id);
        break;

      default:
        result = entity;
        break;
    }

    return result && result[field];
  }
};


/**
 *
 * Reducers - General
 *
 *
 */
export const request = (state) => {
  return state.merge({ fetching: true });
}
export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
}
export const resetAll = () => {
  return INITIAL_STATE;
};


/**
 *
 * Reducers - Success
 *
 *
 */
export const roleSuccess = (state, { role }) => {
  return state.merge({
    fetching: false,
    roles: utils.merge(state.roles || [], [role])
  });
}

export const proposalSuccess = (state, { proposal }) => {
  return state.merge({
    fetching: false,
    requests: utils.merge(state.requests || [], [proposal])
  });
}

export const baseSuccess = (state, { base }) => {
  return state.merge({
    fetching: false,
    roles: utils.merge(state.roles || [], base || [])
  });
}

export const accessSuccess = (state) => {
  return state.merge({ fetching: false });
}


/**
 *
 * Hooks
 *
 *
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]: resetAll,

  [Types.BASE_REQUEST]: request,
  [Types.BASE_SUCCESS]: baseSuccess,
  [Types.BASE_FAILURE]: failure,

  [Types.ROLE_REQUEST]: request,
  [Types.ROLE_SUCCESS]: roleSuccess,
  [Types.ROLE_FAILURE]: failure,

  [Types.ROLES_REQUEST]: request,

  [Types.PROPOSAL_REQUEST]: request,
  [Types.PROPOSAL_SUCCESS]: proposalSuccess,
  [Types.PROPOSAL_FAILURE]: failure,

  [Types.PROPOSALS_REQUEST]: request,

  [Types.ACCESS_REQUEST]: request,
  [Types.ACCESS_SUCCESS]: accessSuccess,
  [Types.ACCESS_FAILURE]: failure
});
