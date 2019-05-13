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
import { Loader } from 'semantic-ui-react';
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
    getOrganization:    PropTypes.func,
    getUsers:           PropTypes.func,
    handleUserSelect:   PropTypes.func,
    id:                 PropTypes.string,
    organization:       PropTypes.object,
    userFromId:         PropTypes.func,
  }


  state = { showManagers: null };


  /**
   * Entry point to perform tasks required to render component.
   */
  componentDidMount () {
    const {
      activeUser,
      getOrganization,
      handleUserSelect,
      id } = this.props;
    getOrganization(activeUser, activeUser === id);
    handleUserSelect(activeUser);
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const {
      activeUser,
      compact,
      getOrganization,
      getUser,
      getUsers,
      organization,
      users,
      userFromId } = this.props;
    if (prevProps.organization !== organization) {
      let diff = [];
      if (compact) {
        diff = [
          ...organization.direct_reports.slice(0, 5),
          ...organization.managers.slice(0, 5),
        ];
      } else {
        diff = [
          ...organization.direct_reports,
          ...organization.managers,
          ...organization.peers,
        ];
      }
      diff = diff.filter(userId =>
        !users.find(user => userId === user.id)
      );
      getUsers(diff, true);

      const user = userFromId(activeUser);
      if ((user && !user.memberOf) || !user)
        getUser(activeUser);
    }
    if (prevProps.activeUser !== activeUser)
      getOrganization(activeUser);
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
      <div className='clear' id='next-organization-peers'>
        { organization.peers &&
          organization.peers.map((userId, index) => (
            <div
              onClick={() => handleUserSelect(userId)}
              className='cursor-pointer next-organization-peer-item'
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
    const { compact, handleUserSelect, organization } = this.props;

    if (!organization.direct_reports)
      return null;

    const directReports = compact ?
      organization.direct_reports.slice(0, 3) :
      organization.direct_reports;

    return (
      <div id='next-organization-direct-reports'>
        { directReports.map((userId, index) => (
          <div
            onClick={() => handleUserSelect(userId)}
            className='cursor-pointer next-organization-direct-report-item'
            key={index}>
            <Avatar
              userId={userId}
              size='small'
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
    const {
      compact,
      handleUserSelect,
      id,
      organization } = this.props;
    return (
      <div id='next-organization-current-person'>
        <div
          onClick={() => handleUserSelect(organization.id)}
          className={`${compact && 'compact'} ${!compact &&
            'cursor-pointer'}`}
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
    const {
      compact,
      fetchingOrganization,
      organization,
      showPeers } = this.props;

    if (fetchingOrganization) {
      return (
        <Loader
          active={fetchingOrganization}
          id='next-people-organization-loader'
          size='large'>
        </Loader>
      );
    }

    if (organization) {
      if (organization.managers.length === 0 &&
          organization.direct_reports === 0 &&
          organization.peers === 0) {
        if (!compact) {
          return (
            <div className='next-organization-error-message'>
              <h3>
                You are not a member of an organization
              </h3>
            </div>
          );
        }
        return null;
      }
    }

    return (
      <div>
        <div
          id='next-organization-container'
          className={`${compact && 'compact'} ${organization &&
            organization.managers.length === 0 && 'next-organization-empty'}`}>
          { organization && this.renderManagers() }
          { organization && this.renderPerson() }
          { organization && showPeers && this.renderPeers() }
        </div>
      </div>

    );
  }

}


export default Organization;
