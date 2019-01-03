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
import { Popup } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './Organization.css';
import Avatar from 'components/layouts/Avatar';


/**
 *
 * @class         Organization
 * @description   Component encapsulating the member list
 *
 *
 */
class Organization extends Component {

  static propTypes = {
    id:                 PropTypes.string,
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
    const { getOrganization, handleUserSelect, id } = this.props;
    getOrganization(id);
    handleUserSelect(id);
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
    const { handleUserSelect, organization } = this.props;
    return (
      <div className='pull-right' id='next-organization-peers'>
        { organization.peers &&
          organization.peers.slice(0, 3).map((userId, index) => (
            <div
              onClick={() => handleUserSelect(userId)}
              className='cursor-pointer next-organization-peer-item'
              key={index}>
              <Popup
                inverted
                trigger={
                  <Avatar
                    userId={userId}
                    size='medium'
                    {...this.props}/>
                }
                content={this.userName(userId)}
                position='bottom center'
                on='hover'/>
            </div>
          ))
        }
      </div>
    );
  }


  /**
   * Render managers
   * @returns {JSX}
   */
  renderManagers () {
    const { handleUserSelect, organization } = this.props;
    return (
      <div id='next-organization-managers'>
        { organization.managers &&
          organization.managers.map((userId, index) => (
            <div
              key={index}
              className='next-organization-manager-item'>
              <div
                className='pull-left cursor-pointer'
                onClick={() => handleUserSelect(userId)}>
                <Avatar
                  userId={userId}
                  size='medium'
                  {...this.props}/>
                <div className='next-organization-user-info'>
                  <h4>
                    {this.userName(userId)}
                  </h4>
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
        { organization.direct_reports &&
          organization.direct_reports.map((userId, index) => (
            <div
              onClick={() => handleUserSelect(userId)}
              className='cursor-pointer next-organization-direct-report-item'
              key={index}>
              <Avatar
                userId={userId}
                size='medium'
                {...this.props}/>
              <div className='next-organization-user-info'>
                <h4>
                  {this.userName(userId)}
                </h4>
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
    const { handleUserSelect, id, organization } = this.props;
    return (
      <div id='next-organization-current-person'>
        <div
          onClick={() => handleUserSelect(organization.id)}
          className='cursor-pointer'
          id='next-organization-current-person-user-info-container'>
          <Avatar
            userId={organization.id}
            size='medium'
            {...this.props}/>
          <div className='next-organization-user-info'>
            <h4>
              {this.userName(organization.id)}
              {organization.id === id && ' (You)'}
            </h4>
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
    // const { showManagers } = this.state;

    // let transition = '';
    // if (showManagers)
    //   transition ='next-organization-managers-show';
    // else if (showManagers !== null)
    //   transition = 'next-organization-managers-hide';

    return (
      <div>
        {/* <Container
          id='next-organization-toggle-manager-button-container'
          textAlign='right'>
          <Button
            onClick={() => this.toggleManagers()}>
            {showManagers ? 'Hide Managers' : 'Show Managers'}
          </Button>
        </Container> */}
        <div id='next-organization-container'>
          { organization && this.renderManagers() }
          { organization && this.renderPerson() }
        </div>
      </div>

    );
  }

}


export default Organization;
