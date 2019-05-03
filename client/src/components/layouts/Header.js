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
import {
  Checkbox,
  Icon,
  Image,
  Label,
  Menu,
  Header as MenuHeader } from 'semantic-ui-react';
import { Link, withRouter } from 'react-router-dom';
import LoadingBar from 'react-redux-loading-bar';
import PropTypes from 'prop-types';


import './Header.css';
import Avatar from './Avatar';
import Notifications from './Notifications';
import About from './About';
import logo from 'images/next-logo-primary.png';
import * as utils from 'services/Utils';
import * as storage from 'services/Storage';


/**
 *
 * @class         Header
 * @description   Header at the top of the viewport
 *
 */
class Header extends Component {

  static propTypes = {
    history:                 PropTypes.object,
    logout:                  PropTypes.func,
    me:                      PropTypes.object,
    openProposalsCount:      PropTypes.number,
    recommendedPacks:        PropTypes.array,
    recommendedRoles:        PropTypes.array,
    startAnimation:          PropTypes.func,
  }


  state = {
    approverViewEnabled:     false,
    globalMenuVisible:       false,
    notificationMenuVisible: false,
  };


  /**
   * Entry point to perform tasks required to render
   * component. Add event listener to handle click outside menu.
   */
  componentDidMount () {
    const {history} = this.props;
    if ( history.location.pathname === '/approval/manage'){
      this.setState({approverViewEnabled: true}
      );
    } else {
      this.setState({
        approverViewEnabled: !!storage.getViewState(),
      });
    }
    const { id, isSocketOpen, sendSocket } = this.props;
    document.addEventListener(
      'mousedown', this.handleClickOutside
    );
    if (isSocketOpen('feed'))
      sendSocket('feed', { next_id: id });
  }


  /**
   * Called whenever Redux state changes. On socket open, send
   * message to feed socket.
   * @param {object} prevProps Props before update
   * @param {object} prevState State before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const {history} = this.props;
    if (history.location.pathname.includes('/approval')  &&
    this.state.approverViewEnabled === false){
      this.setState({approverViewEnabled: true}
      );
    }
    if (!(history.location.pathname.includes('/approval')) &&
    this.state.approverViewEnabled === true){
      this.setState({approverViewEnabled: false}
      );
    }
    const { id, isAuthenticated, isSocketOpen, sendSocket } = this.props;
    if (prevProps.isAuthenticated !== isAuthenticated) {
      this.setState({
        globalMenuVisible: false,
        notificationMenuVisible: false,
      });
    }
    if (prevProps.isSocketOpen('feed') !== isSocketOpen('feed') &&
      isSocketOpen('feed'))
      sendSocket('feed', { next_id: id });
  }


  /**
   * Component teardown. Remove event listener.
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
      this.setState({
        globalMenuVisible: false,
        notificationMenuVisible: false,
      });
  }


  /**
   * Use to get header DOM
   * @param {object} node DOM node
   */
  setRef = (node) => {
    this.ref = node;
  }


  /**
   * Toggle notification menu
   */
  toggleNotificationMenu = () => {
    const { notificationMenuVisible } = this.state;
    this.setState({
      globalMenuVisible: false,
      notificationMenuVisible: !notificationMenuVisible,
    });
  }


  /**
   * Toggle global menu
   */
  toggleGlobalMenu = () => {
    const { globalMenuVisible } = this.state;
    this.setState({
      globalMenuVisible: !globalMenuVisible,
      notificationMenuVisible: false });
  }


  /**
   * Toggle about modal
   */
  toggleAboutModal = () => {
    const { aboutModalVisible } = this.state;
    this.setState({
      aboutModalVisible: !aboutModalVisible,
      globalMenuVisible: false,
    });
  }


  /**
   * Toggle approver view. When enabled, add setting to
   * browser storage and navigate to view.
   * @param {object} event Event passed by Semantic UI
   * @param {object} data  Attributes passed on change
   */
  toggleApproverView = (event, data) => {
    const {
      history,
      recommendedPacks,
      recommendedRoles,
      startAnimation } = this.props;

    if (data.checked) {
      storage.setViewState(1);
      this.setState({ approverViewEnabled: true });
      history.push('/approval/pending/individual');
    } else {
      storage.removeViewState();
      this.setState({ approverViewEnabled: false });
      startAnimation();
      history.push(
        utils.createHomeLink(recommendedPacks, recommendedRoles)
      );
    }
  }


  /**
   * Dispatch logout action
   */
  logout = () => {
    const { logout } = this.props;
    this.toggleGlobalMenu();
    logout();
  }


  /**
   * Determine notification icon count
   * @returns {JSX}
   */
  renderCountIcon () {
    const { expiredCount, openProposalsCount } = this.props;
    return (
      <div>
        { (expiredCount || openProposalsCount) &&
          <Label circular color='red' floating size='mini'>
            {(expiredCount || 0) + (openProposalsCount || 0)}
          </Label>
        }
      </div>
    );
  }

  /**
   * Render aprrover view button
   * @returns {JSX}
   */
  renderApprover = () => {
    const { approverViewEnabled } = this.state;
    return (
      <Menu.Item id='next-header-global-menu-view-toggle'>
        <MenuHeader as='h5'>
          <Icon name='window maximize outline' color='red'/>
          <MenuHeader.Content>
            <span className= 'next-toggle-state-header'>
                  Approver View:
              <span className='next-toggle-state-label'>
                {approverViewEnabled ? 'ON' : 'OFF'}
              </span>
            </span>
            <Checkbox
              id='next-approver-checkbox'
              toggle
              className='pull-right'
              checked={approverViewEnabled}
              onChange={this.toggleApproverView}/>
          </MenuHeader.Content>
        </MenuHeader>
      </Menu.Item>
    );
  };


  /**
   * Render global dropdown menu
   * @returns {JSX}
   */
  renderGlobalMenu () {
    const { id, me } = this.props;

    return (
      <div id='next-header-global-menu'>
        <Menu inverted size='huge' vertical>
          { me &&
            <Menu.Item
              id='next-header-global-menu-profile'
              className='large'>
              <MenuHeader as='h3'>
                <Avatar userId={id} size='medium' {...this.props}/>
                <MenuHeader.Content>
                  {me.name}
                </MenuHeader.Content>
              </MenuHeader>
            </Menu.Item>
          }
          <Menu.Item
            as={Link} to='/approval/manage'
            onClick={this.toggleGlobalMenu}>
            <MenuHeader as='h5'>
              <Icon name='setting' color='grey'/>
              <MenuHeader.Content>
                Manage
              </MenuHeader.Content>
            </MenuHeader>
          </Menu.Item>
          <Menu.Item
            onClick={this.toggleAboutModal}>
            <MenuHeader as='h5'>
              <Icon name='info circle' color='grey'/>
              <MenuHeader.Content>
                About
              </MenuHeader.Content>
            </MenuHeader>
          </Menu.Item>
          <Menu.Item
            id='next-signout-button'
            onClick={this.logout}>
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
      id,
      me,
      recommendedPacks,
      recommendedRoles,
      startAnimation } = this.props;
    const {
      aboutModalVisible,
      approverViewEnabled,
      globalMenuVisible,
      notificationMenuVisible } = this.state;
    return (
      <header className='next-header' ref={this.setRef}>
        <LoadingBar className='next-global-loading-bar'/>
        <About
          showModal={aboutModalVisible}
          handleClose={this.toggleAboutModal}/>
        <div id='next-header-logo'>
          <Image
            as={Link}
            to={approverViewEnabled ?
              '/approval/pending/individual' :
              utils.createHomeLink(recommendedPacks, recommendedRoles)}
            src={logo}
            onClick={startAnimation}
            size='tiny'/>
        </div>
        { me &&
        <div className='next-render-approver'>
          {this.renderApprover()}
        </div>

        }
        { me &&
        <div id='next-header-actions'>
          <div
            id='next-header-actions-bell'
            className='cursor-pointer'
            onClick={this.toggleNotificationMenu}>
            <Icon inverted name='bell'/>
            {this.renderCountIcon()}
          </div>
          { me &&
            <div
              id='next-header-actions-profile'
              onClick={this.toggleGlobalMenu}>
              <div className='cursor-pointer'>
                <Avatar
                  userId={id}
                  size='small'
                  {...this.props}/>
              </div>
            </div>
          }
        </div>
        }
        { globalMenuVisible &&
          this.renderGlobalMenu()
        }
        { notificationMenuVisible &&
          <Notifications
            toggleMenu={this.toggleNotificationMenu}
            {...this.props}/>
        }
      </header>
    );
  }

}


export default withRouter(Header);
