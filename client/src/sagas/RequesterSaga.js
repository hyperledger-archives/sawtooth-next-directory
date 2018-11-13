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
import RequesterActions from '../redux/RequesterRedux';
import UserActions from '../redux/UserRedux';


/**
 *
 * Execute base API request
 *
 * The getBase generator function executes a request to the
 * API to retrieve base data required to hydrate the landing screen.
 *
 * @param action
 *
 */
export function * getBase (api, action) {
  try {
    const res = yield call(api.getRoles);
    yield put(RequesterActions.baseSuccess(res.data.data));
  } catch (err) {
    console.error(err);
  }
}


/**
 *
 * Execute role API request
 *
 * The getRole generator function executes a request to the
 * API and handles the response.
 *
 * @param action
 *
 */
export function * getRole (api, action) {
  try {
    const { id } = action;
    yield get(api, id);
  } catch (err) {
    console.error(err);
  }
}


/**
 *
 * Execute roles API request
 *
 * The getRoles generator function executes a request to the
 * API and handles the response.
 *
 * @param action
 *
 */
export function * getRoles (api, action) {
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
 * Execute proposal API request
 *
 * The getProposal generator function executes a request to the
 * API and handles the response.
 *
 * @param action
 *
 */
export function * getProposal (api, action) {
  try {
    const { id } = action;
    const res = yield call(api.getProposal, id);

    if (res.ok) {
      yield put(RequesterActions.proposalSuccess(res.data.data));
    } else {
      alert(res.data.error);
      yield put(RequesterActions.proposalFailure(res.data.error));
    }
  } catch (err) {
    console.error(err);
  }
}


/**
 *
 * Execute request access API request
 *
 * The requestAccess generator function executes a request to the
 * API and handles the response.
 *
 * @param action
 *
 */
export function * requestAccess (api, action) {
  try {
    const { id, userId, reason } = action;
    const res = yield call(api.requestAccess, id, {
      id: userId,
      reason: reason
    });

    if (res.ok) {
      console.log('Requested access');
      yield put(RequesterActions.accessSuccess(res.data));
      yield put(UserActions.meRequest());
    } else {
      alert(res.data.error);
      yield put(RequesterActions.accessFailure(res.data.error));
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
export function * get (api, id) {
  try {
    const res = yield call(api.getRole, id);

    if (res.ok) {
      yield put(RequesterActions.roleSuccess(res.data.data));
    } else {
      alert(res.data.error);
      yield put(RequesterActions.roleFailure(res.data.error));
    }
  } catch (err) {
    console.error(err);
  }
}
