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
import { INITIAL_STATE, AuthTypes as Types } from './AuthActions';
import * as storage from 'services/Storage';


export const request = {
  signup:    (state) => state.merge({ pendingSignup: true }),
  login:     (state) => state.merge({ pendingLogin: true }),
  logout:    (state) => state.merge({}),
};


export const success = {
  login: (state, { isAuthenticated, payload }) => {
    if (payload.token)
      storage.setToken(payload.token);
    if (payload.data) {
      payload.data.user ?
        storage.setUserId(payload.data.user.id) :
        storage.setUserId(payload.data.next_id);
    }
    return state.merge({
      isAuthenticated,
      pendingLogin: false,
      user: payload.data && payload.data.user,
    });
  },


  signup: (state, { base }) =>
    state.merge({
      pendingSignup: false,
    }),
};


export const failure = (state, { error }) => {
  return state.merge({
    pendingLogin: false,
    pendingSignup: false,
    error,
  });
};


export const resetErrors = (state) =>
  state.merge({ error: null });


export const logout = (state) => {
  storage.removeToken();
  storage.removeUserId();
  return INITIAL_STATE;
};


export const AuthReducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ERRORS]:     resetErrors,

  [Types.LOGIN_REQUEST]:    request.login,
  [Types.LOGIN_SUCCESS]:    success.login,
  [Types.LOGIN_FAILURE]:    failure,

  [Types.SIGNUP_REQUEST]:   request.signup,
  [Types.SIGNUP_SUCCESS]:   success.signup,
  [Types.SIGNUP_FAILURE]:   failure,

  [Types.LOGOUT_REQUEST]:   request.logout,
  [Types.LOGOUT_SUCCESS]:   logout,
  [Types.LOGOUT_FAILURE]:   failure,
});
