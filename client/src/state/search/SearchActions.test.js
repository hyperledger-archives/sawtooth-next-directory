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


import Actions, { INITIAL_STATE } from './SearchActions';
import { SearchReducer as reducer } from './SearchReducer';


test('searchBrowseSuccess', () => {
  const state = reducer(
    INITIAL_STATE,
    Actions.searchBrowseSuccess([])
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBeNull();
});


test('searchBrowseFailure', () => {
  const error = '';
  const state = reducer(
    INITIAL_STATE,
    Actions.searchBrowseFailure(error)
  );
  expect(state.fetching).toBe(false);
  expect(state.error).toBe('');
});
