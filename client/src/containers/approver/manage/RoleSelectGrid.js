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
import { Button, Grid, Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './RoleSelectGrid.css';
import * as utils from 'services/Utils';


/**
 *
 * @class         RoleSelectGrid
 * @description   Create new pack component
 *
 */
class RoleSelectGrid extends Component {

  static propTypes = {
    getRoles:         PropTypes.func,
    handleClick:      PropTypes.func,
    ownedRoles:       PropTypes.array,
    roles:            PropTypes.array,
    roleFromId:       PropTypes.func,
    selectedRoles:    PropTypes.array,
  };


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
   * Render role toggle button
   * @param {string} roleId Role ID
   * @returns {JSX}
   */
  renderRoleToggle = (roleId) => {
    const { handleClick, selectedRoles } = this.props;
    return (
      this.roleName(roleId) &&
      <div>
        <Button
          fluid
          toggle
          className='toggle-card gradient'
          active={selectedRoles.includes(roleId)}
          onClick={() => handleClick(roleId)}
          size='massive'>
          {this.roleName(roleId)}
          { selectedRoles.includes(roleId) &&
            <Icon name='check' color='pink'/>
          }
        </Button>
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { ownedRoles } = this.props;
    return (
      <Grid centered columns={3} id='next-role-select-grid'>
        { ownedRoles && ownedRoles.map(roleId => (
          <Grid.Column key={roleId} width={5}>
            {this.renderRoleToggle(roleId)}
          </Grid.Column>
        ))}
      </Grid>
    );
  }

}


export default RoleSelectGrid;
