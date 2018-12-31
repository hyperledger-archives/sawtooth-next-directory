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
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
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
import ChatMessage from './ChatMessage';
import ChatForm from 'components/forms/ChatForm';
import Avatar from 'components/layouts/Avatar';


// TODO: Break out into child components
/**
 *
 * @class         Chat
 * @description   Component encapsulating the chat view
 *
 */
class Chat extends Component {

  /**
   * Entry point to perform tasks required to render component.
   * If socket open, send message to get initial recommendation
   * from chatbot
   */
  componentDidMount () {
    const { id, isSocketOpen, messages, sendMessage, type } = this.props;

    if (type === 'REQUESTER' &&
        isSocketOpen &&
        !messages) {
      sendMessage({
        do: 'CREATE', message: { text: '/recommend' }, user_id: id,
      });
    }
  }


  /**
   * Called whenever Redux state changes. On socket open, send
   * message to get initial recommendation from chatbot
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
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
        type === 'REQUESTER' &&
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


  /**
   * Get role name from role ID
   * @param {string} roleId Role ID
   * @returns {string}
   */
  roleName = (roleId) => {
    const { roleFromId } = this.props;
    const role = roleFromId(roleId);
    return role && role.name;
  };


  /**
   * Get user name from user ID
   * @param {string} userId User ID
   * @returns {string}
   */
  userName = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    return user && user.name;
  };


  /**
   * Send message to chatbot engine
   * @param {string} message Message body
   */
  send = (message) => {
    const { id, sendMessage } = this.props;
    sendMessage({do: 'REPLY', message: { text: message }, user_id: id});
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


  manualApprove = () => {
    const { approveProposals, selectedProposals, reset } = this.props;
    approveProposals(selectedProposals);
    reset();
  }


  manualReject = () => {
    const { rejectProposals, selectedProposals, reset } = this.props;
    rejectProposals(selectedProposals);
    reset();
  }


  // * Needed for debugging
  manualErrorTest = () => {
    const { sendMessage } = this.props;
    sendMessage({
      fail: 'yes', do: 'CREATE', message: { text: '/recommend' }, user_id: '?',
    });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      activeUser,
      disabled,
      handleChange,
      handleOnBehalfOf,
      selectedProposal,
      selectedRoles,
      selectedUsers,
      subtitle,
      title,
      groupBy,
      type } = this.props;

    return (
      <div id='next-chat-container'>
        { type === 'REQUESTER' && title &&
          <Header id='next-chat-header' size='small' inverted>
            {title}
            <Icon link name='pin' size='mini' className='pull-right'/>
          </Header>
        }

        { type === 'APPROVER' && selectedProposal && title && subtitle &&
          <div id='next-chat-selection-heading-container'>
            <Avatar
              userId={selectedProposal.opener}
              size='medium'
              className='pull-left'
              {...this.props}/>
            <Header as='h3' inverted>
              {title}
              <Header.Subheader>
                {subtitle}
              </Header.Subheader>
            </Header>
          </div>
        }

        { type === 'PEOPLE' &&
          <div id='next-chat-users-selection-container'>
            { activeUser &&
              <div id='next-chat-organization-heading'>
                <Image
                  size='small'
                  src={`http://i.pravatar.cc/150?u=${activeUser}`}
                  avatar/>
                <Header as='h2' inverted>
                  {this.userName(activeUser)}
                </Header>
                <div>
                  <Button
                    as={Link}
                    to={`people/${activeUser}/pending`}
                    onClick={handleOnBehalfOf}>
                    Pending Approvals
                  </Button>
                </div>
              </div>
            }
          </div>
        }

        { type === 'APPROVER' && selectedUsers &&
          <div id='next-chat-selection-heading-container'>
            <Transition.Group
              as={List}
              horizontal
              animation='fade right'
              duration={{hide: 0, show: 1000}}>
              { selectedUsers.map(user =>
                <Avatar
                  key={user}
                  userId={user}
                  size='medium'
                  className='pull-left'
                  {...this.props}/>
              ) }
            </Transition.Group>
            <Transition
              visible={selectedUsers.length > 0}
              animation='fade left'
              duration={{hide: 0, show: 300}}>
              <Header as='h3' inverted>
                {selectedUsers.length === 1 && title}
                <Header.Subheader>
                  {subtitle}
                </Header.Subheader>
              </Header>
            </Transition>
          </div>
        }

        { type === 'APPROVER' && groupBy === 0 && selectedUsers &&
          <div id='next-chat-users-selection-container'>
            <Transition.Group
              as={List}
              animation='fade down'
              duration={{hide: 300, show: 300}}>
              { selectedUsers.map(user =>
                <Segment className='minimal' padded='very' key={user}>
                  <Checkbox
                    checked={!!user}
                    user={user}
                    label={this.userName(user)}
                    onChange={handleChange}/>
                </Segment>
              ) }
            </Transition.Group>
          </div>
        }

        { type === 'APPROVER' && groupBy === 1 && selectedRoles &&
          <div id='next-chat-roles-selection-container'>
            <Transition.Group
              as={List}
              animation='fade down'
              duration={{hide: 300, show: 300}}>
              { [...new Set(selectedRoles)].map(role =>
                <Segment className='minimal' padded='very' key={role}>
                  <Checkbox
                    checked={!!role}
                    role={role}
                    label={this.roleName(role)}
                    onChange={handleChange}/>
                </Segment>
              ) }
            </Transition.Group>
          </div>
        }

        { type === 'APPROVER' && selectedProposal &&
          <div id='next-chat-messages-container'>
            <ChatMessage
              messages={[{
                text: selectedProposal.open_reason,
                from: selectedProposal.opener,
              }]}/>
          </div>
        }

        { type === 'REQUESTER' &&
          <div id='next-chat-messages-container'>
            <ChatMessage {...this.props}/>
          </div>
        }

        { type !== 'PEOPLE' &&
          <div id='next-chat-conversation-dock'>
            <ChatForm
              {...this.props}
              disabled={disabled}
              approve={this.manualApprove}
              reject={this.manualReject}
              requestRole={this.manualRequestRole}
              requestPack={this.manualRequestPack}
              send={this.send}/>
          </div>
        }
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    fetching:      state.chat.fetching,
    socketError:   state.app.socketError,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(Chat);
