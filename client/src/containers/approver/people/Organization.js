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
import { Button, Container, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './Organization.css';


/**
 *
 * @class         Organization
 * @description   Component encapsulating the member list
 *
 *
 */
class Organization extends Component {

  static propTypes = {
    getOrganization:    PropTypes.func,
    handleUserSelect:   PropTypes.func,
    getUsers:           PropTypes.func,
    organization:       PropTypes.object,
    userFromId:         PropTypes.func,
  }


  state = { showManagers: null };


  /**
   * Entry point to perform tasks required to render component.
   */
  componentDidMount () {
    const { getOrganization, handleUserSelect } = this.props;

    // TODO: Use until endpoint ready
    getOrganization('fcb9a003-75d4-48ad-a5fd-aef5c8a56744');
    handleUserSelect('fcb9a003-75d4-48ad-a5fd-aef5c8a56744');
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { getUsers, organization } = this.props;
    if (prevProps.organization !== organization)
      getUsers(Object.values(organization).flat());

  }


  toggleManagers = () => {
    this.setState(prevState => ({
      showManagers: !prevState.showManagers,
    }));
  }


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
   * Render peers
   * @returns {JSX}
   */
  renderPeers () {
    const { organization } = this.props;
    return (
      <div className='pull-right' id='next-organization-peers'>
        { organization.peers.map((userId, index) => (
          <div className='next-organization-peer-item' key={userId}>
            <Image
              src={`http://i.pravatar.cc/300?img=${index}`}
              avatar
              size='mini'/>
          </div>
        ))}
      </div>
    );
  }


  /**
   * Render managers
   * @returns {JSX}
   */
  renderManagers () {
    const { organization } = this.props;
    return (
      <div id='next-organization-managers'>
        { organization.managers.map((userId, index) => (
          <div key={userId} className='next-organization-manager-item'>
            <div className='pull-left'>
              <Image
                src={`http://i.pravatar.cc/300?img=${index}`}
                avatar
                size='mini'/>
              <div className='next-organization-user-info'>
                <h4>{this.userName(userId)}</h4>
                {this.userEmail(userId)}
              </div>
            </div>
            { index === 0 && this.renderPeers() }
          </div>
        ))}
      </div>
    );
  }


  /**
   * Render person
   * @returns {JSX}
   */
  renderDirectReports () {
    const { handleUserSelect, organization } = this.props;
    return (
      <div id='next-organization-direct-reports'>
        { organization.direct_reports.map((userId, index) => (
          <div
            onClick={() => handleUserSelect(userId)}
            className='next-organization-direct-report-item'
            key={userId}>
            <Image
              src={`http://i.pravatar.cc/300?img=${index}`}
              avatar
              size='mini'/>
            <div className='next-organization-user-info'>
              <h4>{this.userName(userId)}</h4>
              {this.userEmail(userId)}
            </div>
          </div>
        ))}
      </div>
    );
  }


  /**
   * Render person
   * @returns {JSX}
   */
  renderPerson () {
    const { organization } = this.props;
    return (
      <div id='next-organization-current-person'>
        <div id='next-organization-current-person-user-info-container'>
          <Image src='http://i.pravatar.cc/300' avatar size='mini'/>
          <div className='next-organization-user-info'>
            <h4>{this.userName(organization.id)}</h4>
            {this.userEmail(organization.id)}
          </div>
        </div>
        {this.renderDirectReports()}
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { organization } = this.props;
    const { showManagers } = this.state;

    let transition = '';
    if (showManagers)
      transition ='next-organization-managers-show';
    else if (showManagers !== null)
      transition = 'next-organization-managers-hide';


    return (
      <div>
        <Container
          id='next-organization-toggle-manager-button-container'
          textAlign='right'>
          <Button
            onClick={() => this.toggleManagers()}>
            {showManagers ? 'Hide Managers' : 'Show Managers'}
          </Button>
        </Container>
        <div className={transition} id='next-organization-container'>
          { organization && this.renderManagers() }
          { organization && this.renderPerson() }
        </div>
      </div>

    );
  }

}


export default Organization;
