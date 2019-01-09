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


import Actions, { INITIAL_STATE } from './RequesterActions';
import { RequesterReducer as reducer } from './RequesterReducer';


test('roleSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.roleSuccess([])
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('packSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.packSuccess([])
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('packFailure', () => {
  const error = '';
  const state = reducer(
    INITIAL_STATE,
    Actions.packFailure(error)
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});


test('proposalSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.proposalSuccess([])
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('allrolesSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.allRolesSuccess([])
  );
  expect(state.fetchingAllRoles).toBe(false);
  expect(state.error).toBeNull();
});


test('accessSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.packAccessSuccess([])
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('resetAll', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.resetAll(null)
  );
});

