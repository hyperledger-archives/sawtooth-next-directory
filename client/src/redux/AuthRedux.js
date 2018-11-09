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
import * as storage from '../services/Storage';


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
  loginRequest:     ['username', 'password'],
  loginSuccess:     ['isAuthenticated', 'payload'],
  loginFailure:     ['error'],

  signupRequest:    ['name', 'username', 'password', 'email'],
  signupSuccess:    ['isAuthenticated', 'payload'],
  signupFailure:    ['error'],

  logoutRequest:    null,
  logoutSuccess:    null,
  logoutFailure:    ['error']
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
  error:            null,
  user:             null
});


/**
 *
 * Selectors
 *
 *
 */
export const AuthSelectors = {
  isAuthenticated: (state) => {
    return !!storage.getToken() || state.auth.isAuthenticated;
  },
  user: (state) => {
    return state.auth.user || { id: storage.get('user_id') }
  }
};


/**
 *
 * Reducers
 *
 *
 */
export const request = (state) => state.merge({ fetching: true, error: false });

export const success = (state, { isAuthenticated, payload }) => {
  storage.setToken(payload.authorization);

  payload.user ?
    storage.set('user_id', payload.user.id) :
    storage.set('user_id', payload.user_id);

  return state.merge({
    isAuthenticated,
    fetching: false,
    user: payload.user,
    token: payload.authorization
  });
}

export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
}

export const logout = (state) => {
  storage.removeToken();
  storage.remove('user_id');

  return INITIAL_STATE;
}


/**
 *
 * Hooks
 *
 *
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.LOGIN_REQUEST]: request,
  [Types.LOGIN_SUCCESS]: success,
  [Types.LOGIN_FAILURE]: failure,

  [Types.SIGNUP_REQUEST]: request,
  [Types.SIGNUP_SUCCESS]: success,
  [Types.SIGNUP_FAILURE]: failure,

  [Types.LOGOUT_REQUEST]: request,
  [Types.LOGOUT_SUCCESS]: logout,
  [Types.LOGOUT_FAILURE]: failure,
});
