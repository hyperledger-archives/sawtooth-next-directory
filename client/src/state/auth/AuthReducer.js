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
import { INITIAL_STATE, AuthTypes as Types } from './AuthActions';
import * as storage from 'services/Storage';


export const request = (state) =>
  state.merge({ fetching: true, error: false });


export const success = (state, { isAuthenticated, payload }) => {
  payload.user ?
    storage.setUserId(payload.user.id) :
    storage.setUserId(payload.user_id);
  return state.merge({
    isAuthenticated,
    fetching: false,
    user: payload.user,
  });
};


export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
};


export const logout = (state) => {
  storage.removeToken();
  storage.removeUserId();
  return INITIAL_STATE;
};


export const AuthReducer = createReducer(INITIAL_STATE, {
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
