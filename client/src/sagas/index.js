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


import { all, takeLatest } from 'redux-saga/effects';


import API from 'services/Api';
import FixtureAPI from 'services/FixtureApi';


import {
  AppTypes,
  ApproverTypes,
  AuthTypes,
  ChatTypes,
  RequesterTypes,
  SearchTypes,
  UserTypes } from 'state';
import {
  approveProposals,
  rejectProposals,
  getOpenProposals,
  getConfirmedProposals,
  getRejectedProposals,
  getRelationships,
  createPack,
  createRole,
  checkRoleExists,
  checkPackExists,
  deletePack } from './ApproverSaga';
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
  getAllPacks,
  getAllRoles,
  manualExpire } from './RequesterSaga';


import { closeSocket, openSocket, sendSocket } from './AppSaga';
import { login, signup, logout } from './AuthSaga';
import { getConversation } from './ChatSaga';
import { searchBrowse, searchPeople } from './SearchSaga';
import { editUser, me, getPeople, getUser, getUsers } from './UserSaga';


const api = API.create();


export default function * root () {
  yield sagas();
}


function * sagas () {
  yield all([

    // App
    takeLatest(AppTypes.SOCKET_OPEN, openSocket),
    takeLatest(AppTypes.SOCKET_CLOSE, closeSocket),
    takeLatest(AppTypes.SOCKET_SEND, sendSocket),

    // Approver
    takeLatest(ApproverTypes.OPEN_PROPOSALS_REQUEST, getOpenProposals, api),
    takeLatest(ApproverTypes.CREATE_PACK_REQUEST, createPack, api),
    takeLatest(ApproverTypes.CREATE_ROLE_REQUEST, createRole, api),
    takeLatest(ApproverTypes.DELETE_PACK_REQUEST, deletePack, api),
    takeLatest(ApproverTypes.APPROVE_PROPOSALS_REQUEST, approveProposals, api),
    takeLatest(ApproverTypes.REJECT_PROPOSALS_REQUEST, rejectProposals, api),
    takeLatest(ApproverTypes.ROLE_EXISTS_REQUEST, checkRoleExists, api),
    takeLatest(ApproverTypes.PACK_EXISTS_REQUEST, checkPackExists, api),
    takeLatest(
      ApproverTypes.CONFIRMED_PROPOSALS_REQUEST, getConfirmedProposals, api
    ),
    takeLatest(
      ApproverTypes.REJECTED_PROPOSALS_REQUEST, getRejectedProposals, api
    ),
    takeLatest(
      ApproverTypes.ORGANIZATION_REQUEST, getRelationships, api
    ),

    // Auth
    takeLatest(AuthTypes.LOGIN_REQUEST, login, api),
    takeLatest(AuthTypes.SIGNUP_REQUEST, signup, api),
    takeLatest(AuthTypes.LOGOUT_REQUEST, logout, FixtureAPI),

    // Chat
    takeLatest(ChatTypes.CONVERSATION_REQUEST, getConversation, FixtureAPI),

    // Requester
    takeLatest(RequesterTypes.ALL_PACKS_REQUEST, getAllPacks, api),
    takeLatest(RequesterTypes.ALL_ROLES_REQUEST, getAllRoles, api),
    takeLatest(RequesterTypes.BASE_REQUEST, getBase, FixtureAPI),
    takeLatest(RequesterTypes.PACK_REQUEST, getPack, api),
    takeLatest(RequesterTypes.PACKS_REQUEST, getPacks, api),
    takeLatest(RequesterTypes.ROLE_REQUEST, getRole, api),
    takeLatest(RequesterTypes.ROLES_REQUEST, getRoles, api),
    takeLatest(RequesterTypes.PROPOSAL_REQUEST, getProposal, api),
    takeLatest(RequesterTypes.PROPOSALS_REQUEST, getProposals, api),
    takeLatest(RequesterTypes.PACK_ACCESS_REQUEST, packAccess, api),
    takeLatest(RequesterTypes.ROLE_ACCESS_REQUEST, roleAccess, api),
    takeLatest(RequesterTypes.MANUAL_EXPIRE, manualExpire, api),

    // Search
    takeLatest(SearchTypes.SEARCH_BROWSE_REQUEST, searchBrowse, api),
    takeLatest(SearchTypes.SEARCH_PEOPLE_REQUEST, searchPeople, api),

    // User
    takeLatest(UserTypes.EDIT_USER_REQUEST, editUser, api),
    takeLatest(UserTypes.ME_REQUEST, me, api),
    takeLatest(UserTypes.USER_REQUEST, getUser, api),
    takeLatest(UserTypes.USERS_REQUEST, getUsers, api),
    takeLatest(UserTypes.PEOPLE_REQUEST, getPeople, api),

  ]);
}
