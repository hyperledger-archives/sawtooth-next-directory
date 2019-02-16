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


import './ManageDelegations.css';
import glyph from 'images/glyph-role.png';
import TrackHeader from 'components/layouts/TrackHeader';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


/**
 *
 * @class         ManageDelegations
 * @description   Manage component
 *
 */
class ManageDelegations extends Component {

  themes = ['minimal', 'contrast', 'magenta'];


  state = {
    start: 0,
    limit: 25,
    delegationList: [],
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
    const { delegations } = this.props;
    if (!utils.arraysEqual(prevProps.delegations, delegations))
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
    const { delegations } = this.props;
    this.reset();
    delegations && this.loadNext(0);
  }


  reset = () => {
    this.setState({ delegationList: [] });
  }


  /**
   * Render a delegation card
   * @param {string} delegationId Delegation ID
   * @returns {JSX}
   */
  renderDelegationCard (delegationId) {
    const { delegationFromId } = this.props;
    const delegation = delegationFromId(delegationId);

    if (!delegation) {
      return (
        <Grid.Column key={delegationId}>
          <Placeholder fluid key={delegationId}>
            <Placeholder.Header image>
              <Placeholder.Line length='full'/>
              <Placeholder.Line length='long'/>
            </Placeholder.Header>
          </Placeholder>
        </Grid.Column>
      );
    }

    return (
      <Grid.Column key={delegationId}>
        <Card
          fluid
          className='minimal medium'>
          <Header as='h3'>
            <div>
              <Image size='mini' src={glyph}/>
            </div>
            <div>
              {utils.countLabel(delegation.roles.length, 'role')}
              <Header.Subheader>
                <div>
                  {'Delegated to '}
                  {delegation.delegate}
                </div>
                {delegation.delegate_message}
              </Header.Subheader>
            </div>
          </Header>
          <Card.Content extra>
            From
            {delegation.start_date}
            {' to '}
            {delegation.end_date}
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
    const { getDelegations, delegations } = this.props;
    const { limit } = this.state;
    if (start === undefined || start === null)
      start = this.state.start;

    delegations && getDelegations(delegations.slice(start, start + limit));
    this.setState(prevState => ({
      delegationList: [
        ...prevState.delegationList,
        ...delegations.slice(start, start + limit),
      ],
      start: start + limit,
    }));
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { delegations } = this.props;
    const { delegationList } = this.state;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Delegations'
            breadcrumb={[
              {name: 'Manage', slug: '/approval/manage'},
              {name: 'Delegations', slug: '/approval/manage/delegations'},
            ]}
            button={() =>
              <Button
                id='next-approver-manage-delegations-create-button'
                icon='add'
                size='huge'
                content='Create Delegation'
                labelPosition='left'
                as={Link}
                to='delegations/create'/>}
            {...this.props}/>
          <div id='next-approver-manage-delegations-content'>
            { delegations && delegations.length > 0 &&
              <h3>
                {utils.countLabel(delegations.length, 'delegation')}
              </h3>
            }
            { delegations && delegations.length === 0 &&
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  You haven&#39;t created any delegations
                </Header.Content>
              </Header>
            }
            <Grid columns={1} stackable>
              { delegationList.map(delegationId =>
                this.renderDelegationCard(delegationId)
              ) }
            </Grid>
            { delegations &&
              delegations.length > 25 &&
              delegationList.length !== delegations.length &&
              <Container
                id='next-manage-delegations-load-next-button'
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


export default ManageDelegations;
