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
 * @property request  Initiating action
 * @property success  Action called on execution success
 * @property failure  Action called on execution failure
 *
 */
const { Types, Creators } = createActions({
  meRequest:     null,
  meSuccess:     ['me'],
  meFailure:     ['error'],
  meReset:       null
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
  requests:         null
});


/**
 *
 * Selectors
 *
 *
 */
export const UserSelectors = {
  me: (state) => state.user.me,
  requests: (state) => state.user.me && state.user.me.proposals
};


/**
 *
 * Reducers
 *
 *
 */
export const request = (state) => state.merge({ fetching: true });

export const success = (state, { me }) => {
  return state.merge({
    fetching: false,
    requests: me.proposals,
    me: me
  });
}

export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
}

export const reset = (state) => INITIAL_STATE;


/**
 *
 * Hooks
 *
 *
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.ME_REQUEST]: request,
  [Types.ME_SUCCESS]: success,
  [Types.ME_FAILURE]: failure,
  [Types.ME_RESET]: reset,
});
