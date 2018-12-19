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
/*


Auth saga
Each generator function executes a request to the
API to retrieve data required to hydrate the UI. */


import { call, put } from 'redux-saga/effects';
import { showLoading, hideLoading } from 'react-redux-loading-bar';
import AuthActions from '../redux/AuthRedux';


/**
 * Authenticate a user
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * login (api, action) {
  try {
    const { username, password } = action;
    const res = yield call(api.login, {
      id: username,
      password: password,
    });

    res.ok ?
      yield put(AuthActions.loginSuccess(true, res.data.data)) :
      yield put(AuthActions.loginFailure(res.data.message));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Create a new user account
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * signup (api, action) {
  try {
    yield put(showLoading());
    const { username, password, name, email } = action;
    const res = yield call(api.signup, {
      username: username,
      password: password,
      email: email,
      name: name,
    });

    res.ok ?
      yield put(AuthActions.signupSuccess(true, res.data.data)) :
      yield put(AuthActions.signupFailure(res.data.message));
  } catch (err) {
    console.error(err);
  } finally {
    yield put(hideLoading());
  }
}


/**
 * Logout of current session
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * logout (api, action) {
  try {
    const res = yield call(api.logout);
    res.ok ?
      yield put(AuthActions.logoutSuccess()) :
      yield put(AuthActions.logoutFailure(res.data.message));
  } catch (err) {
    console.error(err);
  }
}
