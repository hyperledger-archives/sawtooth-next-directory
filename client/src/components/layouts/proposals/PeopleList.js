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
   */
  componentDidMount () {
    const { getUsers, openProposalsByUser } = this.props;

    if (!openProposalsByUser) return;
    getUsers(Object.keys(openProposalsByUser));
  }


  roleName = (roleId) => {
    const { roleFromId } = this.props;
    const role = roleFromId(roleId);

    return role && role.name;
  };


  isChecked = (roleId) => {
    const { selectedRoles } = this.props;
    return selectedRoles.indexOf(roleId) !== -1;
  }


  /**
   *
   * Render role / pack proposals for a given user as a sub-List
   * of a parent user list item.
   *
   * @param {*} userId User ID
   *
   *
   */
  renderUserProposals (userId) {
    const { handleChange, openProposalsByUser,  } = this.props;

    return (
      openProposalsByUser[userId].map((proposal) => (
        <List.Item key={proposal.object}>
          <List.Header>
            <span className='next-people-list-proposal'>
              <Checkbox
                checked={this.isChecked(proposal.object)}
                role={proposal.object}
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
   * Render a list item
   *
   * One list item per user with an open request.
   *
   * @param {*} userId User ID
   * @param {*} index
   *
   */
  renderUserItem (userId) {
    const { users } = this.props;

    if (!users) return null;
    const user = users.find((user) => user.id === userId);

    return (
      <div className='next-people-list-item' key={userId}>
        <List.Item>
          <List.Header>
            { user && user.name &&
              <span className='next-people-list-name'>
                <Checkbox label={user.name}/>
              </span>
            }
            { user && user.email &&
              <span className='next-people-list-email'>
                {user.email}
              </span>
            }
            <Icon name='info circle' color='grey'/>
          </List.Header>
          <List.List>
            { this.renderUserProposals(userId) }
          </List.List>
        </List.Item>
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
