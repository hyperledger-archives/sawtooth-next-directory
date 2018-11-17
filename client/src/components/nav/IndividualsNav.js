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
import { Menu } from 'semantic-ui-react';
import './IndividualsNav.css';


/**
 *
 * @class         IndividualsNav
 * @description   Component encapsulating the template for Individuals
 *                navigation header
 *
 *
 */
export default class IndividualsNav extends Component {

  render () {
    const { activeIndex, setFlow } = this.props;

    return (
      <div id='next-individuals-nav'>
        <Menu compact>
          <Menu.Item
            name='roles'
            active={activeIndex === 0}
            onClick={() => setFlow(0)}>
            Roles
          </Menu.Item>
          <Menu.Item
            name='people'
            active={activeIndex === 1}
            onClick={() => setFlow(1)}>
            People
          </Menu.Item>
        </Menu>
      </div>
    );
  }

}
