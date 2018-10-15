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
import { Container, Search } from 'semantic-ui-react';


import NavList from './NavList';
import './ApproverNav.css';


/**
 * 
 * @class ApproverNav
 * Component encapsulating the template for the sidebar displayed
 * on the approver landing page.
 * 
 */
export default class ApproverNav extends Component {

  /**
   * 
   * Render sidebar hierarchy
   * 
   */
  renderLists () {
    return (
      <div id='next-approver-nav-lists-container'>
        <NavList
          listTitle='Pending'
          list={[
            'Batch',
            'Roles',
            'Individuals',
            'Frequent',
            'About to Expire'
          ]}
          route='/approval-home/pending'/>
        <NavList
          listTitle='Approved'
          list={null}
          route='/approval-home/approved'/>
        <NavList
          listTitle='Expired'
          list={null}
          route='/approval-home/expired'/>
        <NavList
          listTitle='Manage Groups'
          list={null}
          route='/approval-home/manage-groups'/>
        <NavList
          listTitle='People'
          list={null}
          route='/approval-home/people'/>
      </div>
    );
  }


  render () {
    return (
      <Container>

        <Search
          className='next-approver-nav-search'
          category
          loading={false}/>

        { this.renderLists() }

        <Link to='/home' id='next-switch-approver-link'>
          Switch to Requester
        </Link>

      </Container>
    );
  }

}
