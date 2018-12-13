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
import { delay } from 'redux-saga';
import { all, call, fork, put } from 'redux-saga/effects';
import { toast } from 'react-toastify';

export default function * retryServiceCall (
  request,
  payload,
  successAction,
  failureAction,
  successMessage) {

  let errorMessage = '';

  yield call(delay, 5000);

  try {
    const res = yield call(request, payload);

    if (res.ok) {
      successMessage && toast(successMessage);
      yield put(successAction(res.data));
    }else {
      errorMessage = res.data? res.data.error: res.problem;
      yield put(failureAction(res.data.error));
    }

  } catch(err){
    toast(`${errorMessage}. Please try after sometime.`);
    yield put(failureAction(err));
  }
}
