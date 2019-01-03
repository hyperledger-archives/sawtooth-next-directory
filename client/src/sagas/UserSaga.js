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


import { all, call, fork, put } from 'redux-saga/effects';
import { UserActions } from 'state';


/**
 * Get detailed info on the currently logged in user
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * me (api, action) {
  try {
    const res = yield call(api.me);
    res.ok ?
      yield put(UserActions.meSuccess(res.data.data)) :
      yield put(UserActions.meFailure(res.data.message));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get detailed info for a specific user or group of
 * users
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getUser (api, action) {
  try {
    const { id } = action;
    const res = yield call(api.getUser, id);
    res.ok ?
      yield put(UserActions.userSuccess(res.data.data)) :
      yield put(UserActions.userFailure(res.data.message));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get detailed info for an array of users
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getUsers (api, action) {
  try {
    const { ids } = action;
    if (ids.length > 0) yield all(ids.map(id => fork(getUser, api, { id })));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get all users in pagination form
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getAllUsers (api, action) {
  try {
    const { start, limit } = action;
    const res = yield call(api.getUsers, start, limit);
    res.ok ?
      yield put(UserActions.allUsersSuccess(
        res.data.data,
        res.data.paging.total)
      ) :
      yield put(UserActions.allUsersFailure(res.data.message));
  } catch (err) {
    console.error(err);
  }
}
