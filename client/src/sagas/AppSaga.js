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


import { delay, eventChannel } from 'redux-saga';
import { call, put, spawn, take } from 'redux-saga/effects';


import {
  AppActions,
  ApproverActions,
  ChatActions,
  RequesterActions,
  UserActions } from 'state';
import Socket, {
  sockets,
  SOCKET_RECONNECT_TIMEOUT,
  SOCKET_NORMAL_CLOSURE_ERROR_CODE,
  SOCKET_NO_STATUS_RECEIVED_ERROR_CODE,
  incrementSocketAttempt } from 'services/Socket';


const channels = {};


/**
 * Open socket
 * @param {object} action Redux action
 * @generator
 */
export function * openSocket (action) {
  const { endpoint } = action;
  channels[endpoint] = yield call(
    createChannel,
    endpoint,
    Socket.create(endpoint),
  );
  yield spawn(observe, endpoint);
}


/**
 * Close socket
 * @param {object} action Redux action
 * @generator
 */
export function * closeSocket (action) {
  const { endpoint } = action;
  yield channels[endpoint].close();
}


/**
 * Attempt socket reconnect
 * @param {string} endpoint Socket endpoint
 * @generator
 */
export function * reconnect (endpoint) {
  if (incrementSocketAttempt() === -1)
    yield put(AppActions.socketMaxAttemptsReached());
  yield call(delay, SOCKET_RECONNECT_TIMEOUT);
  yield put(AppActions.socketOpen(endpoint));
}


/**
 * Observe and handle incoming channel actions
 * @param {string} endpoint Socket endpoint
 * @generator
 */
export function * observe (endpoint) {
  while (true) {
    try {
      const action = yield take(channels[endpoint]);
      yield put(action);
    } catch (error) {
      console.error('Encountered unexpected socket close. Reconnecting...');
      yield call(reconnect, endpoint);
    }
  }
}


/**
 * Create saga channel to communicate with an external
 * WebSocket event source.
 * @param {string} endpoint Socket endpoint
 * @param {object} socket   WebSocket object
 * @returns {object}
 */
const createChannel = (endpoint, socket) =>
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
    socket.onmessage = (event) => {
      const payload = event.data && JSON.parse(event.data);
      emit(AppActions.socketReceive(payload));

      if (endpoint === 'feed') {
        emit(ApproverActions.feedReceive(payload));
        emit(RequesterActions.feedReceive(payload));
        emit(UserActions.feedReceive(payload));
      }
      if (endpoint === 'chatbot')
        emit(ChatActions.messageReceive(payload));
    };
    socket.onopen = () => emit(AppActions.socketOpenSuccess(endpoint));

    return () => {
      socket.close();
      emit(AppActions.socketCloseSuccess(endpoint));
    };
  });


/**
 * Send a message over a given socket
 * @param {object} action Redux action
 * @generator
 */
export function * sendSocket (action) {
  try {
    const { endpoint, payload } = action;
    yield sockets[endpoint].send(JSON.stringify(payload));
  } catch (err) {
    console.error(err);
  }
}
