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
  batchRequest:           ['userId'],
  batchSuccess:           null,
  batchFailure:           ['error'],

  rolesRequest:           ['userId'],
  rolesSuccess:           null,
  rolesFailure:           ['error'],

  individualsRequest:     ['userId'],
  individualsSuccess:     null,
  individualsFailure:     ['error'],

  frequentRequest:        ['userId'],
  frequentSuccess:        null,
  frequentFailure:        ['error'],

  nearExpiryRequest:      ['userId'],
  nearExpirySuccess:      null,
  nearExpiryFailure:      ['error']
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
  error:            null
});


/**
 * 
 * Selectors
 * 
 * 
 */
export const ApproverSelectors = {
  
};


export const request = (state) => state.merge({ fetching: true });
export const success = (state) => {
  return state.merge({ fetching: false });
}
export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
}


/**
 * 
 * Reducers
 * 
 * 
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.BATCH_REQUEST]: request,
  [Types.BATCH_SUCCESS]: success,
  [Types.BATCH_FAILURE]: failure,

  [Types.ROLES_REQUEST]: request,
  [Types.ROLES_SUCCESS]: success,
  [Types.ROLES_FAILURE]: failure,

  [Types.INDIVIDUALS_REQUEST]: request,
  [Types.INDIVIDUALS_SUCCESS]: success,
  [Types.INDIVIDUALS_FAILURE]: failure,

  [Types.FREQUENT_REQUEST]: request,
  [Types.FREQUENT_SUCCESS]: success,
  [Types.FREQUENT_FAILURE]: failure,

  [Types.NEAR_EXPIRY_REQUEST]: request,
  [Types.NEAR_EXPIRY_SUCCESS]: success,
  [Types.NEAR_EXPIRY_FAILURE]: failure
});
