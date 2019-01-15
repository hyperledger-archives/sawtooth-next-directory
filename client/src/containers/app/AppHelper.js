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


import {
  AppActions,
  ApproverActions,
  AuthActions,
  ChatActions,
  RequesterActions,
  UserActions,

  AppSelectors,
  ApproverSelectors,
  AuthSelectors,
  ChatSelectors,
  RequesterSelectors,
  UserSelectors } from 'state';


// App-wide selectors
export const appState = (state) => {
  return {

    // App
    isAnimating:         AppSelectors.isAnimating(state),
    isRefreshing:        AppSelectors.isRefreshing(state),
    isSocketOpen:        (endpoint) =>
      AppSelectors.isSocketOpen(state, endpoint),
    socketMaxAttemptsReached:
      AppSelectors.socketMaxAttemptsReached(state),
    shouldRefreshOnNextSocketReceive:
      AppSelectors.shouldRefreshOnNextSocketReceive(state),

    // Approver
    confirmedProposals:  ApproverSelectors.confirmedProposals(state),
    rejectedProposals:   ApproverSelectors.rejectedProposals(state),
    openProposals:       ApproverSelectors.openProposals(state),
    openProposalsByRole: ApproverSelectors.openProposalsByRole(state),
    openProposalsByUser: ApproverSelectors.openProposalsByUser(state),
    openProposalsCount:  ApproverSelectors.openProposalsCount(state),
    organization:        ApproverSelectors.organization(state),
    onBehalfOf:          ApproverSelectors.onBehalfOf(state),
    ownedPacks:          ApproverSelectors.ownedPacks(state),
    ownedRoles:          ApproverSelectors.ownedRoles(state),
    openProposalFromId:  (id) =>
      ApproverSelectors.openProposalFromId(state, id),

    // Auth
    isAuthenticated:     AuthSelectors.isAuthenticated(state),

    // Chat
    messages:            ChatSelectors.messages(state),
    messagesById:        (id) => ChatSelectors.messagesById(state, id),
    messagesCountById:   (id) => ChatSelectors.messagesCountById(state, id),

    // Requester
    memberOf:            RequesterSelectors.memberOf(state),
    memberAndOwnerOf:    RequesterSelectors.memberAndOwnerOf(state),
    recommendedRoles:    RequesterSelectors.recommendedRoles(state),
    recommendedPacks:    RequesterSelectors.recommendedPacks(state),
    requests:            RequesterSelectors.requests(state),
    packs:               RequesterSelectors.packs(state),
    roles:               RequesterSelectors.roles(state),
    rolesTotalCount:     RequesterSelectors.rolesTotalCount(state),
    browseData:          RequesterSelectors.browseData(state),
    proposalFromId:      (id)  =>
      RequesterSelectors.proposalFromId(state, id),
    proposalsFromIds:    (ids) =>
      RequesterSelectors.proposalsFromIds(state, ids),
    roleFromId:          (id)  => RequesterSelectors.roleFromId(state, id),
    packFromId:          (id)  => RequesterSelectors.packFromId(state, id),

    // User
    id:                  UserSelectors.id(state),
    me:                  UserSelectors.me(state),
    users:               UserSelectors.users(state),
    usersTotalCount:     UserSelectors.usersTotalCount(state),
    userFromId:          (id) => UserSelectors.userFromId(state, id),
  };
};


// App-wide actions
export const appDispatch = (dispatch) => {
  return {

    // App
    startAnimation:    ()    => dispatch(AppActions.animationBegin()),
    stopAnimation:     ()    => dispatch(AppActions.animationEnd()),
    startRefresh:      ()    => dispatch(AppActions.refreshBegin()),
    stopRefresh:       ()    => dispatch(AppActions.refreshEnd()),
    forceSocketError:  ()    => dispatch(AppActions.socketMaxAttemptsReached()),
    sendSocket:        (endpoint, payload) =>
      dispatch(AppActions.socketSend(endpoint, payload)),
    openSocket:        (endpoint) =>
      dispatch(AppActions.socketOpen(endpoint)),
    closeSocket:       (endpoint) =>
      dispatch(AppActions.socketClose(endpoint)),
    refreshOnNextSocketReceive: (flag) =>
      dispatch(AppActions.refreshOnNextSocketReceive(flag)),

    // Approver
    approveProposals:  (ids) =>
      dispatch(ApproverActions.approveProposalsRequest(ids)),
    rejectProposals:   (ids) =>
      dispatch(ApproverActions.rejectProposalsRequest(ids)),
    getOpenProposals:  (id)    =>
      dispatch(ApproverActions.openProposalsRequest(id)),
    getConfirmedProposals: (id) =>
      dispatch(ApproverActions.confirmedProposalsRequest(id)),
    getRejectedProposals:  (id) =>
      dispatch(ApproverActions.rejectedProposalsRequest(id)),
    createRole: (payload) =>
      dispatch(ApproverActions.createRoleRequest(payload)),
    createPack: (payload) =>
      dispatch(ApproverActions.createPackRequest(payload)),
    getOrganization:  (id) =>
      dispatch(ApproverActions.organizationRequest(id)),
    setOnBehalfOf:    (id) =>
      dispatch(ApproverActions.onBehalfOfSet(id)),

    // Chat
    getConversation:   (id)  => dispatch(ChatActions.conversationRequest(id)),
    resetChat:         ()    => dispatch(ChatActions.clearMessages()),
    sendMessage:       (payload) => {
      dispatch(ChatActions.messageSend(payload)) &&
      dispatch(AppActions.socketSend('chatbot', payload));
    },

    // Requester
    getBase:           ()    => dispatch(RequesterActions.baseRequest()),
    getRole:           (id)  => dispatch(RequesterActions.roleRequest(id)),
    getRoles:          (ids) => dispatch(RequesterActions.rolesRequest(ids)),
    getPack:           (id)  => dispatch(RequesterActions.packRequest(id)),
    getPacks:          (ids) => dispatch(RequesterActions.packsRequest(ids)),
    getProposal:       (id)  => dispatch(RequesterActions.proposalRequest(id)),
    getProposals:      (ids) =>
      dispatch(RequesterActions.proposalsRequest(ids)),
    getAllPacks:       (start, limit) =>
      dispatch(RequesterActions.allPacksRequest(start, limit)),
    getAllRoles:       (start, limit) =>
      dispatch(RequesterActions.allRolesRequest(start, limit)),
    requestRoleAccess:     (id, userId, reason) =>
      dispatch(RequesterActions.roleAccessRequest(id, userId, reason)),
    requestPackAccess:     (id, userId, reason) =>
      dispatch(RequesterActions.packAccessRequest(id, userId, reason)),

    // User
    getMe:             ()    => dispatch(UserActions.meRequest()),
    getUser:           (id)  => dispatch(UserActions.userRequest(id)),
    getUsers:          (ids) => dispatch(UserActions.usersRequest(ids)),
    logout:            ()    => logout(dispatch),
    getAllUsers:       (start, limit) =>
      dispatch(UserActions.allUsersRequest(start, limit)),

  };
};


export const logout = (dispatch) => {
  return dispatch(AuthActions.logoutRequest()) &&
    dispatch(ChatActions.clearMessages()) &&
    dispatch(UserActions.resetAll()) &&
    dispatch(RequesterActions.resetAll()) &&
    dispatch(ApproverActions.resetAll());
};
