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
 * @property loginRequest
 * @property loginSuccess
 * 
 */
const { Types, Creators } = createActions({
  loginRequest:     ['username', 'password'],
  loginSuccess:     ['isAuthenticated'],
  loginFailure:     ['error']
});


export const AuthTypes = Types;
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
  isAuthenticated:  null,
  fetching:         null,
  error:            null
});


/**
 * 
 * Selectors
 * 
 * 
 */
export const AuthSelectors = {
  isAuthenticated: (state) => {
    return state.auth.isAuthenticated;
  }
};


export const request = (state) => state.merge({ fetching: true });
export const success = (state, { isAuthenticated }) => {
  return state.merge({ fetching: false, isAuthenticated });
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
  [Types.LOGIN_REQUEST]: request,
  [Types.LOGIN_SUCCESS]: success,
  [Types.LOGIN_FAILURE]: failure
});
