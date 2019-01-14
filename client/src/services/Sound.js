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


import CHAT_RECEIVE from 'sounds/chat-receive.mp3';
import CHAT_REQUEST_SENT from 'sounds/chat-request-sent.mp3';
import * as utils from 'services/Utils';


const sounds = {
  CHAT_RECEIVE: new Audio(CHAT_RECEIVE),
  CHAT_REQUEST_SENT: new Audio(CHAT_REQUEST_SENT),
};


export const play = (name) => {
  sounds[name].play().catch(error => utils.noop());
};
