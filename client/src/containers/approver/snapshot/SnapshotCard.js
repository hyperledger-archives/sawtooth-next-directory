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
import { Card, Transition } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './SnapshotCard.css';


/**
 *
 * @class         SnapshotCard
 * @description   SnapshotCard component
 *
 *
 */
class SnapshotCard extends Component {

  static propTypes = {
    count:          PropTypes.number,
    image:          PropTypes.object,
    status:         PropTypes.string,
  };

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { image, count, status} = this.props;

    return (
      <Card id='next-snapshot-card'>
        <Card.Content>
          {image}
          <Transition
            visible={count !== null}
            animation='swing down'
            duration={500}>
            <Card.Header
              id='next-snapshot-card-header'
              content={count}/>
          </Transition>
          <Transition
            visible={count !== null && !!status}
            animation='fade up'
            duration={1000}>
            <Card.Description
              id='next-snapshot-card-description'
              content={status}/>
          </Transition>
        </Card.Content>
      </Card>
    );
  }

}


export default SnapshotCard;
