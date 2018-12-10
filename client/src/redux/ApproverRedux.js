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
  openProposalsRequest:       null,
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

  resetAll:                   null,
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
  fetching:           null,
  error:              null,
  openProposals:      null,
  confirmedProposals: null,
});

//
// Selectors
//
//
//
//
export const ApproverSelectors = {
  openProposals:         (state) => state.approver.openProposals,
  confirmedProposals:    (state) => state.approver.confirmedProposals,
  openProposalsByUser:   (state) =>
    utils.groupBy(state.approver.openProposals, 'opener'),
  openProposalsByRole:   (state) =>
    utils.groupBy(state.approver.openProposals, 'object'),
  openProposalsCount:    (state) =>
    (state.approver.openProposals && state.approver.openProposals.length) ||
    null,
  openProposalFromId:    (state, id) =>
    state.approver.openProposals &&
    state.approver.openProposals.find(proposal => proposal.id === id),
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
export const openProposalsSuccess = (state, { openProposals }) => {
  return state.merge({ fetching: false, openProposals: openProposals.data });
};
export const confirmedProposalsSuccess = (state, { confirmedProposals }) => {
  return state.merge({
    fetching: false, confirmedProposals: confirmedProposals.data,
  });
};
export const createRoleSuccess = (state) => {
  return state.merge({ fetching: false });
};
export const createPackSuccess = (state) => {
  return state.merge({ fetching: false });
};
export const approveProposalsSuccess = (state, { closedProposal }) => {
  return state.merge({
    fetching: false,
    openProposals: state.openProposals
      .filter(proposal => proposal.id !== closedProposal.proposal_id),
  });
};
export const rejectProposalsSuccess = (state, { closedProposal }) => {
  return state.merge({
    fetching: false,
    openProposals: state.openProposals
      .filter(proposal => proposal.id !== closedProposal.proposal_id),
  });
};

//
// Hooks
//
//
//
//
export const reducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]: resetAll,

  [Types.OPEN_PROPOSALS_REQUEST]: request,
  [Types.OPEN_PROPOSALS_SUCCESS]: openProposalsSuccess,
  [Types.OPEN_PROPOSALS_FAILURE]: failure,

  [Types.CONFIRMED_PROPOSALS_REQUEST]: request,
  [Types.CONFIRMED_PROPOSALS_SUCCESS]: confirmedProposalsSuccess,
  [Types.CONFIRMED_PROPOSALS_FAILURE]: failure,

  [Types.CREATE_ROLE_REQUEST]: request,
  [Types.CREATE_ROLE_SUCCESS]: createRoleSuccess,
  [Types.CREATE_ROLE_FAILURE]: failure,

  [Types.CREATE_PACK_REQUEST]: request,
  [Types.CREATE_PACK_SUCCESS]: createPackSuccess,
  [Types.CREATE_PACK_FAILURE]: failure,

  [Types.APPROVE_PROPOSALS_REQUEST]: request,
  [Types.APPROVE_PROPOSALS_SUCCESS]: approveProposalsSuccess,
  [Types.APPROVE_PROPOSALS_FAILURE]: failure,

  [Types.REJECT_PROPOSALS_REQUEST]: request,
  [Types.REJECT_PROPOSALS_SUCCESS]: rejectProposalsSuccess,
  [Types.REJECT_PROPOSALS_FAILURE]: failure,
});
