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


import ApproverActions, { ApproverSelectors } from '../../redux/ApproverRedux';
import AuthActions, { AuthSelectors } from '../../redux/AuthRedux';
import ChatActions, { ChatSelectors } from '../../redux/ChatRedux';
import RequesterActions, { RequesterSelectors } from '../../redux/RequesterRedux';
import UserActions, { UserSelectors } from '../../redux/UserRedux';


/**
 *
 *
 *
 * @param {*} state
 *
 *
 */
export const appState = (state) => {
  return {

    // Approver
    openProposals:      ApproverSelectors.openProposals(state),

    // Auth
    isAuthenticated:    AuthSelectors.isAuthenticated(state),

    // Chat
    messages:           ChatSelectors.messages(state),

    // Requester
    activeProposal:     RequesterSelectors.activeProposal(state),
    activeRole:         RequesterSelectors.activeRole(state),
    recommended:        RequesterSelectors.recommended(state),

    // User
    me:                 UserSelectors.me(state),
    requests:           UserSelectors.requests(state),
    users:              UserSelectors.users(state),

  };
};


/**
 *
 *
 *
 * @param {*} dispatch
 *
 *
 */
export const appDispatch = (dispatch) => {
  return {

    // Approver
    getOpenProposals:  ()    => dispatch(ApproverActions.openProposalsRequest()),

    // Chat
    getConversation:   (id)  => dispatch(ChatActions.conversationRequest(id)),
    sendMessage:       (message) => {
      return dispatch(ChatActions.sendRequest(message))
    },

    // Requester
    getBase:           ()    => dispatch(RequesterActions.baseRequest()),
    getRole:           (id)  => dispatch(RequesterActions.roleRequest(id)),
    getProposal:       (id)  => dispatch(RequesterActions.proposalRequest(id)),
    requestAccess:     (id, userId, reason) => {
      return dispatch(RequesterActions.accessRequest(id, userId, reason))
    },

    // User
    getMe:             ()    => dispatch(UserActions.meRequest()),
    getUser:           (id)  => dispatch(UserActions.userRequest(id)),
    logout:            ()    => logout(dispatch),

  };
}


/**
 *
 *
 *
 */
const logout = (dispatch) => {
  return dispatch(AuthActions.logoutRequest()) &&
    dispatch(UserActions.meReset());
}
