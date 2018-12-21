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
import { Header, Image, Loader, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './OrganizationList.css';


/**
 *
 * @class         OrganizationList
 * @description   Component encapsulating the member list
 *
 *
 */
class OrganizationList extends Component {

  static propTypes = {
    fetchingAllUsers:   PropTypes.bool,
    getAllUsers:        PropTypes.func,
    getUsers:           PropTypes.func,
    handleUserSelect:   PropTypes.func,
    id:                 PropTypes.string,
    members:            PropTypes.array,
    owners:             PropTypes.array,
    users:              PropTypes.array,
  }


  /**
   * Entry point to perform tasks required to render component.
   * Get first page of all users.
   */
  componentDidMount   () {
    const { getAllUsers, handleUserSelect, id, users } = this.props;
    (!users || (users && users.length < 99)) && getAllUsers();
    handleUserSelect(id);
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {

  }


  /**
   * Render segment containing user info
   * @returns {JSX}
   */
  renderUserSegment () {
    const { handleUserSelect, users } = this.props;
    return (
      users && users.map((user, index) => (
        <Segment
          key={index}
          onClick={() => handleUserSelect(user.id)}
          className='no-padding minimal'>
          <Header as='h3' className='next-member-list-user-info'>
            <div>
              <Image src={`http://i.pravatar.cc/150?u=${user.id}`} avatar/>
            </div>
            <div>
              {user.name}
              {user.email &&
                <Header.Subheader>{user.email}</Header.Subheader>
              }
            </div>
          </Header>
        </Segment>
      ))
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { fetchingAllUsers } = this.props;

    if (fetchingAllUsers) {
      return (
        <Loader active={fetchingAllUsers} size='large'>
          Loading
        </Loader>
      );
    }

    return (
      <div id='next-approver-people-list-container'>
        {this.renderUserSegment()}
      </div>
    );
  }

}


export default OrganizationList;
