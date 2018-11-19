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
import { Icon, Image, Label, Menu, Header as MenuHeader } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

import './Header.css';
import logo from '../../images/next-logo-primary.png';


/**
 *
 * @class Header
 * Component encapsulating the main application header
 *
 */
export default class Header extends Component {

  state = { menuVisible: false };


  componentDidMount() {
    document.addEventListener(
      'mousedown', this.handleClickOutside
    );
  }


  componentWillUnmount() {
    document.removeEventListener(
      'mousedown', this.handleClickOutside
    );
  }


  handleClickOutside = (event) => {
    this.ref && !this.ref.contains(event.target) &&
      this.setState({ menuVisible: false });
  }


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
          <Menu.Item onClick={() => {}}>
            <MenuHeader as='h5'>
              <Icon name='setting' color='grey'/>
              <MenuHeader.Content>
                Settings
              </MenuHeader.Content>
            </MenuHeader>
          </Menu.Item>
          <Menu.Item onClick={this.logout}>
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


  render () {
    const { me, openProposalsCount } = this.props;
    const { menuVisible } = this.state;

    return (
      <header className='next-header' ref={this.setRef}>
        <div id='next-header-logo'>
          <Image as={Link} to='/' src={logo} size='tiny'/>
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
