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
import { Link } from 'react-router-dom';
import {
  Button, Container, Search, Icon,
} from 'semantic-ui-react';


import PropTypes from 'prop-types';


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
    const { recommended, memberOf, requests } = this.props;

    return (
      <div id="next-requester-nav-lists-container">
        <NavList
          dynamic
          listTitle='Your Packs / Roles'
          route='/home/packs'
          list={memberOf}/>
        <NavList
          dynamic
          listTitle="Your Requests"
          route="/home/requests"
          list={requests}
        />
        <NavList
          dynamic
          listTitle="Recommended Packs"
          route="/home/recommended-packs"
          list={[]}
        />
        <NavList
          dynamic
          listTitle="Recommended Roles"
          route="/home/recommended-roles"
          list={recommended}
        />
      </div>
    );
  }


  render () {
    return (
      <Container>

        <Link to="/browse">
          <Button animated secondary fluid id="next-browse-button">
            <Button.Content visible>BROWSE</Button.Content>
            <Button.Content hidden><Icon name="arrow right" /></Button.Content>
          </Button>
        </Link>

        <Search
          className="next-requester-nav-search"
          category
          loading={false}
        />

        { this.renderLists() }

        <h4 id='next-requester-switch-container'>
          <Link to='/approval/pending/individuals'>
            Switch to Approver
          </Link>
        </h4>

      </Container>
    );
  }
}


RequesterNav.propTypes = {
  packs: PropTypes.arrayOf(PropTypes.string),
  requests: PropTypes.arrayOf(PropTypes.string),
  recommended: PropTypes.arrayOf(PropTypes.string),
  logout: PropTypes.func.isRequired,
};


RequesterNav.defaultProps = {
  packs: '',
  requests:'',
  recommended:'',
};