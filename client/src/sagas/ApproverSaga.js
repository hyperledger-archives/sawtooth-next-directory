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
import ApproverActions from '../redux/ApproverRedux';


/**
 *
 * Execute open proposals API request
 *
 * The getOpenProposals generator function executes a request to the
 * API to get open proposals.
 *
 * @param action
 *
 */
export function * getOpenProposals (api, action) {
  try {

    const res = yield call(api.getOpenProposals);
    yield put(ApproverActions.openProposalsSuccess(res.data));

  } catch (err) {
    console.error(err);
  }
}
