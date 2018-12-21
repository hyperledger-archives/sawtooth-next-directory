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


import { createReducer, createActions } from 'reduxsauce';
import Immutable from 'seamless-immutable';
import ping from '../sounds/ping.mp3';


//
// Actions
//
//
//
//
const { Types, Creators } = createActions({
  conversationRequest:    ['id'],
  conversationSuccess:    ['conversation'],
  conversationFailure:    ['error'],

  messageSend:            ['payload'],
  messageReceive:         ['message'],

  clearMessages:          null,
});


export const ChatTypes = Types;
export default Creators;

//
// State
//
//
//
//
export const INITIAL_STATE = Immutable({
  fetching:         null,
  messages:         null,
  error:            null,
});


//
// Selectors
//
//
//
//
export const ChatSelectors = {
  messages: (state) => state.chat.messages,
};


//
// Reducers
// General
//
//
//
export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
};
export const clearMessages = (state) => {
  return state.merge({ messages: null });
};


//
// Reducers
// Success
//
//
//
export const conversationSuccess = (state, { conversation }) => {
  return state.merge({ fetching: false, messages: conversation.messages });
};

export const messageSend = (state, { payload }) => {
  if (payload.message && payload.message.text.startsWith('/'))
    return state.merge({ fetching: true });
  return state.merge({
    fetching: true,
    messages: payload.do !== 'CREATE' ?
      [payload.message, ...(state.messages || [])] :
      state.messages,
  });
};

export const messageReceive = (state, { message }) => {
  const parsed = JSON.parse(message);

  if (state.messages && state.messages.length > 0) {
    const sound = new Audio(ping);
    sound.play().catch();
  }
  return state.merge({
    fetching: false,
    messages: parsed.length > 0 ?
      [...parsed.reverse(), ...(state.messages || [])] :
      state.messages,
  });
};

//
// Hooks
//
//
//
//
export const reducer = createReducer(INITIAL_STATE, {
  [Types.CLEAR_MESSAGES]: clearMessages,

  // [Types.CONVERSATION_REQUEST]: request,
  // [Types.CONVERSATION_SUCCESS]: conversationSuccess,
  // [Types.CONVERSATION_FAILURE]: failure,

  [Types.MESSAGE_SEND]: messageSend,
  [Types.MESSAGE_RECEIVE]: messageReceive,
});
