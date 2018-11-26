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
import { Checkbox, Header, List, Icon, Image, Segment, Transition } from 'semantic-ui-react';


import './Chat.css';
import ChatForm from '../forms/ChatForm';
import ChatMessage from './ChatMessage';


import chatRequester from '../../mock_data/conversation_action.json';
import chatApprover from '../../mock_data/conversation_action.1.json';


/**
 *
 * @class Chat
 * Component encapsulating the chat widget
 *
 * TODO: Normalize all JSON objects behind a schema
 * TODO: Break out into child components
 *
 */
export default class Chat extends Component {

  roleName = (roleId) => {
    const { roleFromId } = this.props;
    const role = roleFromId(roleId);
    return role && role.name;
  };


  userName = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    return user && user.name;
  };


  send (message, action) {
    const {
      activeRole,
      approveProposals,
      me,
      requestAccess,
      reset,
      selectedProposals,
      sendMessage,
      type } = this.props;

    if (action) {
      switch (action.type) {
        case 0:
          if (type === 0) {
            sendMessage('foobar');
            requestAccess(activeRole.id, me.id, 'some reason');
          } else if (type === 1) {
            approveProposals(selectedProposals);
            reset();
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
      disabled,
      handleChange,
      selectedRoles,
      selectedUsers,
      subtitle,
      title,
      groupBy,
      type } = this.props;

    // ! Temporary
    const actions = type ? chatApprover.actions :
      chatRequester.actions;

    return (
      <div id='next-chat-container'>

        { type === 0 && title &&
          <Header id='next-chat-header' size='small' inverted>
            {title}
            <Icon link name='pin' size='mini' className='pull-right'/>
          </Header>
        }

        { type === 1 && selectedUsers &&
          <div id='next-chat-selection-heading-container'>
            <Transition.Group
              as={List}
              horizontal
              animation='fade right'
              duration={{hide: 0, show: 1000}}>
              { selectedUsers.map(user => (
                <Image
                  key={user}
                  size='tiny'
                  className='pull-left'
                  src='http://i.pravatar.cc/150'
                  avatar/>
              )) }
            </Transition.Group>
            <Transition
              visible={selectedUsers.length > 0}
              animation='fade left'
              duration={{hide: 0, show: 300}}>
              <Header as='h3' inverted>
                {selectedUsers.length === 1 && title}
                <Header.Subheader>{subtitle}</Header.Subheader>
              </Header>
            </Transition>
          </div>
        }

        { type === 1 && groupBy === 0 && selectedUsers &&
          <div id='next-chat-users-selection-container'>
            <Transition.Group
              as={List}
              animation='fade down'
              duration={{hide: 300, show: 300}}>
              { selectedUsers.map(user => (
                <Segment className='minimal' padded='very' key={user}>
                  <Checkbox
                    checked={!!user}
                    user={user}
                    label={this.userName(user)}
                    onChange={handleChange}/>
                </Segment>
              )) }
            </Transition.Group>
          </div>
        }

        { type === 1 && groupBy === 1 && selectedRoles &&
          <div id='next-chat-roles-selection-container'>
            <Transition.Group
              as={List}
              animation='fade down'
              duration={{hide: 300, show: 300}}>
              { [...new Set(selectedRoles)].map(role => (
                <Segment className='minimal' padded='very' key={role}>
                  <Checkbox
                    checked={!!role}
                    role={role}
                    label={this.roleName(role)}
                    onChange={handleChange}/>
                </Segment>
              )) }
            </Transition.Group>
          </div>
        }

        { type === 0 &&
          <div id='next-chat-messages-container'>
            <ChatMessage {...this.props}/>
          </div>
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
