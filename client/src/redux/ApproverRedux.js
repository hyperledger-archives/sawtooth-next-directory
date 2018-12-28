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
  openProposalsRequest:       ['id'],
  openProposalsSuccess:       ['openProposals'],
  openProposalsFailure:       ['error'],

  confirmedProposalsRequest:  null,
  confirmedProposalsSuccess:  ['confirmedProposals'],
  confirmedProposalsFailure:  ['error'],

  createRoleRequest:          ['payload'],
  createRoleSuccess:          ['success'],
  createRoleFailure:          ['error'],

  createPackRequest:          ['payload'],
  createPackSuccess:          ['success'],
  createPackFailure:          ['error'],

  approveProposalsRequest:    ['ids'],
  approveProposalsSuccess:    ['closedProposal'],
  approveProposalsFailure:    ['error'],

  rejectProposalsRequest:     ['ids'],
  rejectProposalsSuccess:     ['closedProposal'],
  rejectProposalsFailure:     ['error'],

  organizationRequest:        ['id'],
  organizationSuccess:        ['organization'],
  organizationFailure:        ['error'],

  resetAll:                   null,
  onBehalfOfSet:              ['id'],
});


export const ApproverTypes = Types;
export default Creators;

//
// State
//
//
//
//
export const INITIAL_STATE = Immutable({
  confirmedProposals:   null,
  error:                null,
  fetching:             null,
  openProposals:        null,
  organization:         null,
  onBehalfOf:           null,
});

//
// Selectors
//
//
//
//
export const ApproverSelectors = {
  confirmedProposals:    (state) => state.approver.confirmedProposals,
  openProposals:         (state) => state.approver.openProposals,
  openProposalsByUser:   (state) =>
    utils.groupBy(state.approver.openProposals, 'opener'),
  openProposalsByRole:   (state) =>
    utils.groupBy(state.approver.openProposals, 'object'),
  openProposalsCount:    (state) => {
    return (
      state.user.me &&
      state.approver.openProposals &&
      state.approver.openProposals
        .filter(proposal => proposal.approvers.includes(state.user.me.id))
        .length
    ) || null;
  },
  openProposalFromId:    (state, id) =>
    state.approver.openProposals &&
    state.approver.openProposals.find(proposal => proposal.id === id),
  organization:          (state) => state.approver.organization,
  onBehalfOf:            (state) => state.approver.onBehalfOf,
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
export const success = {

  // Proposals
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

  // Create
  createRole: (state) =>
    state.merge({ fetching: false }),
  createPack: (state) =>
    state.merge({ fetching: false }),

  // People
  organization: (state, { organization }) =>
    state.merge({
      fetching: false,
      organization: organization,
    }),
  onBehalfOf: (state, { id }) =>
    state.merge({ onBehalfOf: id }),
};

//
// Hooks
//
//
//
//
export const reducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]: resetAll,

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
  [Types.ORGANIZATION_REQUEST]:          request,
  [Types.ORGANIZATION_SUCCESS]:          success.organization,
  [Types.ORGANIZATION_FAILURE]:          failure,
  [Types.ON_BEHALF_OF_SET]:              success.onBehalfOf,

});
