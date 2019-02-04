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
  Container,
  Grid,
  Header,
  Icon,
  Placeholder,
  Popup,
  Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './MemberList.css';
import Avatar from 'components/layouts/Avatar';
import * as utils from 'services/Utils';


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


  state = {
    start: 0,
    limit: 5,
    memberList: [],
  };


  /**
   * Entry point to perform tasks required to render component.
   */
  componentDidMount () {
    const { members, owners } = this.props;
    if (!owners || !members) return;
    this.init();
  }


  /**
   * Called whenever Redux state changes. If members or owners changed,
   * get those not loaded in client
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { members, owners } = this.props;
    if (!utils.arraysEqual(prevProps.members, members) ||
        !utils.arraysEqual(prevProps.owners, owners))
      this.init();
  }


  /**
   * Get users needed to display info for owners and members if
   * not already loaded in client.
   */
  init () {
    this.reset();
    this.loadNext(0);
  }


  reset = () => {
    this.setState({ memberList: [] });
  }


  /**
   * Load next set of data
   * @param {number} start Loading start index
   */
  loadNext = (start) => {
    const { getUsers, members, owners } = this.props;
    const { limit } = this.state;
    if (start === undefined || start === null)
      start = this.state.start;

    const join = [...new Set([...owners, ...members])];
    join && getUsers(join.slice(start, start + limit), true);

    this.setState(prevState => ({
      memberList: [
        ...prevState.memberList,
        ...new Set([...join.slice(start, start + limit)]),
      ],
      start: start + limit,
    }));
  }


  /**
   * Render segment containing user info
   * @param {string} userId User ID
   * @param {boolean} isOwner If user is owner
   * @returns {JSX}
   */
  renderUserSegment (userId, isOwner) {
    const { userFromId } = this.props;
    const user = userFromId(userId);

    if (!user) {
      return (
        <Grid.Column
          key={userId}
          largeScreen={8}
          widescreen={5}>
          <Placeholder fluid>
            <Placeholder.Header image>
              <Placeholder.Line length='very long'/>
              <Placeholder.Line length='medium'/>
            </Placeholder.Header>
          </Placeholder>
        </Grid.Column>
      );
    }

    return (
      <Grid.Column key={userId} largeScreen={8} widescreen={5}>
        <Segment className='avatar no-padding minimal'>
          { isOwner ?
            <Popup trigger={<Icon
              name='shield'
              className='pull-right'
              color='green'/>} content='Owner'
            id='next-member-list-owner-popup-box'
            position='top center' inverted/> :
            <Popup trigger={<Icon
              name='key'
              className='pull-right'
              color='grey'/>} content='Member'
            id='next-member-list-member-popup-box'
            position='top center' inverted/>
          }
          <Header as='h4' className='next-member-list-user-info'>
            <div>
              <Avatar userId={userId} size='medium' {...this.props}/>
            </div>
            <div>
              {(user && user.name) || 'Unnamed'}
              {isOwner && ' (Owner)'}
              <Header.Subheader>
                {user && user.email}
              </Header.Subheader>
            </div>
          </Header>

        </Segment>
      </Grid.Column>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { members, owners } = this.props;
    const { limit, memberList } = this.state;
    const join = [...new Set([...owners, ...members])];

    return (
      <div>
        <Grid columns={3} stackable>
          { memberList.map(userId => {
            const isOwner = owners && owners.includes(userId);
            return this.renderUserSegment(userId, isOwner);
          }) }
        </Grid>
        { join &&
          join.length > limit &&
          memberList.length !== join.length &&
          <Container
            id='next-member-list-load-next-button'
            textAlign='center'>
            <Button size='large' onClick={() => this.loadNext()}>
              Load More
            </Button>
          </Container>
        }
      </div>
    );
  }

}


export default MemberList;
