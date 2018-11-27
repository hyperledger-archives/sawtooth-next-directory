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


/**
 *
 * Actions
 *
 * @property request  Initiating action
 * @property success  Action called on execution success
 * @property failure  Action called on execution failure
 *
 */
const { Types, Creators } = createActions({
  conversationRequest:    ['id'],
  conversationSuccess:    ['conversation'],
  conversationFailure:    ['error'],

  sendRequest:            ['message'],
  sendSuccess:            ['message'],
  sendFailure:            ['error'],

  actionSet:              ['action'],
  socketOpenSuccess:      null,
  socketClose:            null,

  clearMessages:          null,
});


export const ChatTypes = Types;
export default Creators;


/**
 *
 * State
 *
 * @property fetching
 * @property error
 *
 */
export const INITIAL_STATE = Immutable({
  fetching:         null,
  error:            null,
  messages:         null,
  action:           null,
  isSocketOpen:     null,
});


/**
 *
 * Selectors
 *
 *
 */
export const ChatSelectors = {
  isSocketOpen: (state) => state.chat.isSocketOpen,
  messages: (state) => state.chat.messages,
  action: (state) => state.chat.action
};


/**
 *
 * Reducers - General
 *
 *
 */
export const request = (state) => {
  return state.merge({ fetching: true });
}
export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
}
export const clearMessages = (state) => {
  return state.merge({ messages: [] });
};


/**
 *
 * Reducers - Success
 *
 *
 */
export const conversationSuccess = (state, { conversation }) => {
  return state.merge({ fetching: false, messages: conversation.messages });
}

export const socketOpenSuccess = (state) => {
  return state.merge({ fetching: false, isSocketOpen: true });
}

export const sendSuccess = (state, { message }) => {
  const parsed = JSON.parse(message)
  return state.merge({
    fetching: false,
    messages: parsed.length !== 0 ?
      (state.messages || []).concat([JSON.parse(message)[0]]) :
      state.messages
  });
}


/**
 *
 * Reducers - Action
 *
 *
 */
export const actionSet = (state, { action }) => {
  return state.merge({ fetching: false, action });
}

export const socketClose = (state) => {
  return state.merge({ fetching: false, isSocketOpen: false });
}


/**
 *
 * Hooks
 *
 *
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.CLEAR_MESSAGES]: clearMessages,

  [Types.CONVERSATION_REQUEST]: request,
  [Types.CONVERSATION_SUCCESS]: conversationSuccess,
  [Types.CONVERSATION_FAILURE]: failure,

  [Types.SEND_REQUEST]: request,
  [Types.SEND_SUCCESS]: sendSuccess,
  [Types.SEND_FAILURE]: failure,

  [Types.ACTION_SET]: actionSet,
  [Types.SOCKET_OPEN_SUCCESS]: socketOpenSuccess,
  [Types.SOCKET_CLOSE]: socketClose,
});
