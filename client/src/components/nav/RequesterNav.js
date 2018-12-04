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
/*


RequesterNav
Component encapsulating the template for
the sidebar displayed on the requester landing page */


import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import { Button, Icon, Input, Container, Search } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './RequesterNav.css';
import NavList from './NavList';


export default class RequesterNav extends Component {

  static propTypes = {
    memberOf:           PropTypes.array,
    recommendedPacks:   PropTypes.array,
    recommendedRoles:   PropTypes.array,
    requests:           PropTypes.array,
    roleFromId:         PropTypes.func,
    startAnimation:     PropTypes.func,
  };


  renderLists () {
    const {
      recommendedPacks,
      recommendedRoles,
      memberOf,
      requests,
      roleFromId } = this.props;
    return (
      <div id='next-requester-nav-lists-container'>
        <NavList
          listTitle='Your Packs / Roles'
          route='/roles'
          list={memberOf && memberOf.map(roleId => roleFromId(roleId))}/>
        <NavList
          listTitle='Your Requests'
          route='/roles'
          list={requests}/>
        <NavList
          listTitle='Recommended Packs'
          route='/packs'
          list={recommendedPacks}/>
        <NavList
          listTitle='Recommended Roles'
          route='/roles'
          list={recommendedRoles}/>
      </div>
    );
  }


  render () {
    const { startAnimation } = this.props;
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
          <Button
            icon
            as={Link}
            labelPosition='right'
            onClick={startAnimation}
            to='/approval/pending/individual'>
            Switch to Approver
            <Icon name='right arrow'/>
          </Button>
        </div>
      </Container>
    );
  }

}
