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
import AuthActions from '../redux/AuthRedux';


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
      username: username,
      password: password
    });

    if (res.ok) {
      console.log('Authentication successful.');
      yield put(AuthActions.loginSuccess(true));
    } else {
      alert(res.data.error);
      yield put(AuthActions.loginFailure(res.data.error));
    }
  } catch (err) {
    console.error(err);
  }
}
