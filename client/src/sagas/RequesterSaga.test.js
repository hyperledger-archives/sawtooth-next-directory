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


import { call, put } from 'redux-saga/effects';


import FixtureAPI from '../services/FixtureApi';


import RequesterActions from '../redux/RequesterRedux';
import { getBase, getPack } from '../sagas/RequesterSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test('getBase: first calls API', () => {
  const step = stepper(getBase(FixtureAPI));
  
  expect(step()).toEqual(call(FixtureAPI.getRequesterBase));
});


test('getBase: success path', () => {
  const res = FixtureAPI.getRequesterBase();
  const step = stepper(getBase(FixtureAPI));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(RequesterActions.baseSuccess(res.data)));
});


test('getBase: failure path', () => {
  const res = { ok: false, data: {} };

  const step = stepper(getBase(FixtureAPI));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(RequesterActions.baseFailure(res.data.error)));
});




test('getPack: first calls API', () => {
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const step = stepper(getPack(FixtureAPI, {
    id: id
  }));
  
  expect(step()).toEqual(call(FixtureAPI.getPack, id));
});


test('getPack: success path', () => {
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const res = FixtureAPI.getPack(id);
  const step = stepper(getPack(FixtureAPI, {
    id: id,
  }));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(RequesterActions.packSuccess(res.data)));
});


test('getPack: failure path', () => {
  const res = { ok: false, data: {} };
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const step = stepper(getPack(FixtureAPI, {
    id: id,
  }));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(RequesterActions.packFailure(res.data.error)));
});
