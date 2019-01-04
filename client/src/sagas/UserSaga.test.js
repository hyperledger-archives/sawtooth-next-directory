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


import FixtureAPI from 'services/FixtureApi';
import { UserActions } from 'state';
import { me, getUser, getAllUsers } from 'sagas/UserSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test('me API', () => {
  const step = stepper(me(FixtureAPI));
  expect(step()).toEqual(call(FixtureAPI.me));
});


test('me success path', () => {
  const res = FixtureAPI.me();
  const step = stepper(me(FixtureAPI, {}));
  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(UserActions.meSuccess(res.data.data)));
});


test('failure path', () => {
  const res = { ok: false, data: {} };
  const step = stepper(me(FixtureAPI, {}));
  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(UserActions.meFailure(res.data.error)));
});


test('getUser API', () => {
  const id = 'hello';
  const step = stepper(getUser(FixtureAPI, { id }));
  expect(step()).toEqual(call(FixtureAPI.getUser, id));
});


test('getUser success path', () => {
  const id = 'hello';
  const res = FixtureAPI.getUser(id);
  const step = stepper(getUser(FixtureAPI, {
    id,
  }));
  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(UserActions.userSuccess(res.data.data)));
});


test('getUser failure path', () => {
  const res = { ok: false, data: {} };
  const id = 'hello';
  const step = stepper(getUser(FixtureAPI, {
    id,
  }));
  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(UserActions.userFailure(res.data.error)));
});


test('getAllUsers success path', () => {
  const res = { ok: true, data: {data: '', paging: { total: 0 }}};
  const start = 1;
  const limit = 10;
  const step = stepper(getAllUsers(FixtureAPI, start, limit));
  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(UserActions.allUsersSuccess(
    res.data.data,
    res.data.paging.total,
  )));
});


test('getAllUsers failure path', () => {
  const res = { ok: false, data: {message: '', data: ''}};
  const start = 1;
  const limit = 10;
  const step = stepper(getAllUsers(FixtureAPI, start, limit));
  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(UserActions.allUsersFailure(
    res.data.message
  )));
});

