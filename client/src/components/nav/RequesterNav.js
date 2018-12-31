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
import { Button, Icon, Input, Container, Search } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './RequesterNav.css';
import NavList from './NavList';
import * as utils from '../../services/Utils';


/**
 *
 * @class         RequesterNav
 * @description   Component encapsulating the template for
 *                the sidebar displayed on the requester landing page
 *
 */
class RequesterNav extends Component {

  static propTypes = {
    getPacks:           PropTypes.func,
    mine:               PropTypes.array,
    packs:              PropTypes.array,
    recommendedPacks:   PropTypes.array,
    recommendedRoles:   PropTypes.array,
    requests:           PropTypes.array,
    roleFromId:         PropTypes.func,
    startAnimation:     PropTypes.func,
  };


  /**
   * Entry point to perform tasks required to render
   * component
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { recommendedPacks } = this.props;
    if (!utils.arraysEqual(prevProps.recommendedPacks, recommendedPacks))
      this.init();
  }


  /**
   * Determine which packs are not currently loaded
   * in the client and dispatches actions to retrieve them.
   */
  init () {
    const { getPacks, packs, recommendedPacks } = this.props;
    let diff;
    packs && recommendedPacks ?
      diff = recommendedPacks.filter(packId =>
        packs.find(pack => pack.id !== packId)) :
      diff = recommendedPacks;

    diff && diff.length > 0 && getPacks(diff);
  }


  /**
   * Render each list of sidebar groups by passing the root
   * route, title, and array of items to NavList
   * @returns {JSX}
   */
  renderLists () {
    const {
      recommendedPacks,
      recommendedRoles,
      packs,
      mine,
      requests } = this.props;

    // Recommendedations are all roles. Format a separate array of
    // recommended packs to mirror roles and hydrate the sidebar
    const packList = packs && recommendedPacks ?
      packs.filter((pack) => recommendedPacks.includes(pack.id)) :
      [];

    return (
      <div id='next-requester-nav-lists-container'>
        <NavList
          listTitle='Your Packs / Roles'
          list={mine}/>
        <NavList
          listTitle='Your Requests'
          list={requests}/>
        <NavList
          listTitle='Recommended Packs'
          route='/packs'
          list={packList}/>
        <NavList
          listTitle='Recommended Roles'
          route='/roles'
          list={recommendedRoles}/>
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
        <Link to='/browse' id='next-requester-nav-browse'>
          <Button animated primary fluid>
            <Button.Content visible>
              BROWSE
            </Button.Content>
            <Button.Content hidden>
              <Icon name='arrow right'/>
            </Button.Content>
          </Button>
        </Link>
        <Search
          input={() => <Input icon='search' placeholder='Search...'/>}
          className='next-requester-nav-search'
          category
          loading={false}/>
        { this.renderLists() }
      </Container>
    );
  }

}


export default RequesterNav;
