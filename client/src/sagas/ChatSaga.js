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


Chat saga
Each generator function executes a request to the
API to retrieve data required to hydrate the UI. */


import { call, put } from 'redux-saga/effects';
import ChatActions from '../redux/ChatRedux';
import { socket } from '../services/Socket';


/**
 * Get a conversation
 * @param {object} api    API service
 * @param {object} action Redux action
 * @generator
 */
export function * getConversation (api, action) {
  try {
    const { id } = action;
    const res = yield call(api.getConversation, id);
    if (res.ok)
      yield put(ChatActions.conversationSuccess(res.data));
    else
      yield put(ChatActions.conversationFailure(res.data.error));

  } catch (err) {
    console.error(err);
  }
}


/**
 * Send a message to the chatbot engine
 * @param {object} action Redux action
 * @generator
 */
export function * sendMessage (action) {
  try {
    const { payload } = action;
    yield socket.send(JSON.stringify(payload));
  } catch (err) {
    console.error(err);
  }
}
