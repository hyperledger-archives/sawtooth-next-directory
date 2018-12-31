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
import { Grid, Header, Icon, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './MemberList.css';
import Avatar from 'components/layouts/Avatar';


/**
 *
 * @class         MemberList
 * @description   Component encapsulating the member list
 *
 *
 */
class MemberList extends Component {

  static propTypes = {
    getUsers:           PropTypes.func,
    members:            PropTypes.array,
    owners:             PropTypes.array,
    users:              PropTypes.array,
  }


  /**
   * Entry point to perform tasks required to render component.
   * Get users needed to display info for owners and members if
   * not already loaded in client
   */
  componentDidMount   () {
    const { getUsers, members, owners, users } = this.props;
    if (!owners || !members) return;

    const join = [...owners, ...members];

    const diff = users &&
      join.filter(userId =>
        users.find(user => user.id !== userId));

    diff && getUsers(diff);
  }


  /**
   * Called whenever Redux state changes. If members or owners changed,
   * get those not loaded in client
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { getUsers, members, owners, users } = this.props;

    if (prevProps.members !== members || prevProps.owners !== owners) {
      const join = [...members, ...owners];
      const diff = users &&
        join.filter(userId =>
          users.find(user => user.id !== userId));

      diff && getUsers(diff);
    }
  }


  /**
   * Render segment containing user info
   * @param {string} userId User ID
   * @param {boolean} isOwner If user is owner
   * @returns {JSX}
   */
  renderUserSegment (userId, isOwner) {
    const { users } = this.props;

    if (users) {
      const user = users.find((user) => user.id === userId);
      if (!user) {
        return (
          <Grid.Column key={userId} largeScreen={8} widescreen={5}>
            <Segment className='avatar secondary no-padding minimal'>
              <Header as='h4' className='next-member-list-user-info'>
                <div>
                  <Avatar userId={userId} size='medium' {...this.props}/>
                </div>
                <div>
                  Unavailable
                </div>
              </Header>
            </Segment>
          </Grid.Column>
        );
      }

      return (
        user &&
        <Grid.Column key={userId} largeScreen={8} widescreen={5}>
          <Segment className='avatar no-padding minimal'>
            { isOwner ?
              <Icon
                name='shield'
                className='pull-right'
                color='green'/> :
              <Icon
                name='key'
                className='pull-right'
                color='grey'/>
            }
            <Header as='h4' className='next-member-list-user-info'>
              <div>
                <Avatar userId={userId} size='medium' {...this.props}/>
              </div>
              <div>
                {user && user.name}
                <Header.Subheader>
                  {user && user.email}
                </Header.Subheader>
              </div>
            </Header>

          </Segment>
        </Grid.Column>
      );
    }
    return null;
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { members, owners } = this.props;

    return (
      <div>
        <Grid columns={3} stackable>
          { owners && owners.map((owner) => (
            this.renderUserSegment(owner, true)
          )) }

          { members && members.map((member) => (
            this.renderUserSegment(member)
          )) }
        </Grid>

      </div>
    );
  }

}


export default MemberList;
