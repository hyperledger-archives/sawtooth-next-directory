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


import { createReducer } from 'reduxsauce';
import { INITIAL_STATE, ApproverTypes as Types } from './ApproverActions';
import * as utils from 'services/Utils';


export const request = {
  organization: (state) => state.merge({ fetchingOrganization: true }),
  deletePack:   (state) => state.merge({ deletingPack: true }),
  temp:         (state) => state.merge({ fetching: true }),
};


export const failure = (state, { error }) =>
  state.merge({ fetching: false, error });


export const resetAll = () =>
  INITIAL_STATE;


export const resetRoleExists = (state) =>
  state.merge({ roleExists: null });


export const resetPackExists = (state) =>
  state.merge({ packExists: null });


export const feedReceive = (state, { payload }) =>
  payload.open_proposal ?
    state.merge({
      openProposals: utils.merge(
        state.openProposals || [], [payload.open_proposal]
      ),
    }) :
    state.merge({});


export const success = {
  delegations: (state, { delegations }) =>
    state.merge({
      fetching:             false,
      delegations:          delegations.data,
    }),


  openProposals: (state, { openProposals }) =>
    state.merge({
      fetching:             false,
      openProposals:        openProposals.data,
    }),


  confirmedProposals: (state, { confirmedProposals }) =>
    state.merge({
      fetching:             false,
      confirmedProposals:   confirmedProposals.data,
    }),


  rejectedProposals: (state, { rejectedProposals }) =>
    state.merge({
      fetching:             false,
      rejectedProposals:    rejectedProposals.data,
    }),


  approveProposals: (state, { closedProposals }) =>
    closedProposals.proposal_ids ?
      state.merge({
        fetching: false,
        openProposals: state.openProposals.filter(
          proposal => !closedProposals.proposal_ids.includes(proposal.id)
        ),
      }) :
      state.merge({ fetching: false }),


  rejectProposals: (state, { closedProposals }) =>
    closedProposals.proposal_ids ?
      state.merge({
        fetching: false,
        openProposals: state.openProposals.filter(
          proposal => !closedProposals.proposal_ids.includes(proposal.id)
        ),
      }) :
      state.merge({ fetching: false }),


  createRole: (state, { role }) =>
    state.merge({
      fetching: false,
      createdRoles: utils.merge(
        state.createdRoles || [], [role]
      ),
    }),


  createPack: (state, { pack }) =>
    state.merge({
      fetching: false,
      createdPacks: utils.merge(
        state.createdPacks || [], [pack], 'pack_id',
      ),
    }),


  deletePack: (state, { packId }) =>
    state.merge({
      fetching: false,
      deletingPack: false,
      createdPacks: state.createdPacks ?
        state.createdPacks.filter(pack => pack.id !== packId) :
        state.createdPacks,
    }),


  organization: (state, { organization, isMe }) => {
    const { created_date, ...filtered } = organization;
    return state.merge({
      fetchingOrganization: false,
      organization: filtered,
      directReports: isMe ? filtered.direct_reports : state.directReports,
    });
  },


  onBehalfOf: (state, { id }) =>
    state.merge({ onBehalfOf: id }),


  roleExists: (state, { exists }) =>
    state.merge({ roleExists: exists }),


  packExists: (state, { exists }) =>
    state.merge({ packExists: exists }),
};


export const ApproverReducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]:                    resetAll,
  [Types.FEED_RECEIVE]:                 feedReceive,

  // Delegations
  [Types.DELEGATIONS_REQUEST]:          request.temp,
  [Types.DELEGATIONS_SUCCESS]:          success.delegations,
  [Types.DELEGATIONS_FAILURE]:          failure,

  // Proposals
  [Types.CONFIRMED_PROPOSALS_REQUEST]:  request.temp,
  [Types.CONFIRMED_PROPOSALS_SUCCESS]:  success.confirmedProposals,
  [Types.CONFIRMED_PROPOSALS_FAILURE]:  failure,
  [Types.REJECTED_PROPOSALS_REQUEST]:   request.temp,
  [Types.REJECTED_PROPOSALS_SUCCESS]:   success.rejectedProposals,
  [Types.REJECTED_PROPOSALS_FAILURE]:   failure,
  [Types.OPEN_PROPOSALS_REQUEST]:       request.temp,
  [Types.OPEN_PROPOSALS_SUCCESS]:       success.openProposals,
  [Types.OPEN_PROPOSALS_FAILURE]:       failure,
  [Types.APPROVE_PROPOSALS_REQUEST]:    request.temp,
  [Types.APPROVE_PROPOSALS_SUCCESS]:    success.approveProposals,
  [Types.APPROVE_PROPOSALS_FAILURE]:    failure,
  [Types.REJECT_PROPOSALS_REQUEST]:     request.temp,
  [Types.REJECT_PROPOSALS_SUCCESS]:     success.rejectProposals,
  [Types.REJECT_PROPOSALS_FAILURE]:     failure,

  // Create
  [Types.CREATE_ROLE_REQUEST]:          request.temp,
  [Types.CREATE_ROLE_SUCCESS]:          success.createRole,
  [Types.CREATE_ROLE_FAILURE]:          failure,
  [Types.CREATE_PACK_REQUEST]:          request.temp,
  [Types.CREATE_PACK_SUCCESS]:          success.createPack,
  [Types.CREATE_PACK_FAILURE]:          failure,
  [Types.ROLE_EXISTS_REQUEST]:          request.temp,
  [Types.ROLE_EXISTS_SUCCESS]:          success.roleExists,
  [Types.ROLE_EXISTS_FAILURE]:          failure,
  [Types.RESET_ROLE_EXISTS]:            resetRoleExists,
  [Types.PACK_EXISTS_REQUEST]:          request.temp,
  [Types.PACK_EXISTS_SUCCESS]:          success.packExists,
  [Types.PACK_EXISTS_FAILURE]:          failure,
  [Types.RESET_PACK_EXISTS]:            resetPackExists,

  // Delete
  [Types.DELETE_PACK_REQUEST]:          request.deletePack,
  [Types.DELETE_PACK_SUCCESS]:          success.deletePack,
  [Types.DELETE_PACK_FAILURE]:          failure,

  // People
  [Types.ORGANIZATION_REQUEST]:         request.organization,
  [Types.ORGANIZATION_SUCCESS]:         success.organization,
  [Types.ORGANIZATION_FAILURE]:         failure,
  [Types.ON_BEHALF_OF_SET]:             success.onBehalfOf,
});
