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


export let socket;


export const SOCKET_RECONNECT_TIMEOUT = 1e3;
export const SOCKET_NORMAL_CLOSURE_ERROR_CODE = 1e3;
export const SOCKET_NO_STATUS_RECEIVED_ERROR_CODE = 1005;


const MAX_ATTEMPTS = 5;
let attempt = 0;


const create = () =>
  socket = new WebSocket(
    (process.env.REACT_APP_WS_PROTOCOL || 'ws://') +
    (process.env.REACT_APP_SERVER_HOST || 'localhost') + ':' +
    (process.env.REACT_APP_SERVER_PORT || '8000') + '/api/chatbot'
  );


export const incrementSocketAttempt = () => {
  return attempt >= MAX_ATTEMPTS ?
    attempt = -1 :
    ++attempt;
};


export default {
  create,
};
