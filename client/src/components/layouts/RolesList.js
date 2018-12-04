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
import './MemberList.css';
import glyph from '../../images/header-glyph-role.png';


/**
 *
 * @class         RolesList
 * @description   Component encapsulating the roles list
 *
 *
 */
export default class MemberList extends Component {

  static propTypes = {
    activePack:         PropTypes.object,
    getRoles:           PropTypes.func,
    getUsers:           PropTypes.func,
    roles:              PropTypes.array,
    users:              PropTypes.array,
    userFromId:         PropTypes.func,
  }


  componentDidMount () {
    this.init();
  }


  componentDidUpdate (prevProps) {
    const { activePack } = this.props;
    if (prevProps.activePack !== activePack) this.init();
  }


  init () {
    const {
      activePack,
      getRoles,
      getUsers,
      roles,
      users } = this.props;
    if (!roles || !users) return;

    const diff = activePack.roles.filter(roleId =>
      roles.find(role => role.id !== roleId));
    const placeholder = roles.map(role => role.id);
    const diff2 = roles
      .filter(role => placeholder.find(roleId => role.id === roleId))
      .map(role => users
        .find(user => user.id !== role.owners[0]) && role.owners[0])

    diff && getRoles(diff);
    diff2 && getUsers([...new Set(diff2)]);
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


  render () {
    const { roles } = this.props;
    return (
      <div>
        <Grid columns={3} stackable>
          {/* { activePack && activePack.roles.map((roleId) => (
            this.renderRoleSegment(roleId)
          )) } */}
          { roles && roles.map((role) => (
            this.renderRoleSegment(role.id)
          )) }
        </Grid>
      </div>
    );
  }

}
