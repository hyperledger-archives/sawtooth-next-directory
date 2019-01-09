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


import { put } from 'redux-saga/effects';


import FixtureAPI from 'services/FixtureApi';
import { ApproverActions } from 'state';
import { getOpenProposals, getConfirmedProposals } from 'sagas/ApproverSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test('getOpenProposals: call API', () => {
  const res = { ok: true, data: {} };

  const step = stepper(getOpenProposals(FixtureAPI, {id: ''}));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(ApproverActions.openProposalsSuccess(res.data)));
});


test('getConfirmedProposals: call API', () => {
  const res = { ok: true, data: {} };

  const step = stepper(getConfirmedProposals(FixtureAPI));

  step();

  const stepRes = step(res);
  expect(stepRes)
    .toEqual(put(ApproverActions.confirmedProposalsSuccess(res.data)));
});
