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
import UserActions from '../redux/UserRedux';


/**
 *
 * Execute me API request
 *
 * The me generator function executes a request to the
 * API and handles the response.
 *
 * TODO: limit iterator to 3 proposals. UI will never display
 * TODO cont'd: more than 3 proposals in nav.
 *
 * @param action
 *
 */
export function * me (api, action) {
  try {

    const res = yield call(api.me);

    if (res.ok) {
      let me = res.data.data;
      yield put(UserActions.meSuccess(me));
    } else {
      alert(res.data.message);
      yield put(UserActions.meFailure(res.data.message));
    }

  } catch (err) {
    console.error(err);
  }
}


/**
 *
 * Execute getUser API request
 *
 * The getUser generator function executes a request to the
 * API and handles the response.
 *
 * @param action
 *
 */
export function * getUser (api, action) {
  try {
    const { id } = action;
    yield get(api, id);
  } catch (err) {
    console.error(err);
  }
}


/**
 *
 * Execute getUsers API request
 *
 * The getUsers generator function executes a request to the
 * API and handles the response.
 *
 * @param action
 *
 */
export function * getUsers (api, action) {
  try {
    const { ids } = action;

    if (ids.length > 0) {
      yield all(ids.map(id => get(api, id)));
    }
  } catch (err) {
    console.error(err);
  }
}


/**
 *
 * Helpers
 *
 *
 */
function * get (api, id) {
  const res = yield call(api.getUser, id);

  if (res.ok) {
    let user = res.data.data;
    yield put(UserActions.userSuccess(user));
  } else {
    alert(res.data.message);
    yield put(UserActions.userFailure(res.data.message));
  }
}
