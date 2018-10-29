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
import { Button, Container, Search, Icon } from 'semantic-ui-react';


import './RequesterNav.css';
import NavList from './NavList';


/**
 *
 * @class RequesterNav
 * Component encapsulating the template for the sidebar displayed
 * on the requester landing page.
 *
 */
export default class RequesterNav extends Component {



  /**
   *
   * Render sidebar hierarchy
   *
   */
  renderLists () {
    const { recommended, packs, requests } = this.props;

    return (
      <div id='next-requester-nav-lists-container'>
        <NavList
          dynamic
          listTitle='Your Packs / Roles'
          route='/home/packs'
          list={packs}/>
        <NavList
          dynamic
          listTitle='Your Requests'
          route='/home/requests'
          list={requests}/>
        <NavList
          dynamic
          listTitle='Recommended Packs'
          route='/home/recommended-packs'
          list={recommended}/>
        <NavList
          dynamic
          listTitle='Recommended Roles'
          route='/home/recommended-roles'
          list={recommended}/>
      </div>
    );
  }


  render () {
    const { logout } = this.props;

    return (
      <Container>

        <Link to='/browse'>
          <Button animated secondary fluid id='next-browse-button'>
            <Button.Content visible>BROWSE</Button.Content>
            <Button.Content hidden><Icon name='arrow right'/></Button.Content>
          </Button>
        </Link>

        <Search
          className='next-requester-nav-search'
          category
          loading={false}/>

        { this.renderLists() }

        <Link to='/approval-home' id='next-switch-requester-link'>
          Switch to Approver
        </Link>
        
        <Button onClick={() => logout()} animated secondary id="next-logout-button">
          <Button.Content visible>Logout</Button.Content>
          <Button.Content hidden><Icon name='log out'/></Button.Content>
        </Button>

        <Button onClick={() => logout()} animated secondary id="next-logout-button">
          <Button.Content visible>Logout</Button.Content>
          <Button.Content hidden><Icon name='log out'/></Button.Content>
        </Button>

      </Container>
    );
  }

}
