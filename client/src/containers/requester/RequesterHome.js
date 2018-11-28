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
import * as utils from '../../services/Utils';


/**
 *
 * @class         RequesterHome
 * @description   Component encapsulating the requester
 *                home, the default landing page after login
 *
 *
 */
export default class RequesterHome extends Component {

  static propTypes = {
    activeRole:           PropTypes.object,
    history:              PropTypes.object,
    recommended:          PropTypes.array,
  };


  componentDidUpdate (prevProps) {
    const { history, recommended } = this.props;
    const homeLink = recommended && recommended[0] ?
      `/roles/${utils.createSlug(recommended[0].name)}` :
      undefined;

    homeLink && history.push(homeLink);
  }


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
