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


import { createReducer } from 'reduxsauce';
import { INITIAL_STATE, RequesterTypes as Types } from './RequesterActions';
import * as utils from 'services/Utils';


export const request = {
  allRoles:   (state) => state.merge({ fetchingAllRoles: true }),
  allPacks:   (state) => state.merge({ fetchingAllPacks: true }),
  temp:       (state) => state.merge({ fetching: true }),
};


export const success = {
  access: (state) =>
    state.merge({ fetching: false }),
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


  allRoles: (state, { roles, rolesTotalCount }) =>
    state.merge({
      fetchingAllRoles: false,
      rolesTotalCount,
      roles: utils.merge(state.roles || [], roles || []),
    }),
  allPacks: (state, { packs, packsTotalCount }) =>
    state.merge({
      fetchingAllPacks: false,
      packsTotalCount,
      packs: utils.merge(state.packs || [], packs || []),
    }),


  pack: (state, { pack }) =>
    state.merge({
      fetching: false,
      packs: utils.merge(state.packs || [], [pack]),
    }),
  role: (state, { role }) =>
    state.merge({
      fetching: false,
      roles: utils.merge(state.roles || [], [role]),
    }),
  proposal: (state, { proposal }) =>
    state.merge({
      fetching: false,
      requests: utils.merge(state.requests || [], [proposal]),
    }),
};


export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
};


export const resetAll = () => {
  return INITIAL_STATE;
};


export const RequesterReducer = createReducer(INITIAL_STATE, {
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
