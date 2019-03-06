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
import {
  Button,
  Checkbox,
  Dropdown,
  Menu,
  Input,
  Search } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './IndividualNav.css';


/**
 *
 * @class         IndividualNav
 * @description   Component encapsulating the template for Individual
 *                Requests navigation header
 *
 *
 */
class IndividualNav extends Component {

  static propTypes = {
    activeIndex:        PropTypes.number,
    allSelected:        PropTypes.bool,
    handleSelect:       PropTypes.func,
    setFlow:            PropTypes.func,
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      activeIndex,
      allSelected,
      handleSelect,
      setFlow } = this.props;

    return (
      <div id='next-individual-nav'>
        <Menu compact>
          <Menu.Item
            name='roles'
            id='next-individual-nav-roles-click'
            active={activeIndex === 0}
            onClick={() => setFlow(0)}>
            Roles
          </Menu.Item>
          <Menu.Item
            name='people'
            id='next-individual-nav-people-click'
            active={activeIndex === 1}
            onClick={() => setFlow(1)}>
            People
          </Menu.Item>
          <Menu.Item
            name='table'
            id='next-individual-nav-table-click'
            active={activeIndex === 2}
            onClick={() => setFlow(2)}>
            Table
          </Menu.Item>
        </Menu>
        <div id='next-individual-nav-select-dropdown'>
          <Checkbox
            checked={allSelected}
            onChange={handleSelect}/>
          <Dropdown floating trigger={<Button basic/>}>
            <Dropdown.Menu>
              <Dropdown.Item
                text='All'
                onClick={() => handleSelect(undefined, { checked: true })}/>
              <Dropdown.Item
                text='None'
                onClick={() => handleSelect(undefined, { checked: false })}/>
            </Dropdown.Menu>
          </Dropdown>
        </div>
        <Search
          fluid
          input={() => <Input
            fluid
            size='large'
            icon='search'
            placeholder='Search...'/>}
          className='next-individual-search'
          category
          loading={false}/>
      </div>
    );
  }

}


export default IndividualNav;
