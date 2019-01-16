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
import { Link } from 'react-router-dom';
import { Card, Grid, Header, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './RolesList.css';
import glyph from 'images/glyph-role.png';


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
    userFromId:         PropTypes.func,
    users:              PropTypes.array,
  }


  state = { fetchingUsers: null };


  /**
   * Entry point to perform tasks required to render
   * component
   */
  componentDidMount () {
    this.init();
    this.init2();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { activePack } = this.props;

    if (prevProps.activePack !== activePack) {
      this.init();
      this.setState({ fetchingUsers: false });
    }
    this.init2();
  }


  /**
   * Determine which roles are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const { activePack, getRoles, roles } = this.props;
    if (!activePack) return;
    const diff = roles ? activePack.roles.filter(roleId =>
      !roles.find(role => role.id === roleId)) : activePack.roles;

    diff && diff.length > 0 && getRoles(diff);
  }


  /**
   * Determine which users are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init2 = () => {
    const { activePack, getUsers, roles, users } = this.props;
    const { fetchingUsers } = this.state;

    if (!roles) return;
    const fetchedRoles = roles.filter(
      role => activePack.roles.indexOf(role.id) !== -1
    );
    if (fetchingUsers || fetchedRoles.length !== activePack.roles.length)
      return;

    this.setState({ fetchingUsers: true });

    const diff = roles && roles
      .filter(role => activePack.roles.find(roleId => role.id === roleId))
      .map(role => role.owners[0])
      .filter(userId => !users.find(user => user.id === userId));

    diff && diff.length > 0 && getUsers([...new Set(diff)]);
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
          <Header.Subheader>
            By
            {' '}
            {user.name}
          </Header.Subheader>
        }
        {user.email &&
          <Header.Subheader className='next-roles-list-email-subheader'>
            {user.email}
          </Header.Subheader>
        }
      </div>
    );
  }


  /**
   * Render segment that contains role info
   * @param {string} roleId Role ID
   * @returns {JSX}
   */
  renderRoleCard (roleId) {
    const { roles } = this.props;
    if (!roles) return null;
    const role = roles.find((role) => role.id === roleId);

    return (
      role &&
        <Grid.Column key={roleId} largeScreen={8} widescreen={5}>
          <Card
            fluid
            as={Link}
            to={`/roles/${roleId}`}
            className='minimal medium'>
            <Header as='h4' className='next-roles-list-role-info'>
              <div>
                <Image size='mini' src={glyph}/>
              </div>
              <div>
                {role && role.name}
                {role && role.owners && this.renderUserInfo(role.owners[0])}
              </div>
            </Header>
          </Card>
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
            this.renderRoleCard(roleId)
          )) }
        </Grid>
      </div>
    );
  }

}


export default RolesList;
