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
import Immutable from 'seamless-immutable';

const UPDATED_STATE = Immutable({
  fetching:           null,
  error:              null,
  openProposals:      [{id: 'openProposalId'}],
  confirmedProposals: null,
});


test('openProposalsRequest', () => {
  const state = reducer(INITIAL_STATE, Actions.openProposalsRequest(null));
  expect(state.fetching).toBe(true);
});


test('openProposalsSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.openProposalsSuccess([]));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('openProposalsFailure', () => {
  const error = '';
  const state = reducer(INITIAL_STATE, Actions.openProposalsFailure(error));

  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});


test('confirmedProposalsSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.confirmedProposalsSuccess([]));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('createRoleSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.createRoleSuccess([]));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('createPackSuccess', () => {
  const state = reducer(INITIAL_STATE, Actions.createPackSuccess([]));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('approveProposalsSuccess', () => {
  const state = reducer(UPDATED_STATE, Actions.approveProposalsSuccess([]));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('rejectProposalsSuccess', () => {
  const state = reducer(UPDATED_STATE, Actions.rejectProposalsSuccess([]));

  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});
