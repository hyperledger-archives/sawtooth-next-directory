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
import { Link } from 'react-router-dom';
import {
  Button,
  Card,
  Container,
  Grid,
  Header,
  Image,
  Placeholder } from 'semantic-ui-react';

import './ManageRoles.css';
import glyph from 'images/header-glyph-role.png';
import TrackHeader from 'components/layouts/TrackHeader';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


/**
 *
 * @class         ManageRoles
 * @description   Manage component
 *
 */
class ManageRoles extends Component {

  themes = ['minimal', 'contrast', 'magenta'];


  state = {
    start: 0,
    limit: 25,
    roleList: [],
  };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    theme.apply(this.themes);
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { ownedRoles } = this.props;
    if (!utils.arraysEqual(prevProps.ownedRoles, ownedRoles))
      this.init();
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Determine which roles are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const { ownedRoles } = this.props;
    this.reset();
    ownedRoles && this.loadNext(0);
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
          <Placeholder fluid key={roleId}>
            <Placeholder.Header image>
              <Placeholder.Line length='full'/>
              <Placeholder.Line length='long'/>
            </Placeholder.Header>
          </Placeholder>
        </Grid.Column>
      );
    }

    return (
      <Grid.Column key={roleId}>
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
            { role && utils.countLabel([
              ...role.members,
              ...role.owners,
            ]
              .length, 'member', true)
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
    const { getRoles, ownedRoles } = this.props;
    const { limit } = this.state;
    if (start === undefined || start === null)
      start = this.state.start;

    ownedRoles && getRoles(ownedRoles.slice(start, start + limit));
    this.setState(prevState => ({
      roleList: [
        ...prevState.roleList,
        ...ownedRoles.slice(start, start + limit),
      ],
      start: start + limit,
    }));
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { ownedRoles } = this.props;
    const { roleList } = this.state;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Roles'
            breadcrumb={[
              {name: 'Manage', slug: '/approval/manage'},
              {name: 'Roles', slug: '/approval/manage/roles'},
            ]}
            button={() =>
              <Button
                id='next-approver-manage-roles-create-button'
                icon='add'
                size='huge'
                content='Create New Role'
                labelPosition='left'
                as={Link}
                to='roles/create'/>}
            {...this.props}/>
          <div id='next-approver-manage-roles-content'>
            { ownedRoles && ownedRoles.length > 0 &&
              <h3>
                {ownedRoles && utils.countLabel(ownedRoles.length, 'role')}
              </h3>
            }
            { ownedRoles && ownedRoles.length === 0 &&
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  You haven&apos;t created any roles
                </Header.Content>
              </Header>
            }
            <Grid columns={1} stackable>
              { roleList.map(roleId =>
                this.renderRoleCard(roleId)
              ) }
            </Grid>
            { ownedRoles &&
              ownedRoles.length > 25 &&
              roleList.length !== ownedRoles.length &&
              <Container
                id='next-manage-roles-load-next-button'
                textAlign='center'>
                <Button size='large' onClick={() => this.loadNext()}>
                  Load More
                </Button>
              </Container>
            }
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default ManageRoles;
