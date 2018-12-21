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


Approver saga
Each generator function executes a request to the
API to retrieve data required to hydrate the UI. */


import { all, call, fork, put } from 'redux-saga/effects';
import ApproverActions from '../redux/ApproverRedux';
import { toast } from 'react-toastify';


/**
 * Get currently open proposals
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getOpenProposals (api, action) {
  try {
    const res = yield call(api.getOpenProposals);
    yield put(ApproverActions.openProposalsSuccess(res.data));
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
    yield put(ApproverActions.confirmedProposalsSuccess(res.data));
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
      toast('Successfully created a new pack.');
      yield put(ApproverActions.createPackSuccess(res.data));
    } else {
      yield put(ApproverActions.createPackFailure(res.data));
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
      toast('Successfully created a new role.');
      yield put(ApproverActions.createRoleSuccess(res.data));
    } else {
      yield put(ApproverActions.createRoleFailure(res.data.error));
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
    const { ids } = action;
    if (ids.length > 0)
      yield all(ids.map(id => fork(approveProposal, api, id)));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Approve a single proposal
 * @param {object} api    API service
 * @param {object} id     Proposal ID
 * @generator
 */
export function * approveProposal (api, id) {
  try {
    const res = yield call(api.approveProposals, id, {
      status: 'APPROVED',
      reason: '',
    });
    res.ok ?
      yield put(ApproverActions.approveProposalsSuccess(res.data)) :
      yield put(ApproverActions.approveProposalsFailure(res.data.error));
  } catch (err) {
    console.error(err);
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
    const { ids } = action;
    if (ids.length > 0)
      yield all(ids.map(id => fork(rejectProposal, api, id)));
  } catch (err) {
    console.error(err);
  }
}


/**
 * Reject a single proposal
 * @param {object} api    API service
 * @param {object} id     Proposal ID
 * @generator
 */
export function * rejectProposal (api, id) {
  try {
    const res = yield call(api.approveProposals, id, {
      status: 'REJECTED',
      reason: '',
    });
    res.ok ?
      yield put(ApproverActions.rejectProposalsSuccess(res.data)) :
      yield put(ApproverActions.rejectProposalsFailure(res.data.error));
  } catch (err) {
    console.error(err);
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
    const { id } = action;
    const res = yield call(api.getRelationships, id);
    res.ok ?
      yield put(ApproverActions.organizationSuccess(res.data)) :
      yield put(ApproverActions.organizationFailure(res.data.error));
  } catch (err) {
    console.error(err);
  }
}
