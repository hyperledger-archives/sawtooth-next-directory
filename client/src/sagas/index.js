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


import { all, takeLatest } from 'redux-saga/effects';


import API from '../services/Api';
import FixtureAPI from '../services/FixtureApi';


import { AppTypes } from '../redux/AppRedux';
import { ApproverTypes } from '../redux/ApproverRedux';
import { AuthTypes } from '../redux/AuthRedux';
import { ChatTypes } from '../redux/ChatRedux';
import { RequesterTypes } from '../redux/RequesterRedux';
import { UserTypes } from '../redux/UserRedux';


import {
  approveProposals,
  rejectProposals,
  getOpenProposals,
  getConfirmedProposals,
  createPack,
  createRole } from './ApproverSaga';
import {
  packAccess,
  roleAccess,
  getBase,
  getRole,
  getRoles,
  getPack,
  getPacks,
  getProposal,
  getProposals,
  getAllRoles } from './RequesterSaga';


import { closeSocket, openSocket } from './AppSaga';
import { login, signup, logout } from './AuthSaga';
import { getConversation, sendMessage } from './ChatSaga';
import { me, getUser, getUsers } from './UserSaga';


const api = API.create();


/**
 *
 * Construct API sagas
 *
 *
 */
export default function * root () {
  yield sagas();
}


/**
 *
 *
 *
 *
 */
function * sagas () {
  yield all([

    // App
    takeLatest(AppTypes.SOCKET_OPEN, openSocket),
    takeLatest(AppTypes.SOCKET_CLOSE, closeSocket),

    // Approver
    takeLatest(ApproverTypes.OPEN_PROPOSALS_REQUEST, getOpenProposals, api),
    takeLatest(ApproverTypes.CREATE_PACK_REQUEST, createPack, api),
    takeLatest(ApproverTypes.CREATE_ROLE_REQUEST, createRole, api),
    takeLatest(ApproverTypes.APPROVE_PROPOSALS_REQUEST, approveProposals, api),
    takeLatest(ApproverTypes.REJECT_PROPOSALS_REQUEST, rejectProposals, api),
    takeLatest(
      ApproverTypes.CONFIRMED_PROPOSALS_REQUEST, getConfirmedProposals, api
    ),

    // Auth
    takeLatest(AuthTypes.LOGIN_REQUEST, login, api),
    takeLatest(AuthTypes.SIGNUP_REQUEST, signup, api),
    takeLatest(AuthTypes.LOGOUT_REQUEST, logout, FixtureAPI),

    // Chat
    takeLatest(ChatTypes.CONVERSATION_REQUEST, getConversation, FixtureAPI),
    takeLatest(ChatTypes.MESSAGE_SEND, sendMessage),

    // Requester
    takeLatest(RequesterTypes.ALL_ROLES_REQUEST, getAllRoles, api),
    takeLatest(RequesterTypes.BASE_REQUEST, getBase, api),
    takeLatest(RequesterTypes.PACK_REQUEST, getPack, api),
    takeLatest(RequesterTypes.PACKS_REQUEST, getPacks, api),
    takeLatest(RequesterTypes.ROLE_REQUEST, getRole, api),
    takeLatest(RequesterTypes.ROLES_REQUEST, getRoles, api),
    takeLatest(RequesterTypes.PROPOSAL_REQUEST, getProposal, api),
    takeLatest(RequesterTypes.PROPOSALS_REQUEST, getProposals, api),
    takeLatest(RequesterTypes.PACK_ACCESS_REQUEST, packAccess, api),
    takeLatest(RequesterTypes.ROLE_ACCESS_REQUEST, roleAccess, api),

    // User
    takeLatest(UserTypes.ME_REQUEST, me, api),
    takeLatest(UserTypes.USER_REQUEST, getUser, api),
    takeLatest(UserTypes.USERS_REQUEST, getUsers, api),

  ]);
}
