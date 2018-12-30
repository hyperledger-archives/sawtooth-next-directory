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
import { Button, Grid, Header, Image, Segment } from 'semantic-ui-react';


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

  themes = ['minimal', 'contrast'];


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
    const {
      ownedPacks,
      getPacks,
      packs } = this.props;

    const diff = packs ?
      ownedPacks &&
      ownedPacks.filter(
        packId => !packs.find(pack => pack.id === packId)
      ) :
      ownedPacks;
    diff && diff.length > 0 && getPacks(diff);
  }


  /**
   * Get pack name from pack ID
   * @param {string} packId Pack ID
   * @returns {string}
   */
  packName = (packId) => {
    const { packFromId } = this.props;
    const pack = packFromId(packId);
    return pack && pack.name;
  };


  /**
   * Render a list of packs created by the user
   * @returns {JSX}
   */
  renderPacks () {
    const { ownedPacks } = this.props;
    return (
      <div>
        { ownedPacks && ownedPacks.map(packId => (
          this.packName(packId) &&
          <Segment padded className='minimal' key={packId}>
            <Header as='h3'>
              <Image src={glyph} size='mini'/>
              <div>{this.packName(packId)}</div>
            </Header>
          </Segment>
        ))}
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { ownedPacks } = this.props;
    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            title='Packs'
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
            { ownedPacks && ownedPacks.length > 0 ?
              <h2>Packs You&apos;ve Created</h2> :
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  You haven&apos;t created any packs
                </Header.Content>
              </Header>
            }
            {this.renderPacks()}
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default ManagePacks;
