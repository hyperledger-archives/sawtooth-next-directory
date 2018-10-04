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
import { Image, List } from 'semantic-ui-react';


import './NavList.css';


/**
 * 
 * @class NavList
 * Component encapsulating a reusable, selectable list suitable
 * for displaying options in navigation components
 * 
 */
export default class NavList extends Component {

  render() {
    const { title, handleClick } = this.props;

    return (
      <div className='next-requester-nav-list-container'>
        <h3>{title}</h3>
        <List selection verticalAlign='middle'>
          <List.Item onClick={() => handleClick('123')}>
            <Image src=''/>
            <List.Content>
              <List.Header>Pack 1</List.Header>
            </List.Content>
          </List.Item>
          <List.Item onClick={() => handleClick('456')}>
            <Image src=''/>
            <List.Content>
              <List.Header>Pack 2</List.Header>
            </List.Content>
          </List.Item>
          <List.Item onClick={() => handleClick('789')}>
            <Image src=''/>
            <List.Content>
              <List.Header>Pack 3</List.Header>
            </List.Content>
          </List.Item>
        </List>
      </div>
    );
  }
  
}
