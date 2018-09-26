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


import { put } from 'redux-saga/effects';
import HomeActions from '../redux/RequesterRedux';
import packs from '../mock_data/packs';


/**
 * 
 * Execute pack API request
 * 
 * The getPack generator function executes a request to the
 * API and handles the response.
 * 
 * @param action
 * 
 */
export function * getPack (action) {
  try {
    const { id } = action;
    let pack;

    // Hard-coded mock data
    if (id === '123') {
      pack = packs[0];
    } else {
      pack = { id: id };
    }

    // Default to success for now
    yield put(HomeActions.getPackSuccess(pack));
    console.log('Successfully retrieved pack...');
  } catch (err) {
    console.error(err);
  }
}
