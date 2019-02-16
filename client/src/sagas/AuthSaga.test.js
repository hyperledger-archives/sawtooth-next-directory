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


import { call, put } from 'redux-saga/effects';


import FixtureAPI from 'services/FixtureApi';
import { AuthActions } from 'state';
import { login, signup, logout } from 'sagas/AuthSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test('first calls API', () => {
  const username = 'hello';
  const password = 'world';

  const step = stepper(login(FixtureAPI, {
    username,
    password,
  }));

  expect(step()).toEqual(call(FixtureAPI.login, {
    id: username,
    password,
  }));
});


test('success path', () => {
  const username = 'hello';
  const password = 'world';

  const res = FixtureAPI.login(username, password);
  const step = stepper(login(FixtureAPI, {
    username,
    password,
  }));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.loginSuccess(true)));
});


test('failure path', () => {
  const res = { ok: false, data: {} };

  const username = 'hello';
  const password = 'world';

  const step = stepper(login(FixtureAPI, {
    username,
    password,
  }));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.loginFailure(res.data)));
});

test('signup API', async () => {
  const payload = {
    username: 'hello',
    password: 'world',
    email: 'email@default.com',
    name: 'name',
  };

  const { username, password, email, name } = payload;

  const response = FixtureAPI.signup(username, password, email, name);

  const step = stepper(signup(FixtureAPI, payload));

  step();
  step();
  const stepRes = step(response);
  expect(stepRes).toEqual(put(AuthActions.signupSuccess(true)));
});

test('signup success path', () => {
  const username = 'hello';
  const password = 'world';
  const email = 'email@default.com';
  const name = 'name';

  const res = FixtureAPI.signup(name, username, password, email);
  const step = stepper(signup(FixtureAPI, {
    name,
    username,
    password,
    email,
  }));

  step();
  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.signupSuccess(true)));
});

test('signup failure path', () => {
  const res = { ok: false, data: {} };

  const username = 'hello';
  const password = 'world';
  const email = 'email@default.com';
  const name = 'name';

  const step = stepper(signup(FixtureAPI, {
    username,
    password,
    name,
    email,

  }));

  step();
  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.signupFailure(res.data)));
});

test('logout API', () => {

  const step = stepper(logout(FixtureAPI));
  expect(step()).toEqual(call(FixtureAPI.logout));
});

test('logout success path', () => {

  const res = FixtureAPI.logout();
  const step = stepper(logout(FixtureAPI, {

  }));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.logoutSuccess(true)));
});

test('failure path', () => {

  const res = { ok: false, data: {} };

  const step = stepper(logout(FixtureAPI, {}));

  step();

  const stepRes = step(res);
  expect(stepRes).toEqual(put(AuthActions.logoutFailure(res.data)));
});
