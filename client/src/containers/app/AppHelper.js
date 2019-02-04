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
  AppActions as App,
  ApproverActions as Approver,
  AuthActions as Auth,
  ChatActions as Chat,
  RequesterActions as Requester,
  UserActions as User,
  AppSelectors,
  ApproverSelectors,
  AuthSelectors,
  ChatSelectors,
  RequesterSelectors,
  UserSelectors } from 'state';


// App-wide selectors
export const appState = (state) => ({

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
  delegations:         ApproverSelectors.delegations(state),
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
  expired:             UserSelectors.expired(state),
  expiredCount:        UserSelectors.expiredCount(state),
  id:                  UserSelectors.id(state),
  me:                  UserSelectors.me(state),
  people:              UserSelectors.people(state),
  peopleTotalCount:    UserSelectors.peopleTotalCount(state),
  users:               UserSelectors.users(state),
  userFromId:          (id) => UserSelectors.userFromId(state, id),
});


// App-wide actions
export const appDispatch = (dispatch) => ({

  // App
  startAnimation:       () => dispatch(App.animationBegin()),
  stopAnimation:        () => dispatch(App.animationEnd()),
  startRefresh:         () => dispatch(App.refreshBegin()),
  stopRefresh:          () => dispatch(App.refreshEnd()),
  forceSocketError:     () => dispatch(App.socketMaxAttemptsReached()),
  sendSocket: (endpoint, payload) =>
    dispatch(App.socketSend(endpoint, payload)),
  openSocket:   (endpoint) => dispatch(App.socketOpen(endpoint)),
  closeSocket:  (endpoint) => dispatch(App.socketClose(endpoint)),
  refreshOnNextSocketReceive: (flag) =>
    dispatch(App.refreshOnNextSocketReceive(flag)),

  // Approver
  approveProposals:  (ids) => dispatch(Approver.approveProposalsRequest(ids)),
  rejectProposals:   (ids) => dispatch(Approver.rejectProposalsRequest(ids)),
  getDelegations:    (ids) => dispatch(Approver.delegationsRequest(ids)),
  getOpenProposals:   (id) => dispatch(Approver.openProposalsRequest(id)),
  createRole:    (payload) => dispatch(Approver.createRoleRequest(payload)),
  createPack:    (payload) => dispatch(Approver.createPackRequest(payload)),
  getOrganization:    (id) => dispatch(Approver.organizationRequest(id)),
  setOnBehalfOf:      (id) => dispatch(Approver.onBehalfOfSet(id)),
  getConfirmedProposals: (id) =>
    dispatch(Approver.confirmedProposalsRequest(id)),
  getRejectedProposals:  (id) =>
    dispatch(Approver.rejectedProposalsRequest(id)),

  // Chat
  getConversation:   (id) => dispatch(Chat.conversationRequest(id)),
  resetChat:           () => dispatch(Chat.clearMessages()),
  sendMessage:  (payload) => {
    dispatch(Chat.messageSend(payload)) &&
      dispatch(App.socketSend('chatbot', payload));
  },

  // Requester
  getBase:             () => dispatch(Requester.baseRequest()),
  getRole:           (id) => dispatch(Requester.roleRequest(id)),
  getRoles:         (ids) => dispatch(Requester.rolesRequest(ids)),
  getPack:           (id) => dispatch(Requester.packRequest(id)),
  getPacks:         (ids) => dispatch(Requester.packsRequest(ids)),
  getProposal:       (id) => dispatch(Requester.proposalRequest(id)),
  manualExpire:      (id) => dispatch(Requester.manualExpire(id)),
  getProposals:     (ids) => dispatch(Requester.proposalsRequest(ids)),
  getAllPacks: (start, limit) =>
    dispatch(Requester.allPacksRequest(start, limit)),
  getAllRoles: (start, limit) =>
    dispatch(Requester.allRolesRequest(start, limit)),
  requestRoleAccess: (id, userId, reason) =>
    dispatch(Requester.roleAccessRequest(id, userId, reason)),
  requestPackAccess: (id, userId, reason) =>
    dispatch(Requester.packAccessRequest(id, userId, reason)),

  // User
  getMe:              () => dispatch(User.meRequest()),
  logout:             () => logout(dispatch),
  getUser:     (id, summary) =>
    dispatch(User.userRequest(id, summary)),
  getUsers:    (ids, summary) =>
    dispatch(User.usersRequest(ids, summary)),
  getPeople:   (start, limit) =>
    dispatch(User.peopleRequest(start, limit)),
});


export const logout = (dispatch) =>
  dispatch(Auth.logoutRequest()) && dispatch(Chat.clearMessages()) &&
  dispatch(User.resetAll()) && dispatch(Requester.resetAll()) &&
  dispatch(Approver.resetAll());
