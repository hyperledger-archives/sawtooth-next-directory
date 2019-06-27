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
import { toast } from 'react-toastify';
import { showLoading, hideLoading } from 'react-redux-loading-bar';
import { ApproverActions, UserActions } from 'state';


/**
 * Get currently open proposals
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getOpenProposals (api, action) {
  try {
    const { id } = action;
    const res = yield call(api.getOpenProposals, id);
    res.ok ?
      yield put(ApproverActions.openProposalsSuccess(res.data)) :
      yield put(ApproverActions.openProposalsFailure(res.data));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get confirmed proposals
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getConfirmedProposals (api, action) {
  try {
    const res = yield call(api.getConfirmedProposals);
    res.ok ?
      yield put(ApproverActions.confirmedProposalsSuccess(res.data)) :
      yield put(ApproverActions.confirmedProposalsFailure(res.data));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Get rejected proposals
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getRejectedProposals (api, action) {
  try {
    const res = yield call(api.getRejectedProposals);
    res.ok ?
      yield put(ApproverActions.rejectedProposalsSuccess(res.data)) :
      yield put(ApproverActions.rejectedProposalsFailure(res.data));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Create a new pack
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * createPack (api, action) {
  try {
    const { payload } = action;
    const res = yield call(api.createPack, payload);
    if (res.ok) {
      toast.success('Successfully created a new pack.');
      yield put(ApproverActions.createPackSuccess(res.data.data));
    } else {
      yield put(ApproverActions.createPackFailure(res.data));
    }

  } catch (err) {
    console.error(err);
  }
}


/**
 * Delete a pack
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * deletePack (api, action) {
  try {
    const { id } = action;
    const res = yield call(api.deletePack, id);
    if (res.ok) {
      toast.success('Successfully deleted pack.');
      yield put(ApproverActions.deletePackSuccess(res.data.pack_id));
      yield put(UserActions.meRequest());
    } else {
      yield put(ApproverActions.deletePackFailure(res.data));
    }

  } catch (err) {
    console.error(err);
  }
}


/**
 * Create a new role
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * createRole (api, action) {
  try {
    const { payload } = action;
    const res = yield call(api.createRole, payload);
    if (res.ok) {
      toast.success('Successfully created a new role.');
      yield put(ApproverActions.createRoleSuccess(res.data.data));
    } else {
      yield put(ApproverActions.createRoleFailure(res.data));
    }

  } catch (err) {
    console.error(err);
  }
}


/**
 * Approve an array of proposals
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * approveProposals (api, action) {
  try {
    yield put(showLoading());
    const { ids } = action;
    const res = yield call(api.updateProposals, {
      ids,
      status: 'APPROVED',
      reason: '',
    });
    res.ok ?
      yield put(ApproverActions.approveProposalsSuccess(res.data)) :
      yield put(ApproverActions.approveProposalsFailure(res.data));
  } catch (err) {
    console.error(err);
  } finally {
    yield put(hideLoading());
  }
}


/**
 * Reject an array of proposals
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * rejectProposals (api, action) {
  try {
    yield put(showLoading());
    const { ids } = action;
    const res = yield call(api.updateProposals, {
      ids,
      status: 'REJECTED',
      reason: '',
    });
    res.ok ?
      yield put(ApproverActions.rejectProposalsSuccess(res.data)) :
      yield put(ApproverActions.rejectProposalsFailure(res.data));
  } catch (err) {
    console.error(err);
  } finally {
    yield put(hideLoading());
  }
}


/**
 * Get organization
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getRelationships (api, action) {
  try {
    const { id, isMe } = action;
    const res = yield call(api.getRelationships, id);
    res.ok ?
      yield put(ApproverActions.organizationSuccess(res.data.data, isMe)) :
      yield put(ApproverActions.organizationFailure(res.data));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Check if a role with given name exists
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * checkRoleExists (api, action) {
  try {
    const { name } = action;
    const res = yield call(api.roleExists, name);
    res.ok ?
      yield put(ApproverActions.roleExistsSuccess(res.data.exists)) :
      yield put(ApproverActions.roleExistsFailure(res.data));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Check if a pack with given name exists
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * checkPackExists (api, action) {
  try {
    const { name } = action;
    const res = yield call(api.packExists, name);
    res.ok ?
      yield put(ApproverActions.packExistsSuccess(res.data.exists)) :
      yield put(ApproverActions.packExistsFailure(res.data));
  } catch (err) {
    console.error(err);
  }
}
