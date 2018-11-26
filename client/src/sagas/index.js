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
import { all, call, put, take, takeLatest } from 'redux-saga/effects';


import API from '../services/Api';
import FixtureAPI from '../services/FixtureApi';
import Socket from '../services/Socket'


import { ApproverTypes } from '../redux/ApproverRedux';
import { AuthTypes } from '../redux/AuthRedux';
import ChatActions, { ChatTypes } from '../redux/ChatRedux';
import { RequesterTypes } from '../redux/RequesterRedux';
import { UserTypes } from '../redux/UserRedux';


import {
  approveProposals,
  getOpenProposals,
  createRole } from './ApproverSaga';
import {
  requestAccess,
  getBase,
  getRole,
  getRoles,
  getProposal,
  getProposals,
  getAllRoles } from './RequesterSaga';


import { login, signup, logout } from './AuthSaga';
import { getConversation, sendMessage } from './ChatSaga';
import { me, getUser, getUsers } from './UserSaga';


const api = API.create();
const ws = Socket.create();


/**
 *
 * Construct API sagas
 *
 *
 */
export default function * root () {
  yield all([
    sagas(),
    channels(),
  ]);
}


/**
 *
 *
 *
 *
 */
function * channels () {
  const channel = yield call(createChannel);
  while (true) {
    const action = yield take(channel);
    yield put(action);
  }
}


/**
 *
 *
 *
 *
 */
function * sagas () {
  yield all([

    // Approver
    takeLatest(ApproverTypes.OPEN_PROPOSALS_REQUEST, getOpenProposals, api),
    takeLatest(ApproverTypes.CREATE_ROLE_REQUEST, createRole, api),
    takeLatest(ApproverTypes.APPROVE_PROPOSALS_REQUEST, approveProposals, api),

    // Auth
    takeLatest(AuthTypes.LOGIN_REQUEST, login, api),
    takeLatest(AuthTypes.SIGNUP_REQUEST, signup, api),
    takeLatest(AuthTypes.LOGOUT_REQUEST, logout, FixtureAPI),

    // Chat
    takeLatest(ChatTypes.CONVERSATION_REQUEST, getConversation, FixtureAPI),
    takeLatest(ChatTypes.SEND_REQUEST, sendMessage, ws),

    // Requester
    takeLatest(RequesterTypes.BASE_REQUEST, getBase, api),
    takeLatest(RequesterTypes.ROLE_REQUEST, getRole, api),
    takeLatest(RequesterTypes.ROLES_REQUEST, getRoles, api),
    takeLatest(RequesterTypes.ALLROLES_REQUEST, getAllRoles, api),
    takeLatest(RequesterTypes.PROPOSAL_REQUEST, getProposal, api),
    takeLatest(RequesterTypes.PROPOSALS_REQUEST, getProposals, api),
    takeLatest(RequesterTypes.ACCESS_REQUEST, requestAccess, api),

    // User
    takeLatest(UserTypes.ME_REQUEST, me, api),
    takeLatest(UserTypes.USER_REQUEST, getUser, api),
    takeLatest(UserTypes.USERS_REQUEST, getUsers, api),

  ]);
}


/**
 *
 *
 *
 *
 */
const createChannel = () =>
  eventChannel(emitter => {
    ws.onopen = (event) => emitter(ChatActions.socketOpenSuccess())
    ws.onmessage = (event) => emitter(ChatActions.sendSuccess(event.data))
    return () => ws.close();
  });
