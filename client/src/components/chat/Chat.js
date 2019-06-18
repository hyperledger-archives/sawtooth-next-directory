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


import React, { Component } from 'react';
import { connect } from 'react-redux';


import './Chat.css';
import ChatForm from './ChatForm';
import ApproverChat from './ApproverChat';
import RequesterChat from './RequesterChat';
import PeopleChat from './PeopleChat';


import * as storage from 'services/Storage';
import * as sound from 'services/Sound';


// TODO: Consider renaming (sub)component(s)
/**
 *
 * @class         Chat
 * @description   Component encapsulating the chat view
 *
 */
class Chat extends Component {

  /**
   * Called whenever Redux state changes. On socket open, send
   * message to get initial recommendation from chatbot
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const {
      activePack,
      activeRole,
      messages,
      messagesCountById,
      startRefresh,
      refreshOnNextSocketReceive,
      shouldRefreshOnNextSocketReceive } = this.props;

    if (messages !== prevProps.messages) {
      shouldRefreshOnNextSocketReceive && startRefresh();
      refreshOnNextSocketReceive(false);

      const resourceId = (activePack && activePack.id) ||
        (activeRole && activeRole.id);

      if (messages[0] && resourceId && messagesCountById(resourceId) > 2 &&
          messages[0].recipient_id && messages[0].resource_id === resourceId) {
        if (messages[0].text.includes('sent'))
          sound.play('CHAT_REQUEST_SENT');
        else
          sound.play('CHAT_RECEIVE');
      }
    }
  }


  /**
   * Send message to chatbot engine
   * @param {string} message Message body
   */
  send = (message) => {
    const {
      activePack,
      activeRole,
      id,
      sendMessage } = this.props;
    const payload = {
      text: message,
      next_id: id,
      token: storage.getToken(),
      resource_id: (activeRole && activeRole.id) ||
        (activePack && activePack.id),
    };
    sendMessage(payload);
  }


  /**
   * Send manual access request for current role
   * @param {string} message Message body
   */
  manualRequestRole = (message) => {
    const { activeRole, me, requestRoleAccess } = this.props;
    requestRoleAccess(activeRole.id, me.id, message);
  }


  /**
   * Send manual access request for current pack
   * @param {string} message Message body
   */
  manualRequestPack = (message) => {
    const { activePack, me, requestPackAccess } = this.props;
    requestPackAccess(activePack.id, me.id, message);
  }


  /**
   * Approve selected proposals
   */
  manualApprove = () => {
    const { approveProposals, selectedProposals, reset } = this.props;
    approveProposals(selectedProposals);
    reset();
  }


  /**
   * Reject selected proposals
   */
  manualReject = () => {
    const { rejectProposals, selectedProposals, reset } = this.props;
    rejectProposals(selectedProposals);
    reset();
  }


  // * Needed for debugging
  manualErrorTest = () => {
    const { sendMessage } = this.props;
    sendMessage({
      fail: 'yes', do: 'CREATE', message: { text: '/recommend' }, next_id: '?',
    });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      disabled,
      hideButtons,
      hideForm,
      type } = this.props;

    return (
      <div id='next-chat-container'>
        { type === 'APPROVER' &&
          <ApproverChat {...this.props}/>
        }
        { type === 'REQUESTER' &&
          <RequesterChat {...this.props}/>
        }
        { type === 'PEOPLE' &&
          <PeopleChat {...this.props}/>
        }
        { type !== 'PEOPLE' &&
          <div id='next-chat-conversation-dock'>
            <ChatForm
              {...this.props}
              disabled={disabled}
              hideButtons={hideButtons}
              hideForm={hideForm}
              approve={this.manualApprove}
              reject={this.manualReject}
              requestRole={this.manualRequestRole}
              requestPack={this.manualRequestPack}
              send={(message) => this.send(message)}/>
          </div>
        }
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    fetching:             state.chat.fetching,
    socketError:          state.app.socketError,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(Chat);
