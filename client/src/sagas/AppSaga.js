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


import { eventChannel } from 'redux-saga';
import { call, put, take } from 'redux-saga/effects';
import AppActions from '../redux/AppRedux';
import ChatActions from '../redux/ChatRedux';
import Socket from '../services/Socket';


let channel;


export function * openSocket () {
  channel = yield call(createChannel, Socket.create());
  while (true) {
    const action = yield take(channel);
    yield put(action);
  }
}


export function * closeSocket () {
  yield channel.close();
}


const createChannel = (socket) =>
  eventChannel(emit => {
    socket.onerror = (event) => emit(AppActions.socketError(event));
    socket.onmessage = (event) => emit(ChatActions.messageReceive(event.data));
    socket.onopen = () => emit(AppActions.socketOpenSuccess(socket));

    return () => {
      socket.close();
      emit(AppActions.socketCloseSuccess(socket));
    };
  });
