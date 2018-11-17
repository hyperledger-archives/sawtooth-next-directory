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


import './PeopleList.css';


/**
 *
 * @class PeopleList
 *
 *
 */
export default class PeopleList extends Component {

  /**
   *
   * Hydrate data
   *
   *
   */
  componentDidMount () {
    const { getUsers, openProposalsByUser, users } = this.props;

    if (!openProposalsByUser) return;
    let collection;
    const newUsers = Object.keys(openProposalsByUser);

    users ?
      collection = newUsers.filter(newUser =>
        !users.find(user => newUser === user.id)) :
      collection = newUsers;

    getUsers(collection);
  }


  componentWillReceiveProps (newProps) {
    const { getUsers, openProposalsByUser } = this.props;

    const newUsers = Object.keys(newProps.openProposalsByUser);
    const oldUsers = Object.keys(openProposalsByUser);

    if (newUsers.length > oldUsers.length) {
      const diff = newUsers.filter(user => !oldUsers.includes(user));
      getUsers(diff);
    }
  }


  /**
   *
   * Proposal item is checked / unchecked based on its presence in
   * selectedProposals state array
   *
   * @param proposal Selected proposal
   * @param userId   User ID of selected proposal
   *
   *
   */
  isRoleChecked = (proposal, userId) => {
    const { selectedProposals } = this.props;
    return selectedProposals.indexOf(proposal.id) !== -1;
  }


  /**
   *
   * User item is checked / unchecked based on its presence in
   * selectedUsers state array
   *
   * @param userId User ID of selected user
   *
   *
   */
  isUserChecked = (userId) => {
    const { selectedUsers } = this.props;
    return selectedUsers.indexOf(userId) !== -1;
  }


  roleName = (roleId) => {
    const { roleFromId } = this.props;

    const role = roleFromId(roleId);
    return role && role.name;
  };



  /**
   *
   * Render role / pack proposals for a given user as a sub-list
   * of a parent user list item.
   *
   * @param {*} userId User ID
   *
   *
   */
  renderUserProposals (userId, proposals) {
    const { handleChange } = this.props;

    return (
      proposals.map((proposal) => (
        <List.Item key={proposal.id}>
          <List.Header>
            <span className='next-people-list-proposal'>
              <Checkbox
                checked={this.isRoleChecked(proposal, userId)}
                proposals={[proposal]}
                user={userId}
                label={this.roleName(proposal.object)}
                onChange={handleChange}/>
            </span>
          </List.Header>
        </List.Item>
      ))
    );
  }


  /**
   *
   * Render user list item
   *
   * One list item per user with an open request.
   *
   * @param {*} userId User ID
   *
   *
   */
  renderUserItem (userId) {
    const { handleChange, openProposalsByUser, users } = this.props;

    if (!users) return null;

    const user = users.find((user) => user.id === userId);
    const proposals = openProposalsByUser[userId]
      .map(proposal => proposal);

    return (
      <div className='next-people-list-item' key={userId}>
        { user &&
        <List.Item>
          <List.Header>
            { user.name &&
              <span className='next-people-list-name'>
                <Checkbox
                  checked={this.isUserChecked(userId)}
                  user={userId}
                  proposals={proposals}
                  label={user.name}
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
            { this.renderUserProposals(userId, proposals) }
          </List.List>
        </List.Item>
        }
      </div>
    );
  }


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
