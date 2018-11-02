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


import PropTypes from 'prop-types';


import './TrackHeader.css';


/**
 *
 * @class TrackHeader
 * Component encapsulating the track pane header
 *
 */
export default class TrackHeader extends Component {
  render() {
    const { title } = this.props;

    return (
      <div id='next-requester-tracker-header-container'>
        <div id='next-requester-track-header'>
          <h1>{title}</h1>
        </div>
        <div id="next-wave-container">
          <div id="next-wave" />
          <div id="next-wave-alt" />
        </div>
      </div>
    );
  }
}


TrackHeader.propTypes = {
  title: PropTypes.string,
};


TrackHeader.defaultProps = {
  title: '',
};
