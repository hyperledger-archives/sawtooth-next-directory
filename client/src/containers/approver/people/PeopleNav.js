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
import { Menu, Input, Search } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './PeopleNav.css';


/**
 *
 * @class         PeopleNav
 * @description   Component encapsulating the template for the People
 *                screen navigation header
 *
 *
 */
class PeopleNav extends Component {

  static propTypes = {
    activeIndex:        PropTypes.number,
    setFlow:            PropTypes.func,
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { activeIndex, setFlow } = this.props;

    return (
      <div id='next-people-nav'>
        <Menu compact>
          <Menu.Item
            name='organization'
            active={activeIndex === 0}
            onClick={() => setFlow(0)}>
            All People
          </Menu.Item>
          <Menu.Item
            name='people'
            active={activeIndex === 1}
            onClick={() => setFlow(1)}>
            Organization
          </Menu.Item>
        </Menu>
        <Search
          fluid
          input={() => <Input
            fluid
            size='large'
            icon='search'
            placeholder='Search...'/>}
          className='next-people-search'
          category
          loading={false}/>
      </div>
    );
  }

}


export default PeopleNav;
