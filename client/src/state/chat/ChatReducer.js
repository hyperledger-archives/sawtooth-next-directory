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


import { createReducer } from 'reduxsauce';
import { INITIAL_STATE, ChatTypes as Types } from './ChatActions';


export const failure = (state, { error }) =>
  state.merge({ fetching: false, error });


export const clearMessages = (state) =>
  state.merge({ messages: null });


export const conversationSuccess = (state, { conversation }) =>
  state.merge({
    fetching: false,
    messages: conversation.messages,
  });


export const messageSend = (state, { payload }) => {
  if (payload.text && payload.text.startsWith('/update'))
    return state.merge({});
  else if (payload.text && payload.text.startsWith('/'))
    return state.merge({ fetching: true });

  return state.merge({
    fetching: true,
    messages: [payload, ...(state.messages || [])],
  });
};


export const messageReceive = (state, { payload }) =>
  payload[0] && payload[0].text.includes('/noop') ?
    state.merge({}) :
    state.merge({
      fetching: false,
      messages: payload.length > 0 ?
        [...payload.reverse(), ...(state.messages || [])] :
        state.messages,
    });


export const ChatReducer = createReducer(INITIAL_STATE, {
  [Types.CLEAR_MESSAGES]:      clearMessages,
  [Types.MESSAGE_SEND]:        messageSend,
  [Types.MESSAGE_RECEIVE]:     messageReceive,

  // [Types.CONVERSATION_REQUEST]: request,
  // [Types.CONVERSATION_SUCCESS]: conversationSuccess,
  // [Types.CONVERSATION_FAILURE]: failure,
});
