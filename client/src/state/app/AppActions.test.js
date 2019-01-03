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


import Actions, { INITIAL_STATE } from './AppActions';
import { AppReducer as reducer } from './AppReducer';


test('animationBegin', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.animationBegin(null)
  );
  expect(state.isAnimating).toBe(true);
});


test('animationEnd', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.animationEnd(null)
  );
  expect(state.isAnimating).toBe(false);
});


test('socketOpenSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.socketOpenSuccess(null)
  );
  expect(state.isSocketOpen).toBe(true);
});


test('socketCloseSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.socketCloseSuccess(null)
  );
  expect(state.isSocketOpen).toBe(false);
});


test('refreshBegin', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.refreshBegin(null)
  );
  expect(state.isRefreshing).toBe(true);
});


test('refreshEnd', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.refreshEnd(null)
  );
  expect(state.isRefreshing).toBe(false);
});


test('socketError', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.socketError(null)
  );
  expect(state.error).toBeNull();
});


test('socketOpen', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.socketOpen(null)
  );
});


test('socketClose', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.socketClose(null)
  );
});


test('refreshOnNextSocketReceive', () => {
  const flag = '';
  const state = reducer(
    INITIAL_STATE,
    Actions.refreshOnNextSocketReceive(flag)
  );
});
