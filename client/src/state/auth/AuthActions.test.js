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


import Actions, { INITIAL_STATE } from './AuthActions';
import { AuthReducer as reducer } from './AuthReducer';


test('loginRequest', () => {
  const username = 'hello';
  const password = 'world';
  const state = reducer(INITIAL_STATE,
    Actions.loginRequest(username, password));

  expect(state.fetching).toBe(true);
});


test('loginSuccess', () => {
  const isAuthenticated = true;
  const authData = {
    authorization: '',
    user_id: '',
  };
  const state = reducer(INITIAL_STATE,
    Actions.loginSuccess(isAuthenticated, authData));

  expect(state.fetching).toBe(false);
  expect(state.isAuthenticated).toBe(true);
  expect(state.error).toBeNull();
});


test('loginFailure', () => {
  const error = '';
  const state = reducer(
    INITIAL_STATE,
    Actions.loginFailure(error)
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});


test('logout', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.logoutSuccess(null)
  );
});

