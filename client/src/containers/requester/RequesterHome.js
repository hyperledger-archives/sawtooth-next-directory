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
import { Container, Grid } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './RequesterHome.css';
import * as utils from 'services/Utils';


/**
 *
 * @class         RequesterHome
 * @description   Component encapsulating the requester
 *                home, the fallback landing page after login given no
 *                recommended packs or roles
 *
 */
class RequesterHome extends Component {

  static propTypes = {
    activeRole:             PropTypes.object,
    history:                PropTypes.object,
    recommendedPacks:       PropTypes.array,
    recommendedRoles:       PropTypes.array,
  };


  /**
   * Called whenever Redux state changes. Determine home URL and redirect.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { history, recommendedPacks, recommendedRoles } = this.props;
    if (prevProps.recommendedPacks !== recommendedPacks ||
        prevProps.recommendedRoles !== recommendedRoles) {
      history.push(
        utils.createHomeLink(recommendedPacks, recommendedRoles)
      );
    }
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    return (
      <Grid id='next-requester-grid'>
        <Grid.Column
          id='next-requester-grid-track-column'
          width={16}>
          <Container id='next-requester-landing-container'></Container>
        </Grid.Column>
      </Grid>
    );
  }

}


export default RequesterHome;
