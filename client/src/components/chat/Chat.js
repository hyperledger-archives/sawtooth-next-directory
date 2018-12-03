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
/*

Chat
Component encapsulating the chat view */


import React, { Component } from 'react';
import {
  Button,
  Checkbox,
  Header,
  List,
  Icon,
  Image,
  Segment,
  Transition } from 'semantic-ui-react';


import './Chat.css';
import ChatForm from '../forms/ChatForm';
import ChatMessage from './ChatMessage';


import chatRequester from '../../mock_data/conversation_action.json';
import chatApprover from '../../mock_data/conversation_action.1.json';


// TODO: Break out into child components
export default class Chat extends Component {

  componentDidMount () {
    const { id, isSocketOpen, messages, sendMessage, type } = this.props;

    if (type === 0 &&
        isSocketOpen &&
        !messages) {
      sendMessage({
        do: 'CREATE', message: { text: '/recommend' }, user_id: id,
      });
    }
  }


  componentDidUpdate (prevProps) {
    const {
      id,
      isSocketOpen,
      messages,
      sendMessage,
      startRefresh,
      type,
      refreshOnNextSocketReceive,
      shouldRefreshOnNextSocketReceive } = this.props;

    if (prevProps.isSocketOpen !== isSocketOpen &&
        type === 0 &&
        isSocketOpen &&
        !messages) {
      sendMessage({
        do: 'CREATE', message: { text: '/recommend' }, user_id: id,
      });
    }

    if (messages !== prevProps.messages) {
      shouldRefreshOnNextSocketReceive && startRefresh();
      refreshOnNextSocketReceive(false);
    }
  }


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


  send (message) {
    const { id, sendMessage } = this.props;
    sendMessage({do: 'REPLY', message: { text: message }, user_id: id});
  }


  // * Needed for debugging
  manualRequest = () => {
    const { activeRole, me, requestAccess } = this.props;
    requestAccess(activeRole.id, me.id, 'some reason');
  }


  // * Needed for debugging
  manualApprove = () => {
    const { approveProposals, selectedProposals, reset } = this.props;
    approveProposals(selectedProposals);
    reset();
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

        <div id='next-manual-triggers'>
          <Button size='tiny' onClick={this.manualRequest}>
            Request
          </Button>
          <Button size='tiny' onClick={this.manualApprove}>
            Approve
          </Button>
        </div>

        <div id='next-chat-conversation-dock'>
          <ChatForm
            {...this.props}
            disabled={disabled}
            actions={actions}
            submit={(message) => this.send(message)}/>
        </div>
      </div>
    );
  }

}
