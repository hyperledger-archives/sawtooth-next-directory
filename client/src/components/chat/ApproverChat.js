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
import {
  Checkbox,
  Header,
  List,
  Segment,
  Transition } from 'semantic-ui-react';


import './ApproverChat.css';
import ChatTranscript from './ChatTranscript';
import Avatar from 'components/layouts/Avatar';
import { Icon } from 'semantic-ui-react';


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
            <Transition.Group
              as={List}
              horizontal
              animation='fade right'
              duration={{hide: 0, show: 1000}}>
              { selectedUsers.map((user, index) => {
                if (index > 2) return null;

                if (index === 2) {
                  return (
                    <span className='next-chat-list-icon'>
                      <Icon inverted name='add' size='tiny'/>
                    </span>
                  );
                }
                return (<Avatar
                  key={user}
                  userId={user}
                  size='medium'
                  className='pull-left'
                  {...this.props}/>);
              })}
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
        { groupBy === 0 && selectedUsers &&
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
        { groupBy === 1 && selectedRoles &&
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
