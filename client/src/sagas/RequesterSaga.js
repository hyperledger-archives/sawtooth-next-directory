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


Requester saga
Each generator function executes a request to the
API to retrieve data required to hydrate the UI. */


import { all, call, fork, put } from 'redux-saga/effects';
import RequesterActions from '../redux/RequesterRedux';
import UserActions from '../redux/UserRedux';


/**
 * Get the base data needed to hydrate the UI
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
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
 * Get detailed info for a specific role
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getRole (api, action) {
  try {
    const { id } = action;
    yield fetchRole(api, id);
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get detailed info for an array of roles
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getRoles (api, action) {
  try {
    const { ids } = action;
    if (ids.length > 0) yield all(ids.map(id => fork(fetchRole, api, id)));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get all roles
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getAllRoles (api) {
  try {
    const res = yield call(api.getRoles);
    if (res.ok) {
      yield put(RequesterActions.allrolesSuccess(res.data.data));
    } else {
      alert(res.data.error);
      yield put(RequesterActions.allrolesFailure(res.data.error));
    }
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get detailed info for a specific proposa
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getProposal (api, action) {
  try {
    const { id } = action;
    yield fetchProposal(api, id);
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get detailed info for an array of proposals
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getProposals (api, action) {
  try {
    const { ids } = action;
    if (ids.length > 0) yield all(ids.map(id => fork(fetchProposal, api, id)));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Send a request to become a member of a role
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * requestAccess (api, action) {
  try {
    const { id, userId, reason } = action;
    const res = yield call(api.requestAccess, id, {
      id: userId,
      reason: reason,
    });
    if (res.ok) {
      yield put(RequesterActions.accessSuccess(res.data));
      yield put(UserActions.meRequest());
    } else {
      yield put(RequesterActions.accessFailure(res.data.error));
    }
  } catch (err) {
    console.error(err);
  }
}


/**
 * Helper for getting detailed info for a specific role
 * @param {object} api    API service
 * @param {object} id     Role ID
 * @generator
 */
export function * fetchRole (api, id) {
  try {
    const res = yield call(api.getRole, id);
    res.ok ?
      yield put(RequesterActions.roleSuccess(res.data.data)) :
      yield put(RequesterActions.roleFailure(res.data.error));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Helper for getting detailed info for a specific proposal
 * @param {object} api    API service
 * @param {object} id     Proposal ID
 * @generator
 */
export function * fetchProposal (api, id) {
  try {
    const res = yield call(api.getProposal, id);
    res.ok ?
      yield put(RequesterActions.proposalSuccess(res.data.data)) :
      yield put(RequesterActions.proposalFailure(res.data.error))
  } catch (err) {
    console.error(err);
  }
}
