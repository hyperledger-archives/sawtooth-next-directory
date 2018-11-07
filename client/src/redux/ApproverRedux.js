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


/**
 *
 * Actions
 *
 * @property
 * @property
 *
 */
const { Types, Creators } = createActions({
  openProposalsRequest:   null,
  openProposalsSuccess:   ['openProposals'],
  openProposalsFailure:   ['error'],
});


export const ApproverTypes = Types;
export default Creators;


/**
 *
 * State
 *
 * @property isAuthenticated
 * @property fetching
 * @property error
 *
 */
export const INITIAL_STATE = Immutable({
  fetching:         null,
  error:            null,
  openProposals:    null,
});


/**
 *
 * Selectors
 *
 *
 */
export const ApproverSelectors = {
  openProposals: (state) => state.approver.openProposals
};


/**
 *
 * Reducers
 *
 *
 */
export const request = (state) => state.merge({ fetching: true });
export const success = (state, { openProposals }) => {
  return state.merge({ fetching: false, openProposals });
}
export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
}


/**
 *
 * Hooks
 *
 *
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.OPEN_PROPOSALS_REQUEST]: request,
  [Types.OPEN_PROPOSALS_SUCCESS]: success,
  [Types.OPEN_PROPOSALS_FAILURE]: failure,
});
