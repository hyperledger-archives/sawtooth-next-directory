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
import { INITIAL_STATE, ApproverTypes as Types } from './ApproverActions';
import * as utils from 'services/Utils';


export const request = (state) =>
  state.merge({ fetching: true });


export const failure = (state, { error }) =>
  state.merge({ fetching: false, error });


export const resetAll = () =>
  INITIAL_STATE;


export const feedReceive = (state, { payload }) =>
  payload.open_proposal ?
    state.merge({
      openProposals: utils.merge(
        state.openProposals || [], [payload.open_proposal]
      ),
    }) :
    state.merge({});


export const success = {
  openProposals: (state, { openProposals }) =>
    state.merge({
      fetching: false,
      openProposals: openProposals.data,
    }),


  confirmedProposals: (state, { confirmedProposals }) =>
    state.merge({
      fetching: false,
      confirmedProposals: confirmedProposals.data,
    }),


  approveProposals: (state, { closedProposal }) =>
    state.merge({
      fetching: false,
      openProposals: state.openProposals.filter(
        proposal => proposal.id !== closedProposal.proposal_id
      ),
    }),


  rejectProposals: (state, { closedProposal }) =>
    state.merge({
      fetching: false,
      openProposals: state.openProposals.filter(
        proposal => proposal.id !== closedProposal.proposal_id
      ),
    }),


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
        state.createdPacks || [], [pack]
      ),
    }),


  organization: (state, { organization }) =>
    state.merge({
      fetching: false,
      organization,
    }),


  onBehalfOf: (state, { id }) =>
    state.merge({ onBehalfOf: id }),
};


export const ApproverReducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]:                    resetAll,
  [Types.FEED_RECEIVE]:                 feedReceive,

  // Proposals
  [Types.CONFIRMED_PROPOSALS_REQUEST]:  request,
  [Types.CONFIRMED_PROPOSALS_SUCCESS]:  success.confirmedProposals,
  [Types.CONFIRMED_PROPOSALS_FAILURE]:  failure,
  [Types.OPEN_PROPOSALS_REQUEST]:       request,
  [Types.OPEN_PROPOSALS_SUCCESS]:       success.openProposals,
  [Types.OPEN_PROPOSALS_FAILURE]:       failure,
  [Types.APPROVE_PROPOSALS_REQUEST]:    request,
  [Types.APPROVE_PROPOSALS_SUCCESS]:    success.approveProposals,
  [Types.APPROVE_PROPOSALS_FAILURE]:    failure,
  [Types.REJECT_PROPOSALS_REQUEST]:     request,
  [Types.REJECT_PROPOSALS_SUCCESS]:     success.rejectProposals,
  [Types.REJECT_PROPOSALS_FAILURE]:     failure,

  // Create
  [Types.CREATE_ROLE_REQUEST]:          request,
  [Types.CREATE_ROLE_SUCCESS]:          success.createRole,
  [Types.CREATE_ROLE_FAILURE]:          failure,
  [Types.CREATE_PACK_REQUEST]:          request,
  [Types.CREATE_PACK_SUCCESS]:          success.createPack,
  [Types.CREATE_PACK_FAILURE]:          failure,

  // People
  [Types.ORGANIZATION_REQUEST]:         request,
  [Types.ORGANIZATION_SUCCESS]:         success.organization,
  [Types.ORGANIZATION_FAILURE]:         failure,
  [Types.ON_BEHALF_OF_SET]:             success.onBehalfOf,
});
