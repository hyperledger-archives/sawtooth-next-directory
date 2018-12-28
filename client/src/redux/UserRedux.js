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
import * as storage from 'services/Storage';


//
// Actions
//
//
//
//
const { Types, Creators } = createActions({
  meRequest:       null,
  meSuccess:       ['me'],
  meFailure:       ['error'],

  usersRequest:    ['ids'],
  userRequest:     ['id'],
  userSuccess:     ['user'],
  userFailure:     ['error'],

  allUsersRequest: null,
  allUsersSuccess: ['users'],
  allUsersFailure: ['error'],

  resetAll:        null,
});


export const UserTypes = Types;
export default Creators;

//
// State
//
//
//
//
export const INITIAL_STATE = Immutable({
  fetchingMe:       null,
  fetchingUser:     null,
  fetchingUsers:    null,
  fetchingAllUsers: null,

  error:            null,
  me:               null,
  users:            null,
});

//
// Selectors
//
//
//
//
export const UserSelectors = {
  me:         (state) => state.user.me,
  id:         (state) =>
    (state.user.me && state.user.me.id) || storage.getUserId(),
  users:      (state) => state.user.users,
  memberOf:   (state) => state.user.me && state.user.me.memberOf,
  userFromId: (state, id) =>
    state.user.users &&
    state.user.users.find(user => user.id === id),
};

//
// Reducuers
// General
//
//
//
export const request = {
  allUsers:   (state) => state.merge({ fetchingAllUsers: true }),
  me:         (state) => state.merge({ fetchingMe: true }),
  user:       (state) => state.merge({ fetchingUser: true }),
  users:      (state) => state.merge({ fetchingUsers: true }),
};

export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
};
export const resetAll = (state) => {
  return INITIAL_STATE;
};

//
// Reducuers
// Success
//
//
//
export const success = {
  me: (state, { me }) =>
    state.merge({
      fetching: false,
      me: me,
      users: utils.merge(state.users || [], [me]),
    }),
  user: (state, { user }) =>
    state.merge({
      fetching: false,
      users: utils.merge(state.users || [], [user]),
    }),
  allUsers: (state, { users }) => {
    return state.merge({
      fetchingAllUsers: false,
      users: utils.merge(state.users || [], users),
    });
  },
};

//
// Hooks
//
//
//
//
export const reducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]:          resetAll,

  [Types.ME_REQUEST]:         request.me,
  [Types.ME_SUCCESS]:         success.me,
  [Types.ME_FAILURE]:         failure,

  [Types.USERS_REQUEST]:      request.users,
  [Types.USER_REQUEST]:       request.user,
  [Types.USER_SUCCESS]:       success.user,
  [Types.USER_FAILURE]:       failure,

  [Types.ALL_USERS_REQUEST]:  request.allUsers,
  [Types.ALL_USERS_SUCCESS]:  success.allUsers,
  [Types.ALL_USERS_FAILURE]:  failure,
});
