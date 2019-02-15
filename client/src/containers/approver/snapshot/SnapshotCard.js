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
import { Card, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './SnapshotCard.css';
import myIcon from 'images/icon-expired@3x.png';


/**
 *
 * @class         SnapshotCard
 * @description   SnapshotCard component
 *
 *
 */
class SnapshotCard extends Component {

  static propTypes = {
    isimageNeeded:  PropTypes.bool,
    roleCount:      PropTypes.string,
    roleStatus:     PropTypes.string,
  };

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { roleCount, roleStatus, isimageNeeded} = this.props;

    return (
      <Card id='next-snapshot-card'>
        <Card.Content>
          { isimageNeeded ? <Image floated='right'
            src={ myIcon } id='next-expired-image'/> : ''}
          <Card.Header id='next-snapshotcard-header' content={roleCount}/>
          <Card.Description id='next-snapshotcard-description'
            content={roleStatus}/>
        </Card.Content>
      </Card>
    );
  }

}


export default SnapshotCard;
