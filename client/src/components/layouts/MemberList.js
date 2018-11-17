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
import { Grid, Header, Icon, Image, Segment } from 'semantic-ui-react';
import './MemberList.css';


/**
 *
 * @class         MemberList
 * @description   Component encapsulating the member list
 *
 *
 */
export default class MemberList extends Component {

  /**
   *
   * Hydrate data
   *
   *
   */
  componentDidMount () {
    const { getUsers, members, owners, users } = this.props;
    if (!owners || !members) return;

    const join = [...owners, ...members];

    const diff = users &&
      join.filter(userId =>
        users.find(user => user.id !== userId));

    diff && getUsers(diff);
  }


  componentWillReceiveProps (newProps) {
    const { getUsers, members, owners, users } = this.props;

    if (newProps.members !== members || newProps.owners !== owners) {
      const join = [...newProps.members, ...newProps.owners];
      const diff = users &&
        join.filter(userId =>
          users.find(user => user.id !== userId));

      diff && getUsers(diff);
    }
  }


  renderUserSegment (userId, isOwner) {
    const { users } = this.props;

    if (!users) return null;
    const user = users.find((user) => user.id === userId);

    return (
      user &&
        <Grid.Column key={userId} largeScreen={8} widescreen={5}>
          <Segment padded raised>
            <Icon
              name='shield'
              className='pull-right'
              color={ isOwner ? 'red' : 'blue' }/>

            <Header as='h4' className='next-member-list-user-info'>
              <div>
                <Image src='http://i.pravatar.cc/300' avatar/>
              </div>
              <div>
                {user && user.name}
                <Header.Subheader>{user && user.email}</Header.Subheader>
              </div>
            </Header>

          </Segment>
        </Grid.Column>
    );
  }


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
