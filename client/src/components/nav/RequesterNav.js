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
import { Button, Container, Search } from 'semantic-ui-react';


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
   * @param id Pack Id
   * 
   */
  getPack = (id) => {
    const { getPackRequest } = this.props;
    getPackRequest(id);
  }


  render () {
    return (
      <Container>
        <Link to='/browse'>
          <Button fluid>Browse Packs/Roles</Button>
        </Link>
        <Search className='next-requester-nav-search' category loading={false}/>
        <NavList title='Your Requests' handleClick={this.getPack}/>
        <NavList title='Recommended Packs' handleClick={this.getPack}/>
        <NavList title='Your Packs' handleClick={this.getPack}/>
        <Link to='/approval-home' id='next-switch-requester-link'>Switch to Approver</Link>
      </Container>
    );
  }

}
