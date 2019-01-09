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


import { all, call, fork, put, spawn } from 'redux-saga/effects';
import { showLoading, hideLoading } from 'react-redux-loading-bar';
import { RequesterActions, UserActions } from 'state';


/**
 * Get the base data needed to hydrate the UI
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getBase (api, action) {
  try {
    yield put(showLoading());
    const res = yield all([
      call(api.getRecommended),
    ]);
    yield put(RequesterActions.baseSuccess(res));
  } catch (err) {
    console.error(err);
  } finally {
    yield put(hideLoading());
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
    if (ids.length > 0)
      yield all(ids.map(id => spawn(fetchRole, api, id)));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get detailed info for a specific pack
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getPack (api, action) {
  try {
    const { id } = action;
    yield fetchPack(api, id);
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get detailed info for an array of packs
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getPacks (api, action) {
  try {
    const { ids } = action;
    if (ids.length > 0)
      yield all(ids.map(id => spawn(fetchPack, api, id)));
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
export function * getAllRoles (api, action) {
  try {
    const { start, limit } = action;
    const res = yield call(api.getRoles, start, limit);
    if (res.ok) {
      yield put(RequesterActions.allRolesSuccess(
        res.data.data,
        res.data.paging.total),
      );
    } else {
      yield put(RequesterActions.allRolesFailure(res.data.error));
    }

  } catch (err) {
    console.error(err);
  }
}


/**
 * Get all packs
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getAllPacks (api, action) {
  try {
    const { start, limit } = action;
    const res = yield call(api.getPacks, start, limit);
    if (res.ok) {
      yield put(RequesterActions.allPacksSuccess(
        res.data.data,
        res.data.paging.total),
      );
    } else {
      yield put(RequesterActions.allPacksFailure(res.data.error));
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
 * @param {string} action Redux action
 * @generator
 */
export function * roleAccess (api, action) {
  try {
    const { id, userId, reason } = action;
    const res = yield call(api.requestRoleAccess, id, {
      id: userId,
      reason,
    });
    if (res.ok) {
      yield put(RequesterActions.roleAccessSuccess(res.data));
      yield put(UserActions.meRequest());
    } else {
      yield put(RequesterActions.roleAccessFailure(res.data.error));
    }
  } catch (err) {
    console.error(err);
  }
}


/**
 * Send a request to become a member of a pack's roles
 * @param {object} api    API service
 * @param {string} action Redux action
 * @generator
 */
export function * packAccess (api, action) {
  try {
    const { id, userId, reason } = action;
    const res = yield call(api.requestPackAccess, id, {
      id: userId,
      reason,
    });
    if (res.ok) {
      yield put(RequesterActions.packAccessSuccess(res.data));
      yield put(UserActions.meRequest());
    } else {
      yield put(RequesterActions.packAccessFailure(res.data.error));
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
 * Helper for getting detailed info for a specific pack
 * @param {object} api    API service
 * @param {object} id     Pack ID
 * @generator
 */
export function * fetchPack (api, id) {
  try {
    const res = yield call(api.getPack, id);
    res.ok ?
      yield put(RequesterActions.packSuccess(res.data.data)) :
      yield put(RequesterActions.packFailure(res.data.error));
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
      yield put(RequesterActions.proposalFailure(res.data.error));
  } catch (err) {
    console.error(err);
  }
}
