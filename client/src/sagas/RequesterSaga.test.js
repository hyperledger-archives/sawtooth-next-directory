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


import FixtureAPI from '../services/FixtureApi';
import { call } from 'redux-saga/effects';
import { getBase, getPack } from '../sagas/RequesterSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;

test('getBase: first calls API', () => {
  const step = stepper(getBase(FixtureAPI));
  
  expect(step()).toEqual(call(FixtureAPI.getRequesterBase));
});


test('getPack: first calls API', () => {
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const step = stepper(getPack(FixtureAPI, {
    id: id
  }));
  
  expect(step()).toEqual(call(FixtureAPI.getPack, id));
});
