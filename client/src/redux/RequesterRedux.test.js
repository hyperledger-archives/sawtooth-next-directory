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


test('baseRequest', () => {
  const state = reducer(INITIAL_STATE, Actions.baseRequest(null));

  expect(state.fetching).toBe(true);
});

test('packRequest', () => {
  const id = 'abc123'
  const state = reducer(INITIAL_STATE, Actions.packRequest(id));

  expect(state.fetching).toBe(true);
});




test('baseSuccess', () => {
  const base = { recommended: [] };
  const state = reducer(INITIAL_STATE, Actions.baseSuccess(base));

  expect(state.fetching).toBe(false);
  expect(state.recommended).toEqual([]);
  expect(state.error).toBeNull();
});

test('packSuccess', () => {
  const activePack = {};
  const state = reducer(INITIAL_STATE, Actions.packSuccess(activePack));

  expect(state.fetching).toBe(false);
  expect(state.activePack).toEqual({});
  expect(state.error).toBeNull();
});



test('baseFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.baseFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});

test('packFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.packFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});
