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
  Grid,
  Header,
  Image,
  Placeholder } from 'semantic-ui-react';

import './ManagePacks.css';
import glyph from 'images/header-glyph-pack.png';
import TrackHeader from 'components/layouts/TrackHeader';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


/**
 *
 * @class         ManagePacks
 * @description   Manage component
 *
 */
class ManagePacks extends Component {

  themes = ['minimal', 'contrast', 'magenta'];


  state = {
    start: 0,
    limit: 25,
    packList: [],
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
    const { ownedPacks } = this.props;
    if (!utils.arraysEqual(prevProps.ownedPacks, ownedPacks))
      this.init();
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Determine which packs are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const { ownedPacks } = this.props;
    this.reset();
    ownedPacks && this.loadNext(0);
  }


  reset = () => {
    this.setState({ packList: [] });
  }


  /**
   * Render a pack card
   * @param {string} packId Pack ID
   * @returns {JSX}
   */
  renderPackCard (packId) {
    const { packFromId } = this.props;
    const pack = packFromId(packId);

    if (!pack) {
      return (
        <Grid.Column key={packId}>
          <Placeholder fluid key={packId}>
            <Placeholder.Header image>
              <Placeholder.Line length='full'/>
              <Placeholder.Line length='long'/>
            </Placeholder.Header>
          </Placeholder>
        </Grid.Column>
      );
    }

    return (
      <Grid.Column key={packId}>
        <Card
          fluid
          as={Link}
          to={`/packs/${packId}`}
          className='minimal medium'>
          <Header as='h3'>
            <div>
              <Image size='mini' src={glyph}/>
            </div>
            <div>
              {pack.name}
              <Header.Subheader>
                {pack.description || 'No description available.'}
              </Header.Subheader>
            </div>
          </Header>
          <Card.Content extra>
            {pack && utils.countLabel(pack.roles.length, 'role')}
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
    const { getPacks, ownedPacks } = this.props;
    const { limit } = this.state;
    if (start === undefined || start === null)
      start = this.state.start;

    ownedPacks && getPacks(ownedPacks.slice(start, start + limit));
    this.setState(prevState => ({
      packList: [
        ...prevState.packList,
        ...ownedPacks.slice(start, start + limit),
      ],
      start: start + limit,
    }));
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { ownedPacks } = this.props;
    const { packList } = this.state;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Packs'
            breadcrumb={[
              {name: 'Manage', slug: '/approval/manage'},
              {name: 'Packs', slug: '/approval/manage/packs'},
            ]}
            button={() =>
              <Button
                id='next-approver-manage-packs-create-button'
                icon='add'
                size='huge'
                content='Create New Pack'
                labelPosition='left'
                as={Link}
                to='packs/create'/>}
            {...this.props}/>
          <div id='next-approver-manage-packs-content'>
            { ownedPacks && ownedPacks.length > 0 &&
              <h3>
                {ownedPacks && utils.countLabel(ownedPacks.length, 'pack')}
              </h3>
            }
            { ownedPacks && ownedPacks.length === 0 &&
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  You haven&apos;t created any packs
                </Header.Content>
              </Header>
            }
            <Grid columns={1} stackable>
              { packList.map(packId =>
                this.renderPackCard(packId)
              ) }
            </Grid>
            { ownedPacks &&
              ownedPacks.length > 25 &&
              packList.length !== ownedPacks.length &&
              <div id='next-manage-packs-load-next-button'>
                <Button size='large' onClick={() => this.loadNext()}>
                  Load More
                </Button>
              </div>
            }
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default ManagePacks;
