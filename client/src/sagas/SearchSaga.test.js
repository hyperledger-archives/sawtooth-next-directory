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


import { put } from 'redux-saga/effects';


import FixtureAPI from 'services/FixtureApi';
import { SearchActions } from 'state';
import { searchBrowse } from 'sagas/SearchSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test('browse: success path', () => {
  const query = {
    query: {
      search_input: 'a',
      page: 1,
    },
  };

  const res = FixtureAPI.search(query);
  const step = stepper(searchBrowse(FixtureAPI, query));

  step();
  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(
    put(SearchActions.searchBrowseSuccess(res.data.data))
  );
});


test('browse: failure path', () => {
  const query = {
    query: {
      search_input: 'a',
      page: NaN,
    },
  };

  const res = { ok: false, data: {} };
  const step = stepper(searchBrowse(FixtureAPI, query));

  step();
  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(
    put(SearchActions.searchBrowseFailure(res.data.error))
  );
});
