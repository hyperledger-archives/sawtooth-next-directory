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


import Actions, { INITIAL_STATE } from './UserActions';
import { UserReducer as reducer } from './UserReducer';


test('meFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.userFailure(error));
  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});


test('resetAll', () => {
  const state = reducer(INITIAL_STATE, Actions.resetAll(null));
});


test('meSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.meSuccess([]));
  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('userSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.userSuccess([]));
  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});
