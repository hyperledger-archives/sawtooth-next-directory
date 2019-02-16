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
  Button,
  Icon,
  Image,
  Menu,
  Header as MenuHeader } from 'semantic-ui-react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';


import './Notifications.css';
import glyph from 'images/glyph-role.png';


import Avatar from './Avatar';
import * as utils from 'services/Utils';


/**
 *
 * @class         Notifications
 * @description   Notifications menu
 *
 */
class Notifications extends Component {

  static propTypes = {
    getUsers:             PropTypes.func,
    openProposalsByUser:  PropTypes.object,
    toggleMenu:           PropTypes.func,
    userFromId:           PropTypes.func,
    users:                PropTypes.array,
  };


  /**
   * Entry point to perform tasks required to render
   * component. Load users not loaded in client.
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes. Load users not loaded in client.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { me, openProposalsByUser } = this.props;
    if (prevProps.openProposalsByUser !== openProposalsByUser)
      this.init();
    if (prevProps.me !== me)
      this.init();
  }


  /**
   * Determine which roles and users are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const {
      getRoles,
      getUsers,
      openProposalsByUser,
      expired,
      roles,
      users } = this.props;

    if (expired) {
      let roleIds = expired;
      if (roles && roles.length) {
        roleIds = roleIds.filter(
          roleId => !roles.find(role => role.id === roleId)
        );
      }
      getRoles(roleIds);
    }
    if (openProposalsByUser) {
      let userIds = Object.keys(openProposalsByUser);
      if (users && users.length) {
        userIds = userIds.filter(
          userId => !users.find(user => user.id === userId)
        );
      }
      getUsers(userIds, true);
    }
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      expired,
      openProposalsByUser,
      roleFromId,
      toggleMenu,
      userFromId } = this.props;

    return (
      <div id='next-header-notification-menu'>
        <Menu
          inverted
          size='huge'
          vertical>
          { openProposalsByUser &&
            Object.keys(openProposalsByUser).length > 0 &&
            <div className='menu-section'>
              <Menu.Header>
                Pending Requests
              </Menu.Header>
              <div className='menu-tray'>
                { Object.keys(openProposalsByUser).map(userId => {
                  const user = userFromId(userId);
                  return (
                    user &&
                    <Menu.Item
                      key={userId}
                      as={Link}
                      to='/approval/pending/individual'
                      className='medium'
                      onClick={toggleMenu}>
                      <MenuHeader as='h5'>
                        <div>
                          <Avatar
                            userId={userId}
                            size='small'
                            {...this.props}/>
                          <MenuHeader.Content>
                            <strong>
                              {user.name}
                            </strong>
                            {' requested access to '}
                            <strong>
                              { utils.countLabel(
                                openProposalsByUser[userId].length,
                                'role',
                              )}
                            </strong>
                          </MenuHeader.Content>
                        </div>
                      </MenuHeader>
                    </Menu.Item>
                  );
                }) }
              </div>
            </div>
          }
          { expired && expired.length > 0 &&
            <div className='menu-section'>
              <Menu.Header>
                Expired Roles
              </Menu.Header>
              <div className='menu-tray'>
                { expired.map(roleId => {
                  const role = roleFromId(roleId);
                  return (
                    role &&
                    <Menu.Item
                      className='medium'
                      key={roleId}>
                      <MenuHeader as='h5'>
                        <div>
                          <Image size='small' src={glyph}/>
                          <MenuHeader.Content>
                            {'Your membership to '}
                            <strong>
                              {role.name}
                            </strong>
                            {' has expired.'}
                          </MenuHeader.Content>
                        </div>
                        <Button
                          as={Link}
                          to={`/roles/${roleId}`}
                          size='mini'
                          inverted
                          color='blue'
                          onClick={toggleMenu}>
                          Renew
                        </Button>
                      </MenuHeader>
                    </Menu.Item>
                  );
                }) }
              </div>
            </div>
          }
          { openProposalsByUser && expired &&
            Object.keys(openProposalsByUser).length === 0 &&
            expired.length === 0 &&
            <MenuHeader as='h3' icon inverted textAlign='center'>
              <Icon name='check circle outline' color='green'/>
              You&#39;re all caught up
              <MenuHeader.Subheader>
                You have no pending notifications
              </MenuHeader.Subheader>
            </MenuHeader>
          }
        </Menu>
      </div>
    );
  }
}


export default Notifications;
