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
  Icon,
  Table } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './TableList.css';
import * as utils from 'services/Utils';
import Avatar from 'components/layouts/Avatar';


/**
 *
 * @class         TableList
 * @description   Displays roles in a list when approving proposals
 *
 */
class TableList extends Component {

  static propTypes = {
    getRoles:              PropTypes.func,
    getUsers:              PropTypes.func,
    handleChange:          PropTypes.func,
    openProposalsByRole:   PropTypes.object,
    openProposalsByUser:   PropTypes.object,
    roleFromId:            PropTypes.func,
    roles:                 PropTypes.array,
    selectedProposals:     PropTypes.array,
    selectedRoles:         PropTypes.array,
    users:                 PropTypes.array,
  };


  state = { column: null, direction: null };


  // TODO: Refactor
  /**
   * Entry point to perform tasks required to render
   * component. Get users not loaded in client.
   */
  componentDidMount  () {
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

    getUsers(collection, true);

    const newRoles = Object.keys(openProposalsByRole);
    roles ?
      collection = newRoles.filter(newRole =>
        !roles.find(role => newRole === role.id)) :
      collection = newRoles;

    getRoles(collection);
  }


  /**
   * Called whenever Redux state changes. Get roles and
   * users not loaded in client on state change.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const {
      getRoles,
      getUsers,
      openProposalsByRole,
      openProposalsByUser } = this.props;

    const newRoles = Object.keys(openProposalsByRole);
    const newUsers = Object.keys(openProposalsByUser);
    const oldRoles = Object.keys(prevProps.openProposalsByRole);
    const oldUsers = Object.keys(prevProps.openProposalsByUser);

    if (newUsers.length > oldUsers.length) {
      const diff = newUsers.filter(user => !oldUsers.includes(user));
      getUsers(diff, true);
    }
    if (newRoles.length > oldRoles.length) {
      const diff = newRoles.filter(role => !oldRoles.includes(role));
      getRoles(diff);
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
   * Render user avatars for a given role
   * @param {string} roleId Role ID
   * @returns {JSX}
   */
  renderUsers (roleId) {
    const { openProposalsByRole } = this.props;
    return (
      <div className='pull-right'>
        { openProposalsByRole[roleId].map((proposal, index) => {
          if (index > 2) return null;
          if (index === 2) {
            return (
              <span
                key={proposal.id}
                className='next-role-list-icon'>
                <Icon
                  color='orange'
                  name='add'
                  size='tiny'/>
                {openProposalsByRole[roleId].length - 2}
              </span>
            );
          }
          return (
            <Avatar
              key={proposal.id}
              userId={proposal.opener}
              size='medium'
              {...this.props}/>
          );
        })}
      </div>
    );
  }


  /**
   * Proposal item is checked / unchecked based on its presence in
   * selectedProposals state array
   * @param {object} proposal Selected proposal
   * @returns {boolean}
   */
  isProposalChecked = (proposal) => {
    const { selectedProposals } = this.props;
    return selectedProposals.indexOf(proposal.id) !== -1;
  }


  /**
   * Is checkbox state indeterminate (i.e., should show dot)
   * @param {string} roleId Selected role
   * @returns {boolean}
   */
  // TODO: Indeterminate state not adding class to UI in one scenario
  isIndeterminate = (roleId) => {
    const { selectedProposals, openProposalsByRole } = this.props;
    const selected = openProposalsByRole[roleId].filter(proposal =>
      selectedProposals.includes(proposal.id));

    return selected.length > 0 &&
      selected.length < openProposalsByRole[roleId].length;
  }


  /**
   * Toggle checkbox when table row clicked
   * @param {string} proposal Proposal
   */
  handleRowClick = (proposal) => {
    const { handleChange } = this.props;
    handleChange(undefined, {
      checked: !this.isProposalChecked(proposal),
      proposal: proposal.id,
      user: proposal.opener,
    });
  }


  /**
   * Sort
   */
  handleSort = () => {
    // Not yet implemented
  };


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
   * Get user email from user ID
   * @param {string} userId User ID
   * @returns {string}
   */
  userEmail = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    return user && user.email;
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { handleChange, openProposals } = this.props;
    const { column, direction } = this.state;

    return (
      <Table
        sortable
        selectable
        singleLine
        striped
        padded='very'
        className='cursor-pointer'>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell/>
            <Table.HeaderCell
              sorted={column === 'role_name' ? direction : null}
              onClick={this.handleSort('role_name')}>
              Role Name
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'requester' ? direction : null}
              onClick={this.handleSort('requester')}>
              Requester
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'requester_email' ? direction : null}
              onClick={this.handleSort('requester_email')}>
              Requester Email
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'created_date' ? direction : null}
              onClick={this.handleSort('created_date')}>
              Opened On
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          { openProposals && openProposals.map(proposal => (
            <Table.Row
              key={proposal.id}
              onClick={() => this.handleRowClick(proposal)}>
              <Table.Cell collapsing>
                <Checkbox
                  checked={this.isProposalChecked(proposal)}
                  proposal={proposal.id}
                  user={proposal.opener}
                  onChange={handleChange}/>
              </Table.Cell>
              <Table.Cell>
                {this.roleName(proposal.object)}
              </Table.Cell>
              <Table.Cell>
                <Header as='h4' className='next-approver-approved-table-opener'>
                  <Avatar
                    userId={proposal.opener}
                    size='small'
                    {...this.props}/>
                  <Header.Content>
                    {this.userName(proposal.opener)}
                  </Header.Content>
                </Header>
              </Table.Cell>
              <Table.Cell className='next-approver-approved-table-email'>
                {this.userEmail(proposal.opener)}
                <Icon name='info circle' color='grey'/>
              </Table.Cell>
              <Table.Cell>
                {utils.formatDate(proposal.created_date)}
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    );

  }

}


export default TableList;
