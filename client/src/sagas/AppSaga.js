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


import { delay, eventChannel } from 'redux-saga';
import { call, put, take } from 'redux-saga/effects';


import { AppActions, ChatActions } from 'state';
import Socket, {
  SOCKET_RECONNECT_TIMEOUT,
  SOCKET_NORMAL_CLOSURE_ERROR_CODE,
  SOCKET_NO_STATUS_RECEIVED_ERROR_CODE,
  incrementSocketAttempt } from 'services/Socket';


let channel;


/**
 * Open socket
 * @generator
 */
export function * openSocket () {
  channel = yield call(createChannel, Socket.create());
  while (true) {
    try {
      const action = yield take(channel);
      yield put(action);
    } catch (error) {
      console.error('Encountered unexpected socket close. Reconnecting...');
      yield call(reconnect);
    }
  }
}


/**
 * Close socket
 * @generator
 */
export function * closeSocket () {
  yield channel.close();
}


/**
 * Attempt socket reconnect
 * @generator
 */
export function * reconnect () {
  if (incrementSocketAttempt() === -1)
    yield put(AppActions.socketMaxAttemptsReached());
  yield call(delay, SOCKET_RECONNECT_TIMEOUT);
  yield call(openSocket);
}


/**
 * Create saga channel to communicate with an external
 * WebSocket event source.
 * @param {object} socket WebSocket object
 * @returns {object}
 */
const createChannel = (socket) =>
  eventChannel(emit => {
    socket.onerror = (event) => {
      if (event && event.code === 'ECONNREFUSED') {
        emit(AppActions.socketError(event));
        emit(new Error(event.reason));
      }
    };
    socket.onclose = (event) => {
      if (event.code !== SOCKET_NORMAL_CLOSURE_ERROR_CODE &&
          event.code !== SOCKET_NO_STATUS_RECEIVED_ERROR_CODE) {
        emit(AppActions.socketError(event));
        emit(new Error(event.reason));
      }
    };
    socket.onmessage = (event) => emit(ChatActions.messageReceive(event.data));
    socket.onopen = () => emit(AppActions.socketOpenSuccess(socket));

    return () => {
      socket.close();
      emit(AppActions.socketCloseSuccess(socket));
    };
  });
