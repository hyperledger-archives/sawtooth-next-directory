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


import AuthActions from '../redux/AuthRedux';
import { login } from '../sagas/AuthSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test.skip('first calls API', () => {
  const username = 'hello';
  const password = 'world';

  const step = stepper(login(FixtureAPI, {
    username: username,
    password: password
  }));

  expect(step()).toEqual(call(FixtureAPI.login, {
    id: username,
    password: password
  }));
});


test.skip('success path', () => {
  const username = 'hello';
  const password = 'world';

  const res = FixtureAPI.login(username, password);
  const step = stepper(login(FixtureAPI, {
    username: username,
    password: password
  }));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.loginSuccess(true)));
});


test.skip('failure path', () => {
  const res = { ok: false, data: {} };

  const username = 'hello';
  const password = 'world';

  const step = stepper(login(FixtureAPI, {
    username: username,
    password: password
  }));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.loginFailure(res.data.error)));
});
