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
import { Link, withRouter } from 'react-router-dom';
import { Button, Header, Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './NotFound.css';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


/**
 *
 * @class         NotFound
 * @description   Component encapsulating 404 screen
 *
 *
 */
class NotFound extends Component {

  static propTypes = {
    history:                 PropTypes.object,
    recommendedPacks:        PropTypes.array,
    recommendedRoles:        PropTypes.array,
  }


  themes = ['dark'];


  /**
   * Entry point to perform tasks required to render
   * component. On load, get roles
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
   * Navigate to previous location
   */
  goBack () {
    const {
      history,
      recommendedPacks,
      recommendedRoles } = this.props;

    history.length < 3 ?
      history.push(
        utils.createHomeLink(recommendedPacks, recommendedRoles)
      ) :
      history.goBack();
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      recommendedPacks,
      recommendedRoles } = this.props;

    return (
      <div id='next-not-found-container'>
        <Header as='h1'>
          Oops.
          <Header.Subheader>
            This page doesn&#39;t seem to exist.
          </Header.Subheader>
        </Header>
        <div id='next-not-found-actions'>
          <Button
            animated
            primary
            fluid
            onClick={() => this.goBack()}>
            <Button.Content visible>
              Go back
            </Button.Content>
            <Button.Content hidden>
              <Icon name='arrow left'/>
            </Button.Content>
          </Button>
          <Button
            animated
            inverted
            fluid
            as={Link}
            to={utils.createHomeLink(recommendedPacks, recommendedRoles)}>
            <Button.Content visible>
              Return home
            </Button.Content>
            <Button.Content hidden>
              <Icon name='arrow right'/>
            </Button.Content>
          </Button>
        </div>
      </div>
    );
  }

}


export default withRouter(NotFound);
