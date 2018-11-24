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
import './RoleList.css';
import { Checkbox, Image, Segment } from 'semantic-ui-react';


/**
 *
 * @class RoleList
 *
 *
 */
export default class RoleList extends Component {

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


  roleName = (roleId) => {
    const { roleFromId } = this.props;

    const role = roleFromId(roleId);
    return role && role.name;
  };


  /**
   *
   * Render user avatars for a given role
   *
   *
   *
   */
  renderUsers (roleId) {
    const { openProposalsByRole } = this.props;

    return (
      <div className='pull-right'>
        { openProposalsByRole[roleId].map(proposal => (
          <Image
            key={proposal.id}
            src={'http://i.pravatar.cc/150?' + proposal.id}
            size='mini'
            avatar/>
        ))}
      </div>
    );
  }


  isRoleChecked = (roleId) => {
    const { selectedRoles } = this.props;
    return selectedRoles.indexOf(roleId) !== -1;
  }


  // TODO: Indeterminate state not adding class to UI in one scenario
  isIndeterminate = (roleId) => {
    const { selectedProposals, openProposalsByRole } = this.props;
    const selected = openProposalsByRole[roleId].filter(proposal =>
        selectedProposals.includes(proposal.id))

    return selected.length > 0 &&
      selected.length < openProposalsByRole[roleId].length;
  }


  /**
   *
   * Render role list item
   *
   * One list item per role with an open request.
   *
   * @param {*} roleId Role ID
   *
   *
   */
  renderRoleItem (roleId) {
    const { handleChange} = this.props;
    return (
      <div className='next-role-list-item' key={roleId}>
        <Segment className='light' padded>
          <Checkbox
            defaultIndeterminate={this.isIndeterminate(roleId)}
            checked={this.isRoleChecked(roleId)}
            role={roleId}
            label={this.roleName(roleId)}
            onChange={handleChange}/>
          {this.renderUsers(roleId)}
        </Segment>
      </div>
    );
  }


  render () {
    const { openProposalsByRole } = this.props;
    if (!openProposalsByRole) return null;

    return (
      <div id='next-roles-list-container'>
        { Object.keys(openProposalsByRole).map(roleId => (
          this.renderRoleItem(roleId)
        ))}
      </div>
    );
  }

}
