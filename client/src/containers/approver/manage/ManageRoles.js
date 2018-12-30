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
import { Link } from 'react-router-dom';
import { Button, Grid, Header, Image, Segment } from 'semantic-ui-react';


import './ManageRoles.css';
import glyph from 'images/header-glyph-role.png';
import TrackHeader from 'components/layouts/TrackHeader';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


/**
 *
 * @class         ManageRoles
 * @description   Manage component
 *
 */
class ManageRoles extends Component {

  themes = ['minimal', 'contrast', 'magenta'];


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    theme.apply(this.themes);
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
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
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
   * Render a list of roles created by the user
   * @returns {JSX}
   */
  renderRoles () {
    const { ownedRoles } = this.props;
    return (
      <div>
        { ownedRoles && ownedRoles.map(roleId => (
          this.roleName(roleId) &&
          <Segment padded className='minimal' key={roleId}>
            <Header as='h3'>
              <Image src={glyph} size='mini'/>
              <div>{this.roleName(roleId)}</div>
            </Header>
          </Segment>
        ))}
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
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Roles'
            breadcrumb={[
              {name: 'Manage', slug: '/approval/manage'},
              {name: 'Roles', slug: '/approval/manage/roles'},
            ]}
            button={() =>
              <Button
                id='next-approver-manage-roles-create-button'
                icon='add'
                size='huge'
                content='Create New Role'
                labelPosition='left'
                as={Link}
                to='roles/create'/>}
            {...this.props}/>
          <div id='next-approver-manage-roles-content'>
            { ownedRoles && ownedRoles.length > 0 ?
              <div></div> :
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  You haven&apos;t created any roles
                </Header.Content>
              </Header>
            }
            {this.renderRoles()}
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default ManageRoles;
