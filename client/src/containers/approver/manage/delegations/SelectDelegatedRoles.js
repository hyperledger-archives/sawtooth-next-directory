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
  Grid,
  Input,
  Search,
  Table } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './SelectDelegatedRoles.css';
import * as utils from 'services/Utils';


/**
 *
 * @class         SelectDelegatedRoles
 * @description   Component encapsulating manual and suggested role
 *                selection for a new delegation.
 */
class SelectDelegatedRoles extends Component {

  static propTypes = {
    getRoles:         PropTypes.func,
    ownedRoles:       PropTypes.array,
    roleFromId:       PropTypes.func,
    roles:            PropTypes.array,
    selectedRoles:    PropTypes.array,
  };


  state = { column: null, direction: null };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { ownedRoles } = this.props;
    if (!utils.arraysEqual(prevProps.ownedRoles, ownedRoles))
      this.init();
  }


  /**
   * Determine which roles are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const {
      ownedRoles,
      getRoles,
      roles } = this.props;

    const diff = roles ?
      ownedRoles &&
      ownedRoles.filter(
        roleId => !roles.find(role => role.id === roleId)
      ) :
      ownedRoles;
    diff && diff.length > 0 && getRoles(diff);
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
   * Sort
   */
  handleSort = () => {
    // Not yet implemented
  };


  /**
   * Render roles table
   * @returns {JSX}
   */
  renderTable () {
    const { ownedRoles } = this.props;
    const { column, direction } = this.state;

    return (
      <Table
        basic
        sortable
        selectable
        singleLine
        striped
        className='cursor-pointer'>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>
              <Checkbox/>
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'role_name' ? direction : null}
              onClick={this.handleSort('role_name')}>
              Role Name
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'role_id' ? direction : null}
              onClick={this.handleSort('role_id')}>
              Role ID
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          { ownedRoles && ownedRoles.map(roleId => (
            <Table.Row
              key={roleId}
              onClick={() => {}}>
              <Table.Cell collapsing>
                <Checkbox/>
              </Table.Cell>
              <Table.Cell>
                {this.roleName(roleId)}
              </Table.Cell>
              <Table.Cell className='next-approver-approved-table-email'>
                Unavailable
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { ownedRoles } = this.props;
    return (
      <div>
        <Search
          fluid
          input={() =>
            <Input
              fluid
              size='large'
              icon='search'
              placeholder='Search your roles...'/>}
          className='next-select-delegated-roles-search'
          category
          loading={false}/>
        <Grid centered columns={3} id='next-select-delegated-roles-grid'>
          { ownedRoles && ownedRoles.length > 0 &&
            this.renderTable()
          }
        </Grid>
      </div>
    );
  }

}


export default SelectDelegatedRoles;
