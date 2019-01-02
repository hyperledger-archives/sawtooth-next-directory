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


import { combineReducers } from 'redux';
import { loadingBarReducer } from 'react-redux-loading-bar';


import { AppReducer } from './app/AppReducer';
import { ApproverReducer } from './approver/ApproverReducer';
import { AuthReducer } from './auth/AuthReducer';
import { ChatReducer } from './chat/ChatReducer';
import { RequesterReducer } from './requester/RequesterReducer';
import { UserReducer } from './user/UserReducer';


export { default as AppActions, AppTypes } from './app/AppActions';
export { AppReducer } from './app/AppReducer';
export { AppSelectors } from './app/AppSelectors';


export {
  default as ApproverActions,
  ApproverTypes } from './approver/ApproverActions';
export { ApproverReducer } from './approver/ApproverReducer';
export { ApproverSelectors } from './approver/ApproverSelectors';


export { default as AuthActions, AuthTypes } from './auth/AuthActions';
export { AuthReducer } from './auth/AuthReducer';
export { AuthSelectors } from './auth/AuthSelectors';


export { default as ChatActions, ChatTypes } from './chat/ChatActions';
export { ChatReducer } from './chat/ChatReducer';
export { ChatSelectors } from './chat/ChatSelectors';


export {
  default as RequesterActions,
  RequesterTypes } from './requester/RequesterActions';
export { RequesterReducer } from './requester/RequesterReducer';
export { RequesterSelectors } from './requester/RequesterSelectors';


export { default as UserActions, UserTypes } from './user/UserActions';
export { UserReducer } from './user/UserReducer';
export { UserSelectors } from './user/UserSelectors';


const reducers = combineReducers({
  app:        AppReducer,
  approver:   ApproverReducer,
  auth:       AuthReducer,
  chat:       ChatReducer,
  requester:  RequesterReducer,
  user:       UserReducer,
  loadingBar: loadingBarReducer,
});


export default reducers;
