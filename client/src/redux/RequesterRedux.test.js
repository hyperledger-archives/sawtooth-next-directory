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


import Actions, { reducer, INITIAL_STATE } from './RequesterRedux';


test.skip('baseRequest', () => {
  const state = reducer(INITIAL_STATE, Actions.baseRequest(null));

  expect(state.fetching).toBe(true);
});

test('roleRequest', () => {
  const id = 'abc123';
  const state = reducer(INITIAL_STATE, Actions.roleRequest(id));

  expect(state.fetching).toBe(true);
});




test.skip('baseSuccess', () => {
  const base = { recommended: [] };
  const state = reducer(INITIAL_STATE, Actions.baseSuccess(base));

  expect(state.fetching).toBe(false);
  expect(state.recommended).toEqual([]);
  expect(state.error).toBeNull();
});

test.skip('roleSuccess', () => {
  const activeRole = {};
  const state = reducer(INITIAL_STATE, Actions.roleSuccess(activeRole));

  expect(state.fetching).toBe(false);
  expect(state.activeRole).toEqual({});
  expect(state.error).toBeNull();
});



test.skip('baseFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.baseFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});

test('roleFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.roleFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});
