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


import Actions, { reducer, INITIAL_STATE } from './ApproverRedux';


test('batchRequest', () => {
  const userId = 'abc123';
  const state = reducer(INITIAL_STATE, Actions.batchRequest(userId));

  expect(state.fetching).toBe(true);
});

test('rolesRequest', () => {
  const userId = 'abc123';
  const state = reducer(INITIAL_STATE, Actions.rolesRequest(userId));

  expect(state.fetching).toBe(true);
});

test('individualsRequest', () => {
  const userId = 'abc123';
  const state = reducer(INITIAL_STATE, Actions.individualsRequest(userId));

  expect(state.fetching).toBe(true);
});

test('frequentRequest', () => {
  const userId = 'abc123';
  const state = reducer(INITIAL_STATE, Actions.frequentRequest(userId));

  expect(state.fetching).toBe(true);
});

test('nearExpiryRequest', () => {
  const userId = 'abc123';
  const state = reducer(INITIAL_STATE, Actions.nearExpiryRequest(userId));

  expect(state.fetching).toBe(true);
});




test('batchSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.batchSuccess(null));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});

test('rolesSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.rolesSuccess(null));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});

test('individualsSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.individualsSuccess(null));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});

test('frequentSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.frequentSuccess(null));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});

test('nearExpirySuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.nearExpirySuccess(null));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});




test('batchFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.batchFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});

test('rolesFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.rolesFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});

test('individualsFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.individualsFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});

test('frequentFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.frequentFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});

test('nearExpiryFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.nearExpiryFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});
