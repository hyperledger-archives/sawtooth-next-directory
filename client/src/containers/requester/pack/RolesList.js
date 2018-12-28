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
import { Grid, Header, Image, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './RolesList.css';
import glyph from 'images/header-glyph-role.png';


/**
 *
 * @class         RolesList
 * @description   Component encapsulating the roles list
 *
 *
 */
class RolesList extends Component {

  static propTypes = {
    activePack:         PropTypes.object,
    getRoles:           PropTypes.func,
    getUsers:           PropTypes.func,
    roles:              PropTypes.array,
    users:              PropTypes.array,
    userFromId:         PropTypes.func,
  }


  /**
   * Entry point to perform tasks required to render
   * component
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
    const { activePack } = this.props;
    if (prevProps.activePack !== activePack) this.init();
  }


  /**
   * Determine which roles and users are not currently loaded
   * in the client and dispatches actions to retrieve them.
   */
  init () {
    const {
      activePack,
      getRoles,
      getUsers,
      roles,
      users } = this.props;

    if (!activePack) return;

    const diff = roles ? activePack.roles.filter(roleId =>
      roles.find(role => role.id !== roleId)) : activePack.roles;

    const diff2 = roles && users && roles
      .filter(role => activePack.roles.find(roleId => role.id === roleId))
      .map(role => users
        .find(user => user.id !== role.owners[0]) && role.owners[0])
      .filter(userId => userId);


    diff && diff.length > 0 && getRoles(diff);
    diff2 && diff2.length > 0 && getUsers([...new Set(diff2)]);
  }


  /**
   * Render user info
   * @param {string} userId User ID
   * @returns {JSX}
   */
  renderUserInfo = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    if (!user) return null;
    return (
      <div>
        { user.name &&
          <Header.Subheader>By {user.name}</Header.Subheader>
        }
        {user.email &&
          <Header.Subheader>{user.email}</Header.Subheader>
        }
      </div>
    );
  }


  /**
   * Render segment that contains role info
   * @param {string} roleId Role ID
   * @returns {JSX}
   */
  renderRoleSegment (roleId) {
    const { roles } = this.props;
    if (!roles) return null;
    const role = roles.find((role) => role.id === roleId);

    return (
      role &&
        <Grid.Column key={roleId} largeScreen={8} widescreen={5}>
          <Segment padded className='minimal'>
            <Header as='h4' className='next-roles-list-role-info'>
              <div>
                <Image size='mini' src={glyph}/>
              </div>
              <div>
                {role && role.name}
                {role && role.owners && this.renderUserInfo(role.owners[0])}
              </div>
            </Header>
          </Segment>
        </Grid.Column>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { activePack } = this.props;
    return (
      <div>
        <Grid columns={3} stackable>
          { activePack && activePack.roles && activePack.roles.map((roleId) => (
            this.renderRoleSegment(roleId)
          )) }
        </Grid>
      </div>
    );
  }

}


export default RolesList;
