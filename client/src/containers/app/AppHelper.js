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


import AppActions, { AppSelectors } from '../../redux/AppRedux';
import ApproverActions, { ApproverSelectors } from '../../redux/ApproverRedux';
import AuthActions, { AuthSelectors } from '../../redux/AuthRedux';
import ChatActions, { ChatSelectors } from '../../redux/ChatRedux';
import UserActions, { UserSelectors } from '../../redux/UserRedux';
import RequesterActions, {
  RequesterSelectors } from '../../redux/RequesterRedux';


//
// App-wide selectors
//
//
//
//
export const appState = (state) => {
  return {

    // App
    isAnimating:         AppSelectors.isAnimating(state),
    isRefreshing:        AppSelectors.isRefreshing(state),
    isSocketOpen:        AppSelectors.isSocketOpen(state),
    shouldRefreshOnNextSocketReceive:
      AppSelectors.shouldRefreshOnNextSocketReceive(state),

    // Approver
    confirmedProposals:  ApproverSelectors.confirmedProposals(state),
    openProposals:       ApproverSelectors.openProposals(state),
    openProposalsByRole: ApproverSelectors.openProposalsByRole(state),
    openProposalsByUser: ApproverSelectors.openProposalsByUser(state),
    openProposalsCount:  ApproverSelectors.openProposalsCount(state),
    organization:        ApproverSelectors.organization(state),
    openProposalFromId:  (id) =>
      ApproverSelectors.openProposalFromId(state, id),

    // Auth
    isAuthenticated:     AuthSelectors.isAuthenticated(state),

    // Chat
    messages:            ChatSelectors.messages(state),

    // Requester
    mine:                RequesterSelectors.mine(state),
    recommendedRoles:    RequesterSelectors.recommendedRoles(state),
    recommendedPacks:    RequesterSelectors.recommendedPacks(state),
    requests:            RequesterSelectors.requests(state),
    packs:               RequesterSelectors.packs(state),
    roles:               RequesterSelectors.roles(state),
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
    memberOf:            UserSelectors.memberOf(state),
    userFromId:          (id) => UserSelectors.userFromId(state, id),

  };
};


//
// App-wide actions
//
//
//
//
export const appDispatch = (dispatch) => {
  return {

    // App
    startAnimation:    ()    => dispatch(AppActions.animationBegin()),
    stopAnimation:     ()    => dispatch(AppActions.animationEnd()),
    openSocket:        ()    => dispatch(AppActions.socketOpen()),
    closeSocket:       ()    => dispatch(AppActions.socketClose()),
    startRefresh:      ()    => dispatch(AppActions.refreshBegin()),
    stopRefresh:       ()    => dispatch(AppActions.refreshEnd()),
    refreshOnNextSocketReceive: (flag) =>
      dispatch(AppActions.refreshOnNextSocketReceive(flag)),

    // Approver
    approveProposals:  (ids) =>
      dispatch(ApproverActions.approveProposalsRequest(ids)),
    rejectProposals:   (ids) =>
      dispatch(ApproverActions.rejectProposalsRequest(ids)),
    getOpenProposals:  ()    =>
      dispatch(ApproverActions.openProposalsRequest()),
    getConfirmedProposals: () =>
      dispatch(ApproverActions.confirmedProposalsRequest()),
    createRole: (payload) =>
      dispatch(ApproverActions.createRoleRequest(payload)),
    createPack: (payload) =>
      dispatch(ApproverActions.createPackRequest(payload)),
    getOrganization:   (id)    =>
      dispatch(ApproverActions.organizationRequest(id)),

    // Chat
    resetChat:         ()    => dispatch(ChatActions.clearMessages()),
    getConversation:   (id)  => dispatch(ChatActions.conversationRequest(id)),
    sendMessage:       (payload) =>
      dispatch(ChatActions.messageSend(payload)),

    // Requester
    getBase:           ()    => dispatch(RequesterActions.baseRequest()),
    getRole:           (id)  => dispatch(RequesterActions.roleRequest(id)),
    getRoles:          (ids) => dispatch(RequesterActions.rolesRequest(ids)),
    getPack:           (id)  => dispatch(RequesterActions.packRequest(id)),
    getPacks:          (ids) => dispatch(RequesterActions.packsRequest(ids)),
    getProposal:       (id)  => dispatch(RequesterActions.proposalRequest(id)),
    getProposals:      (ids) =>
      dispatch(RequesterActions.proposalsRequest(ids)),
    requestRoleAccess:     (id, userId, reason) =>
      dispatch(RequesterActions.roleAccessRequest(id, userId, reason)),
    requestPackAccess:     (id, userId, reason) =>
      dispatch(RequesterActions.packAccessRequest(id, userId, reason)),

    // User
    getMe:             ()    => dispatch(UserActions.meRequest()),
    getUser:           (id)  => dispatch(UserActions.userRequest(id)),
    getUsers:          (ids) => dispatch(UserActions.usersRequest(ids)),
    logout:            ()    => logout(dispatch),

  };
};


const logout = (dispatch) => {
  return dispatch(AuthActions.logoutRequest()) &&
    dispatch(ChatActions.clearMessages()) &&
    dispatch(UserActions.resetAll()) &&
    dispatch(RequesterActions.resetAll()) &&
    dispatch(ApproverActions.resetAll());
};
