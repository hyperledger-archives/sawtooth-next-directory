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


import { all, call, put } from 'redux-saga/effects';
import AuthActions from '../redux/AuthRedux';
import ApproverActions from '../redux/ApproverRedux';
import RequesterActions from '../redux/RequesterRedux';


/**
 *
 * Execute login API request
 *
 * The login generator function executes a request to the
 * API and handles the response.
 *
 * @param action
 *
 */
export function * login (api, action) {
  try {

    const { username, password } = action;
    const res = yield call(api.login, {
      id: username,
      password: password
    });

    if (res.ok) {
      yield put(AuthActions.loginSuccess(true, res.data.data));
    } else {
      alert(res.data.message);
      yield put(AuthActions.loginFailure(res.data.message));
    }

  } catch (err) {
    console.error(err);
  }
}

/**
 *
 * Execute Signup API request
 *
 * The s=Signup generator function executes a request to the
 * API for creating new user and handles the response.
 *
 * @param action
 *
 */

export function * signup (api, action) {
  try {

    const { username, password, name, email } = action;
    const res = yield call(api.signup, {
      username: username,
      password: password,
      email: email,
      name: name
    });

    if (res.ok) {
      yield put(AuthActions.signupSuccess(true, res.data.data));
    } else {
      alert(res.data.message);
      yield put(AuthActions.signupFailure(res.data.message));
    }

  } catch (err) {
    console.error(err);
  }
}

export function * logout (api, action) {
  try {

    const res = yield call(api.logout);
    if (res.ok) {
      yield all([
        put(AuthActions.logoutSuccess()),
        put(ApproverActions.resetAll()),
        put(RequesterActions.resetAll()),
      ]);
    } else {
      alert(res.data.message);
      yield put(AuthActions.logoutFailure(res.data.message));
    }

  } catch (err) {
    console.error(err);
  }
}
