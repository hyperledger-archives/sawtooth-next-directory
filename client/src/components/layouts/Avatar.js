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
import {  } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './Avatar.css';


/**
 *
 * @class         Avatar
 * @description   Component encapsulating a user avatar
 *
 *
 */
export default class Avatar extends Component {

  static propTypes = {
    onClick:        PropTypes.func,
    size:           PropTypes.string,
    users:          PropTypes.array,
    userId:         PropTypes.string,
  }


  colors = 12;


  /**
   * Generate initials from a user's name
   * @returns {string}
   */
  generatePlaceholder = () => {
    const { users, userId } = this.props;
    const user = users && users.find(user => user.id === userId);

    if (!user) return '?';
    const names = user.name.split(' ');
    let initials = names[0]
      .substring(0, 1)
      .toUpperCase();

    if (names.length > 1) {
      initials += names[names.length - 1]
        .substring(0, 1)
        .toUpperCase();
    }

    return initials;
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { onClick, size, userId } = this.props;
    const charCode = Math.min(
      Math.abs(1 - (userId.charCodeAt(2) / 1e2)), 1
    );
    const index = Math.floor((charCode * this.colors) + 1);
    return (
      <div
        onClick={onClick}
        className={`next-avatar-container
                    avatar-palette-${index}
                    ${size}`}>
        {this.generatePlaceholder()}
      </div>
    );
  }

}
