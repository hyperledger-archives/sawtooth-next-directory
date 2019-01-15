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
import { Link, withRouter } from 'react-router-dom';
import {
  Button,
  Icon,
  Container,
  Input,
  Search } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './ApproverNav.css';
import NavList from './NavList';


/**
 *
 * @class         ApproverNav
 * @description   Component encapsulating the template for
 *                the sidebar displayed on the approver landing page
 *
 */
class ApproverNav extends Component {

  static propTypes = {
    location:               PropTypes.object,
    onBehalfOf:             PropTypes.string,
    openProposalsCount:     PropTypes.number,
    recommendedPacks:       PropTypes.array,
    recommendedRoles:       PropTypes.array,
    startAnimation:         PropTypes.func,
    users:                  PropTypes.array,
  };


  /**
   * Determine if nav item is active
   * @param {object} name Nav item name
   * @returns {boolean}
   */
  isItemActive = (name) => {
    const { location } = this.props;
    return location.pathname.includes(`/${name}`);
  };


  /**
   * Render each list of sidebar groups by passing the root
   * route, title, and array of items to NavList
   * @returns {JSX}
   */
  renderLists () {
    const { openProposalsCount } = this.props;

    return (
      <div
        id='next-approver-nav-lists-container'
        className='nav-list'>
        <NavList
          disabled
          listTitle='Pending'
          labels={[
            openProposalsCount,
            null,
          ]}
          list={[
            { name: 'Individual', slug: 'individual' },
            { name: 'About to Expire', slug: 'about-to-expire' },
          ]}
          route='/approval/pending'/>
        <h4 className={`hover ${this.isItemActive('delegated') ?
          'active' : ''}`}>
          <Link to='/approval/delegated'>
            Delegated
          </Link>
        </h4>
        <h4 className={`hover ${this.isItemActive('approved') ?
          'active' : ''}`}>
          <Link to='/approval/approved'>
            Approved
          </Link>
        </h4>
        <h4 className={`hover ${this.isItemActive('rejected') ?
          'active' : ''}`}>
          <Link to='/approval/rejected'>
            Rejected
          </Link>
        </h4>
        <h4 className={`hover ${this.isItemActive('expired') ?
          'active' : ''}`}>
          <Link to='/approval/expired'>
            Expired
          </Link>
        </h4>
        <h4 className={`hover ${this.isItemActive('people') ?
          'active' : ''}`}>
          <NavList
            titleIsLink
            listTitle='People'
            // list={bar}
            route='/approval/people'/>
        </h4>
        <h4 className={`hover ${this.isItemActive('manage') ?
          'active' : ''}`}>
          <Link to='/approval/manage'>
            Manage
          </Link>
        </h4>
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    return (
      <Container>
        <Link to='/' id='next-approver-nav-snapshot'>
          <Button animated primary fluid>
            <Button.Content visible>
              SNAPSHOT
            </Button.Content>
            <Button.Content hidden>
              <Icon name='arrow right'/>
            </Button.Content>
          </Button>
        </Link>
        <Search
          input={() => <Input icon='search' placeholder='Search...'/>}
          className='next-approver-nav-search'
          category
          loading={false}/>
        { this.renderLists() }
      </Container>
    );
  }

}


export default withRouter(ApproverNav);
