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
import { Checkbox, List, Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './PeopleList.css';


/**
 *
 * @class         PeopleList
 * @description   Displays people in a list when approving proposals
 *
 */
class PeopleList extends Component {

  static propTypes = {
    getRoles:                 PropTypes.func,
    getUsers:                 PropTypes.func,
    handleChange:             PropTypes.func,
    openProposalsByRole:      PropTypes.object,
    openProposalsByUser:      PropTypes.object,
    roleFromId:               PropTypes.func,
    selectedProposals:        PropTypes.array,
    selectedUsers:            PropTypes.array,
    roles:                    PropTypes.array,
    users:                    PropTypes.array,
  };


  /**
   * Entry point to perform tasks required to render
   * component. Get users not loaded in client.
   */
  componentDidMount () {
    const {
      getRoles,
      getUsers,
      openProposalsByRole,
      openProposalsByUser,
      roles,
      users } = this.props;

    if (!openProposalsByUser) return;
    let collection;
    const newUsers = Object.keys(openProposalsByUser);

    users ?
      collection = newUsers.filter(newUser =>
        !users.find(user => newUser === user.id)) :
      collection = newUsers;

    getUsers(collection);

    const newRoles = Object.keys(openProposalsByRole);
    roles ?
      collection = newRoles.filter(newRole =>
        !roles.find(role => newRole === role.id)) :
      collection = newRoles;

    getRoles(collection);
  }


  /**
   * Called whenever Redux state changes. Get users not
   * loaded in client on state change.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { getUsers, openProposalsByUser } = this.props;
    const newUsers = Object.keys(openProposalsByUser);
    const oldUsers = Object.keys(prevProps.openProposalsByUser);

    if (newUsers.length > oldUsers.length) {
      const diff = newUsers.filter(user => !oldUsers.includes(user));
      getUsers(diff);
    }
  }


  /**
   * Proposal item is checked / unchecked based on its presence in
   * selectedProposals state array
   * @param {object} proposal Selected proposal
   * @returns {boolean}
   */
  isRoleChecked = (proposal) => {
    const { selectedProposals } = this.props;
    return selectedProposals.indexOf(proposal.id) !== -1;
  }


  /**
   * User item is checked / unchecked based on its presence in
   * selectedUsers state array
   * @param {string} userId User ID of selected user
   * @returns {boolean}
   */
  isUserChecked = (userId) => {
    const { selectedUsers } = this.props;
    return selectedUsers.indexOf(userId) !== -1;
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
   * Render role / pack proposals for a given user as a sub-list
   * of a parent user list item.
   * @param {string} userId    User ID
   * @param {array}  proposals Array of user proposals
   * @returns {JSX}
   */
  renderUserProposals (userId, proposals) {
    const { handleChange } = this.props;
    return (
      proposals.map((proposal) => (
        <List.Item key={proposal.id}>
          <List.Header key={proposal.id}>
            <span className='next-people-list-proposal-role'>
              <Checkbox
                checked={this.isRoleChecked(proposal)}
                proposal={proposal.id}
                user={userId}
                label={this.roleName(proposal.object)}
                onChange={handleChange}/>
            </span>
            <span className='next-people-list-proposal-reason'>
              {proposal.open_reason}
            </span>
          </List.Header>
        </List.Item>
      ))
    );
  }


  /**
   * Render user list item
   * One list item per user with an open request.
   * @param {string} userId User ID
   * @returns {JSX}
   */
  renderUserItem (userId) {
    const { handleChange, openProposalsByUser, users } = this.props;

    if (!users) return null;
    const user = users.find((user) => user.id === userId);

    return (
      <div className='next-people-list-item' key={userId}>
        { user &&
        <List.Item>
          <List.Header>
            { user.name &&
              <span className='next-people-list-name'>
                <Checkbox
                  checked={this.isUserChecked(userId)}
                  label={user.name}
                  user={userId}
                  onChange={handleChange}/>
              </span>
            }
            { user.email &&
              <span className='next-people-list-email'>
                {user.email}
              </span>
            }
            <Icon name='info circle' color='grey'/>
          </List.Header>
          <List.List>
            { this.renderUserProposals(
              userId,
              openProposalsByUser[userId].map(proposal => proposal)
            )}
          </List.List>
        </List.Item>
        }
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { openProposalsByUser } = this.props;
    if (!openProposalsByUser) return null;
    return (
      <div>
        <List>
          { Object.keys(openProposalsByUser).map((userId) => (
            this.renderUserItem(userId)
          ))}
        </List>
      </div>
    );
  }

}


export default PeopleList;
