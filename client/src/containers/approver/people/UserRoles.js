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
import { Link } from 'react-router-dom';
import {
  Button,
  Card,
  Container,
  Grid,
  Header,
  Image,
  Placeholder } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './UserRoles.css';
import glyph from 'images/glyph-role.png';
import * as utils from 'services/Utils';


/**
 *
 * @class         UserRoles
 * @description   Manage component
 *
 */
class UserRoles extends Component {

  static propTypes = {
    activeUser:            PropTypes.string,
    getRoles:              PropTypes.func,
    roleFromId:            PropTypes.func,
    userFromId:            PropTypes.func,
  };


  state = {
    start: 0,
    limit: 10,
    roleList: [],
  };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { activeUser } = this.props;
    if (prevProps.activeUser !== activeUser)
      this.init();
  }


  /**
   * Determine which roles are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const { activeUser, userFromId } = this.props;
    this.reset();

    const user = userFromId(activeUser);
    if (!user) return;

    user.memberOf && user.memberOf.length > 0 && this.loadNext(0);
  }


  reset = () => {
    this.setState({ roleList: [] });
  }


  /**
   * Render a role card
   * @param {string} roleId Role ID
   * @returns {JSX}
   */
  renderRoleCard (roleId) {
    const { roleFromId } = this.props;
    const role = roleFromId(roleId);

    if (!role) {
      return (
        <Grid.Column key={roleId}>
          <Placeholder
            fluid
            key={roleId}
            className='contrast'>
            <Placeholder.Header image>
              <Placeholder.Line length='full'/>
              <Placeholder.Line length='long'/>
            </Placeholder.Header>
          </Placeholder>
        </Grid.Column>
      );
    }

    return (
      <Grid.Column className='next-people-user-roles-item' key={roleId}>
        <Card
          fluid
          as={Link}
          to={`/roles/${roleId}`}
          className='minimal medium'>
          <Header as='h3'>
            <div>
              <Image size='mini' src={glyph}/>
            </div>
            <div>
              {role.name}
              <Header.Subheader>
                {role.description || 'No description available.'}
              </Header.Subheader>
            </div>
          </Header>
          <Card.Content extra>
            { role &&
              utils.countLabel(role.members.length, 'member')
            }
          </Card.Content>
        </Card>
      </Grid.Column>
    );
  }


  /**
   * Load next set of data
   * @param {number} start Loading start index
   */
  loadNext = (start) => {
    const { activeUser, getRoles, userFromId } = this.props;
    const { limit } = this.state;

    const user = userFromId(activeUser);
    if (!user) return;

    if (start === undefined || start === null)
      start = this.state.start;

    user.memberOf && getRoles(user.memberOf.slice(start, start + limit));
    this.setState(prevState => ({
      roleList: [
        ...prevState.roleList,
        ...user.memberOf.slice(start, start + limit),
      ],
      start: start + limit,
    }));
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { activeUser, userFromId } = this.props;
    const { roleList, limit } = this.state;

    const user = userFromId(activeUser);
    if (!user) return null;

    return (
      <Grid columns={1} stackable>
        <div id='next-people-user-roles-content'>
          { roleList.map(roleId => {
            return this.renderRoleCard(roleId);
          }) }
          { user.memberOf &&
            user.memberOf.length > limit &&
            roleList.length !== user.memberOf.length &&
            <Container
              id='next-people-user-roles-load-next-button'
              textAlign='center'>
              <Button size='large' onClick={() => this.loadNext()}>
                Load More
              </Button>
            </Container>
          }
        </div>
      </Grid>
    );
  }

}


export default UserRoles;
