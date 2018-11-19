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


import React, { Component } from 'react';
import { Header, Icon, Image, Segment } from 'semantic-ui-react';


import './Chat.css';
import ChatForm from '../forms/ChatForm';
import ChatMessage from './ChatMessage';
import * as utils from '../../services/Utils';


import chatRequester from '../../mock_data/conversation_action.json';
import chatApprover from '../../mock_data/conversation_action.1.json';


/**
 *
 * @class Chat
 * Component encapsulating the chat widget
 *
 * TODO: Normalize all JSON objects behind a schema
 *
 */
export default class Chat extends Component {

  /**
   *
   * Switch chat context when active pack changes
   *
   */
  componentWillReceiveProps (newProps) {
    const { activeRole, getConversation } = this.props;

    if (newProps.activeRole !== activeRole) {
      getConversation(newProps.activeRole['conversation_id']);
    }
  }


  roleName = (roleId) => {
    const { roleFromId } = this.props;
    const role = roleFromId(roleId);

    return role && role.name;
  };


  send (message, action) {
    const {
      activeRole,
      approveProposals,
      history,
      me,
      requestAccess,
      selectedProposals,
      type } = this.props;

    if (action) {
      switch (action.type) {
        case 0:
          if (type === 0) {
            requestAccess(activeRole.id, me.id, 'some reason');
            const slug = utils.createSlug(activeRole.name);
            history.push(`/requests/${slug}`);
          }
          if (type === 1) {
            approveProposals(selectedProposals);
          }
          break;

        case 1:
          alert('Cancel');
          break;

        default:
          break;
      }
    }
  }


  render () {
    const {
      messages,
      selectedRoles,
      selectedUsers,
      title,
      disabled,
      type } = this.props;

    // ! Temporary
    const actions = type ? chatApprover.actions :
      chatRequester.actions;

    return (
      <div id='next-chat-container'>
        { title &&
          <Header id='next-chat-header' size='small' inverted>
            {title}
            <Icon link name='pin' size='mini' className='pull-right'/>
          </Header>
        }
        {
          selectedUsers &&
          <div id='next-chat-users-selection-container'>
          { selectedUsers.map(user => (
            <Image key={user} src='http://i.pravatar.cc/300' avatar/>
          )) }
          </div>
        }
        { selectedRoles &&
          <div id='next-chat-roles-selection-container'>
          { selectedRoles.map(role => (
            <Segment key={role}>
              { this.roleName(role) }
              {/* <Checkbox
                checked={!!role}
                role={role}
                label={this.roleName(role)}
                onChange={handleProposalChange}/> */}
            </Segment>
          )) }
          </div>
        }
        { messages &&
          <ChatMessage {...this.props}/>
        }

        <div id='next-chat-conversation-dock'>
          <ChatForm
            disabled={disabled}
            actions={actions}
            submit={(message, action) => this.send(message, action)}/>
        </div>
      </div>
    );
  }

}
