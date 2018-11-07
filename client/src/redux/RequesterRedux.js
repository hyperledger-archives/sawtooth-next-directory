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
  roleSuccess:       ['activeRole'],
  roleFailure:       ['error'],

  proposalRequest:   ['id'],
  proposalSuccess:   ['activeProposal'],
  proposalFailure:   ['error'],

  accessRequest:     ['id', 'userId', 'reason'],
  accessSuccess:     null,
  accessFailure:     null
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
});


/**
 *
 * Selectors
 *
 *
 */
export const RequesterSelectors = {
  activeRole:      (state) => state.requester.activeRole,
  activeProposal:  (state) => state.requester.activeProposal,
  recommended:     (state) => state.requester.recommended,

  idFromSlug: (collection, slug, field) => {
    if (!collection) return null;

    field = field || 'id';

    const entity = collection.find((item) => {
      return utils.createSlug(item.name) === slug
    });

    return entity && entity[field];
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


/**
 *
 * Reducers - Success
 *
 *
 */
export const roleSuccess = (state, { activeRole }) => {
  return state.merge({
    fetching: false,
    activeRole: activeRole.data
  });
}

export const proposalSuccess = (state, { activeProposal }) => {
  return state.merge({
    fetching: false,
    activeProposal: activeProposal.data
  });
}

export const baseSuccess = (state, { base }) => {
  return state.merge({
    fetching: false,
    // recommended: base.recommended,

    // ! Use existing endpoint for now
    recommended: base.data,
    requests: base.requests
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
  [Types.BASE_REQUEST]: request,
  [Types.BASE_SUCCESS]: baseSuccess,
  [Types.BASE_FAILURE]: failure,

  [Types.ROLE_REQUEST]: request,
  [Types.ROLE_SUCCESS]: roleSuccess,
  [Types.ROLE_FAILURE]: failure,

  [Types.PROPOSAL_REQUEST]: request,
  [Types.PROPOSAL_SUCCESS]: proposalSuccess,
  [Types.PROPOSAL_FAILURE]: failure,

  [Types.ACCESS_REQUEST]: request,
  [Types.ACCESS_SUCCESS]: accessSuccess,
  [Types.ACCESS_FAILURE]: failure
});
