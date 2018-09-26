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
import { Link } from 'react-router-dom'
import { Container, List, Image, Search } from 'semantic-ui-react';


import './styles/ApproverNav.css';


/**
 * 
 * @class ApproverNav
 * Component encapsulating the template for the sidebar displayed
 * on the approver landing page.
 * 
 */
export default class ApproverNav extends Component {

  render () {
    return (
      <Container>
        <Search className='next-approver-nav-search' category loading={false}/>
        <h3>Pending</h3>

        <List selection verticalAlign='middle'>
          <Link to='/approval-home/batch'>
            <List.Item>
              <Image src=''/>
              <List.Content>
                <List.Header>Batch</List.Header>
              </List.Content>
            </List.Item>
          </Link>
          <Link to='/approval-home/roles'>
            <List.Item>
              <Image src=''/>
              <List.Content>
                <List.Header>Roles</List.Header>
              </List.Content>
            </List.Item>
          </Link>
          <Link to='/approval-home/individuals'>
            <List.Item>
              <Image src=''/>
              <List.Content>
                <List.Header>Individuals</List.Header>
              </List.Content>
            </List.Item>
          </Link>
          <Link to='/approval-home/frequent'>
            <List.Item>
              <Image src=''/>
              <List.Content>
                <List.Header>Frequent</List.Header>
              </List.Content>
            </List.Item>
          </Link>
          <Link to='/approval-home/expiring'>
            <List.Item>
              <Image src=''/>
              <List.Content>
                <List.Header>About to Expire</List.Header>
              </List.Content>
            </List.Item>
          </Link>
        </List>

        <h3>Approved</h3>
        <h3>Expired</h3>
        <h3>Manage Groups</h3>
        <h3>People</h3>

        <Link to='/home' id='next-switch-approver-link'>Switch to Requester</Link>

      </Container>
    );
  }

}
