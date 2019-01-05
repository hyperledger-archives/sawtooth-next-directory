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
import {
  Icon,
  Menu,
  Header as MenuHeader } from 'semantic-ui-react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';


import './Notifications.css';
import * as utils from 'services/Utils';
import Avatar from './Avatar';


/**
 *
 * @class         Notifications
 * @description   Notifications menu
 *
 */
export default class Notifications extends Component {

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
    const { openProposalsByUser } = this.props;
    if (prevProps.openProposalsByUser !== openProposalsByUser)
      this.init();
  }


  /**
   * Determine which users are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const { getUsers, openProposalsByUser, users } = this.props;
    if (!openProposalsByUser) return;

    let userIds = Object.keys(openProposalsByUser);
    if (users && users.length) {
      userIds = userIds.filter(
        userId => !users.find(user => user.id === userId)
      );
    }
    getUsers(userIds);
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { openProposalsByUser, toggleMenu, userFromId } = this.props;

    return (
      <div id='next-header-notification-menu'>
        <Menu
          inverted
          size='huge'
          vertical>
          { openProposalsByUser &&
            Object.keys(openProposalsByUser).length !== 0 &&
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
                      onClick={toggleMenu}>
                      <MenuHeader as='h5'>
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
                      </MenuHeader>
                    </Menu.Item>
                  );
                }) }
              </div>
            </div>
          }
          { openProposalsByUser &&
            Object.keys(openProposalsByUser).length === 0 &&
            <MenuHeader as='h3' icon inverted textAlign='center'>
              <Icon name='check circle outline'/>
              You&apos;re all caught up
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
