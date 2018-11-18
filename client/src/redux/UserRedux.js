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
  resetAll:      null,

  meRequest:     null,
  meSuccess:     ['me'],
  meFailure:     ['error'],

  userRequest:   ['id'],
  userSuccess:   ['user'],
  userFailure:   ['error'],

  usersRequest:  ['ids'],
});


export const UserTypes = Types;
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
  me:               null,
  users:            null,
});


/**
 *
 * Selectors
 *
 *
 */
export const UserSelectors = {
  me:         (state) => state.user.me,
  id:         (state) => state.user.me && state.user.me.id,
  users:      (state) => state.user.users,
  memberOf:   (state) => state.user.me && state.user.me.memberOf,
};


/**
 *
 * Reducers - General
 *
 *
 */
export const request = (state) => {
  return state.merge({ fetching: true });
};
export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
};
export const resetAll = (state) => {
  return INITIAL_STATE;
};


/**
 *
 * Reducers - Success
 *
 *
 */
export const meSuccess = (state, { me }) => {
  return state.merge({
    fetching: false,
    me: me,
    users: utils.merge(state.users || [], [me])
  });
};

export const userSuccess = (state, { user }) => {
  return state.merge({
    fetching: false,
    users: utils.merge(state.users || [], [user])
  });
};


/**
 *
 * Hooks
 *
 *
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]: resetAll,

  [Types.ME_REQUEST]: request,
  [Types.ME_SUCCESS]: meSuccess,
  [Types.ME_FAILURE]: failure,

  [Types.USER_REQUEST]: request,
  [Types.USER_SUCCESS]: userSuccess,
  [Types.USER_FAILURE]: failure,

  [Types.USERS_REQUEST]: request,
});
