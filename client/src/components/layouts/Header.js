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
import { Icon, Image } from 'semantic-ui-react';


import PropTypes from 'prop-types';
import './Header.css';
import logo from '../../images/next-logo-primary.png';


/**
 *
 * @class Header
 * Component encapsulating the main application header
 *
 */
export default class Header extends Component {

  render() {
    const { me } = this.props;

    return (
      <header className='next-header'>
        <div id='next-header-logo'>
          <Image
            src={logo}
            as='a'
            size='tiny'
            href='/home'
          />
        </div>
        <Icon inverted name='search' />
        <Icon inverted name='bell' />
        <Image src='http://i.pravatar.cc/300' avatar />
        <span id='next-header-username'>{me && me.name}</span>
      </header>
    );
  }
}

Header.propTypes = {
  me: PropTypes.arrayOf(PropTypes.shape(
    {
      name: PropTypes.string,
    },
  )),
};

Header.defaultProps = {
  me: '',
};

