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
import {
  Icon,
  Image,
  Label,
  Menu,
  Header as MenuHeader } from 'semantic-ui-react';
import { Link } from 'react-router-dom';
import LoadingBar from 'react-redux-loading-bar';
import PropTypes from 'prop-types';


import './Header.css';
import * as utils from '../../services/Utils';
import logo from '../../images/next-logo-primary.png';


/**
 *
 * @class         Header
 * @description   Header at the top of the viewport
 *
 */
class Header extends Component {

  static propTypes = {
    logout:                 PropTypes.func,
    me:                     PropTypes.object,
    startAnimation:         PropTypes.func,
    openProposalsCount:     PropTypes.number,
    recommendedPacks:       PropTypes.array,
    recommendedRoles:       PropTypes.array,
  }


  state = { menuVisible: false };



  /**
   * Entry point to perform tasks required to render
   * component. Add event listener to handle click outside menu.
   */
  componentDidMount () {
    document.addEventListener(
      'mousedown', this.handleClickOutside
    );
  }


  /**
   * Called whenever Redux state changes. Remove event listener.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentWillUnmount () {
    document.removeEventListener(
      'mousedown', this.handleClickOutside
    );
  }


  /**
   * Close menu if mouse clicks outside
   * @param {object} event Event
   */
  handleClickOutside = (event) => {
    this.ref && !this.ref.contains(event.target) &&
      this.setState({ menuVisible: false });
  }


  /**
   * Use to get header DOM
   * @param {object} node DOM node
   */
  setRef = (node) => {
    this.ref = node;
  }


  toggleMenu = () => {
    const { menuVisible } = this.state;
    this.setState({ menuVisible: !menuVisible });
  }


  logout = () => {
    const { logout } = this.props;
    this.toggleMenu();
    logout();
  }


  /**
   * Render global dropdown menu
   * @returns {JSX}
   */
  renderMenu () {
    const { me } = this.props;

    return (
      <div id='next-header-menu'>
        <Menu inverted size='huge' vertical>
          { me &&
            <Menu.Item>
              <MenuHeader as='h3'>
                <Image
                  avatar
                  src='http://i.pravatar.cc/300'
                  size='large'/>
                <MenuHeader.Content>
                  {me.name}
                </MenuHeader.Content>
              </MenuHeader>
            </Menu.Item>
          }
          <Menu.Item as={Link} to='/approval/manage' onClick={this.toggleMenu}>
            <MenuHeader as='h5'>
              <Icon name='setting' color='grey'/>
              <MenuHeader.Content>
                Manage
              </MenuHeader.Content>
            </MenuHeader>
          </Menu.Item>
          <Menu.Item  id='next-signout-button' onClick={this.logout}>
            <MenuHeader as='h5'>
              <Icon name='sign out' color='grey'/>
              <MenuHeader.Content>
                Sign out
              </MenuHeader.Content>
            </MenuHeader>
          </Menu.Item>
        </Menu>
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      me,
      openProposalsCount,
      recommendedPacks,
      recommendedRoles,
      startAnimation } = this.props;
    const { menuVisible } = this.state;

    return (
      <header className='next-header' ref={this.setRef}>
        <LoadingBar className='next-global-loading-bar'/>
        <div id='next-header-logo'>
          <Image
            as={Link}
            to={utils.createHomeLink(recommendedPacks, recommendedRoles)}
            src={logo}
            onClick={startAnimation}
            size='tiny'/>
        </div>
        { me &&
        <div id='next-header-actions'>
          <Icon inverted name='search'/>
          <div id='next-header-bell'>
            <Link to='/approval/pending/individual'>
              <Icon inverted name='bell'/>
              { openProposalsCount &&
                <Label circular color='blue' floating size='mini'>
                  {openProposalsCount}
                </Label>
              }
            </Link>
          </div>
          { me &&
            <Image
              avatar
              src='http://i.pravatar.cc/300'
              onClick={this.toggleMenu}/> }
        </div>
        }
        { menuVisible && this.renderMenu() }
      </header>
    );
  }

}


export default Header;
