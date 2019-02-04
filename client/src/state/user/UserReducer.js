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
import { INITIAL_STATE, UserTypes as Types } from './UserActions';
import * as utils from 'services/Utils';


export const request = {
  me:         (state) => state.merge({ fetchingMe: true }),
  people:     (state) => state.merge({ fetchingPeople: true }),
  user:       (state) => state.merge({ fetchingUser: true }),
  users:      (state) => state.merge({ fetchingUsers: true }),
};


export const success = {
  me: (state, { me }) =>
    state.merge({
      fetching: false, me, users: utils.merge(state.users || [], [me]),
    }),
  people: (state, { people, peopleTotalCount }) =>
    state.merge({
      fetchingPeople: false,
      peopleTotalCount,
      people: utils.sort(
        utils.merge(state.people || [], people),
        'name',
      ),
      users: utils.merge(state.users || [], people),
    }),
  user: (state, { user }) =>
    state.merge({
      fetching: false, users: utils.merge(state.users || [], [user]),
    }),
};


export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
};


export const resetAll = (state) => {
  return INITIAL_STATE;
};


export const UserReducer = createReducer(INITIAL_STATE, {
  [Types.RESET_ALL]:          resetAll,

  [Types.ME_REQUEST]:         request.me,
  [Types.ME_SUCCESS]:         success.me,
  [Types.ME_FAILURE]:         failure,

  [Types.USERS_REQUEST]:      request.users,
  [Types.USER_REQUEST]:       request.user,
  [Types.USER_SUCCESS]:       success.user,
  [Types.USER_FAILURE]:       failure,

  [Types.PEOPLE_REQUEST]:     request.people,
  [Types.PEOPLE_SUCCESS]:     success.people,
  [Types.PEOPLE_FAILURE]:     failure,
});
