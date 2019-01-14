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
import { Button, Icon } from 'semantic-ui-react';
import { Link } from 'react-router-dom';
import * as utils from 'services/Utils';
import PropTypes from 'prop-types';

import './PageNotFound.css';


/**
 *
 * @class         PageNotFound
 * @description   Component encapsulating 404 page
 *
 *
 */
export default class PageNotFound extends Component {


  static propTypes = {
    recommendedPacks:        PropTypes.array,
    recommendedRoles:        PropTypes.array,
  }

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { recommendedPacks, recommendedRoles } = this.props;

    return (
      <div className ='error-layout-container'>
        <section>
          <h1 className='error-layout-heading'>
            404
          </h1>
          <p className='error-layout-text'>
            Page not found
          </p>
          <p>
            Oops.. ! you were not supposed to be here. Go back ?
          </p>
          <Link to={utils.createHomeLink(recommendedPacks, recommendedRoles)}>
            <Button animated fluid>
              <Button.Content visible>
                HOME
              </Button.Content>
              <Button.Content hidden>
                <Icon name='arrow left'/>
              </Button.Content>
            </Button>
          </Link>
        </section>
      </div>
    );
  }
};
