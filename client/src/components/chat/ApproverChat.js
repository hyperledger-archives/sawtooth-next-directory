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
import {
  Checkbox,
  Header,
  Image,
  List,
  Segment,
  Transition } from 'semantic-ui-react';


import './ApproverChat.css';
import ChatTranscript from './ChatTranscript';
import Avatar from 'components/layouts/Avatar';
import glyph from 'images/glyph-role.png';


/**
 *
 * @class         ApproverChat
 * @description   Component encapsulating the approver chat view
 *
 */
class ApproverChat extends Component {

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
    const { id, userFromId } = this.props;
    const user = userFromId(userId);
    if (user)
      return userId === id ? `${user.name} (You)` : user.name;
    return null;
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      handleChange,
      selectedProposal,
      selectedRoles,
      selectedUsers,
      subtitle,
      title,
      groupBy } = this.props;

    return (
      <div>
        {(((groupBy === 0 || groupBy === 2) &&
            selectedUsers && selectedUsers.length === 0) ||
          (groupBy === 1 && selectedRoles && selectedRoles.length === 0)) &&
          <div id='next-chat-message-info-container'>
            <Header
              as='h3'
              content='No items selected'
              subheader={`To approve or reject a request or group of requests,
                          pick one or more items from the list on the left.`}/>
          </div>
        }
        { selectedProposal && title && subtitle &&
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
        { selectedUsers &&
          <div id='next-chat-selection-heading-container'>
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
        { (groupBy === 0 || groupBy === 2) && selectedUsers &&
          <div id='next-chat-users-selection-container'>
            <Transition.Group
              as={List}
              animation='fade up'
              duration={{hide: 0, show: 200}}>
              { selectedUsers.map(user =>
                <Segment className='minimal select' padded key={user}>
                  <Checkbox
                    checked={!!user}
                    user={user}
                    onChange={handleChange}/>
                  <div id='next-chat-users-selection-label'>
                    <Avatar
                      size='medium'
                      userId={user}
                      {...this.props}/>
                    <label>
                      {this.userName(user)}
                    </label>
                  </div>
                </Segment>
              ) }
            </Transition.Group>
          </div>
        }
        { groupBy === 1 && selectedRoles &&
          <div id='next-chat-roles-selection-container'>
            <Transition.Group
              as={List}
              animation='fade up'
              duration={{hide: 0, show: 200}}>
              { [...new Set(selectedRoles)].map(role =>
                <Segment className='minimal select' key={role}>
                  <Checkbox
                    checked={!!role}
                    role={role}
                    onChange={handleChange}/>
                  <div id='next-chat-roles-selection-label'>
                    <Image src={glyph} size='mini'/>
                    <label>
                      {this.roleName(role)}
                    </label>
                  </div>
                </Segment>
              ) }
            </Transition.Group>
          </div>
        }
        { selectedProposal &&
          <div id='next-approver-chat-transcript-container'>
            <ChatTranscript {...this.props}
              messages={[{
                text: selectedProposal.open_reason,
                from: selectedProposal.opener,
              }]}/>
          </div>
        }
      </div>
    );
  }

}


export default ApproverChat;
