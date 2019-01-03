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


import Actions, { INITIAL_STATE } from './ChatActions';
import { ChatReducer as reducer } from './ChatReducer';


test('clearMessages', () => {
  const state = reducer(INITIAL_STATE, Actions.clearMessages(null));
  expect(state.messages).toBe(null);
});


test('messageSend', () => {
  const argument =  {payload: { message: { text: 'userid' }}};
  const state = reducer(
    INITIAL_STATE,
    Actions.messageSend(argument)
  );
  expect(state.fetching).toBe(true);
});


test('messageReceive', () => {
  const Message = JSON.stringify({ message: { length: 'userid' }});
  const state = reducer(
    INITIAL_STATE,
    Actions.messageReceive(Message)
  );
  expect(state.fetching).toBe(false);
  expect(state.messages).toBe(null);
});
