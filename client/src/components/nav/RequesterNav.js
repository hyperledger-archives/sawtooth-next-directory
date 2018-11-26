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
import { Button, Icon, Input, Container, Search } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './RequesterNav.css';
import NavList from './NavList';


/**
 *
 * @class         RequesterNav
 * @description   Component encapsulating the template for
 *                the sidebar displayed on the requester landing page
 *
 *
 */
export default class RequesterNav extends Component {

  static propTypes = {
    memberOf:           PropTypes.array,
    recommended:        PropTypes.array,
    requests:           PropTypes.array,
    roleFromId:         PropTypes.func,
  };


  /**
   *
   * Render sidebar hierarchy
   *
   *
   */
  renderLists () {
    const { recommended, memberOf, requests, roleFromId } = this.props;

    return (
      <div id='next-requester-nav-lists-container'>
        <NavList
          dynamic
          listTitle='Your Packs / Roles'
          route='/roles'
          list={memberOf && memberOf.map(roleId => roleFromId(roleId))}/>
        <NavList
          dynamic
          listTitle='Your Requests'
          route='/roles'
          list={requests}/>
        <NavList
          dynamic
          listTitle='Recommended Packs'
          route='/packs'
          list={[]}/>
        <NavList
          dynamic
          listTitle='Recommended Roles'
          route='/roles'
          list={recommended}/>
      </div>
    );
  }


  render () {
    return (
      <Container>

        <Link to='/browse' id='next-requester-nav-browse'>
          <Button animated primary fluid>
            <Button.Content visible>BROWSE</Button.Content>
            <Button.Content hidden><Icon name='arrow right'/></Button.Content>
          </Button>
        </Link>

        <Search
          input={() => <Input icon='search' placeholder='Search...'/>}
          className='next-requester-nav-search'
          category
          loading={false}/>

        { this.renderLists() }

        <div id='next-requester-switch-container'>
          <Button icon labelPosition='right' as={Link} to='/approval/pending/individual'>
            Switch to Approver
            <Icon name='right arrow'/>
          </Button>
        </div>

      </Container>
    );
  }

}
