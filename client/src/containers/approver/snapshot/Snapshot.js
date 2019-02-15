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
import { Button, Header, Image } from 'semantic-ui-react';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';

import './Snapshot.css';
import expireGlyph from 'images/glyph-expire-soon.png';
import SnapshotCard from './SnapshotCard';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


/**
 *
 * @class         Snapshot
 * @description   Snapshot component
 *
 *
 */
class Snapshot extends Component {

  static propTypes = {
    history:                  PropTypes.object,
    openProposalsByRoleCount: PropTypes.number,
    openProposalsCount:       PropTypes.number,
  };


  themes = ['dark', 'gradient'];


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    theme.apply(this.themes);
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      history,
      openProposalsCount,
      openProposalsByRoleCount } = this.props;

    return (
      <div className='snapshot-container'>
        <div className='snapshot-header'>
          <Header
            as='h1'
            id='next-snapshot-header'
            inverted>
            Requests Snapshot
          </Header>
          <Button id='next-snapshot-button'
            onClick={() => history.goBack()}
            icon='close'
            size='huge'/>
        </div>
        <div className='snapshot-sub-container'>
          <SnapshotCard
            count={openProposalsCount || 0}
            status={`Pending across ${
              utils.countLabel(openProposalsByRoleCount, 'role')
            }`}/>
          <SnapshotCard
            image={<Image
              floated='right'
              src={expireGlyph}
              className='next-snapshot-glyph'/>}
            count={0}
            status='About to Expire'/>
          <SnapshotCard
            count={0}
            status='Delegated'/>
          <SnapshotCard
            count={0}
            status='Unattended for 1 week'/>
          <SnapshotCard
            count={0}
            status='Escalated'/>
          <SnapshotCard
            count={0}
            status='Messages'/>
        </div>
      </div>
    );
  }

};


export default withRouter(Snapshot);
