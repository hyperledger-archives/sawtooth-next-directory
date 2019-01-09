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


import FixtureAPI from 'services/FixtureApi';
import { ChatActions } from 'state';
import { getConversation } from 'sagas/ChatSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test('chat conversation', () => {
  const id = '490d7d4c-6e07-4795-b785-7a0146d4ec0f';

  const step = stepper(getConversation(FixtureAPI, {
    id,
  }));

  expect(step()).toEqual(call(FixtureAPI.getConversation, id));
});


test('conversation success', () => {
  const id = '490d7d4c-6e07-4795-b785-7a0146d4ec0f';
  const res = FixtureAPI.getConversation(id);

  const step = stepper(getConversation(FixtureAPI, {
    id,
  }));

  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(ChatActions.conversationSuccess(res.data)));

});


test('conversation failure', () => {
  const res = { ok: false, data: {} };
  const id = '';

  const step = stepper(getConversation(FixtureAPI, {
    id,
  }));

  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(ChatActions.conversationFailure(res.data.error)));
});
