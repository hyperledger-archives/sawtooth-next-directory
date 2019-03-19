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
  Button,
  Header,
  Modal } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './About.css';


/**
 *
 * @class         About
 * @description   About modal
 *
 */
class About extends Component {

  static propTypes = {
    handleClose:      PropTypes.func,
    showModal:        PropTypes.bool,
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { handleClose, showModal } = this.props;
    return (
      <Modal
        open={showModal}
        onClose={handleClose}
        size='mini'>
        <Header
          id='next-about-modal-header'
          icon='info circle'
          content='About'/>
        <Modal.Content id='next-about-modal-content'>
          <Header
            as='h3'
            content='NEXT Directory'/>
          <span>
            {'Version '}
            {process.env.REACT_APP_VERSION_NUMBER}
          </span>
        </Modal.Content>
        <Modal.Actions id='next-about-modal-actions'>
          <Button primary size='large' onClick={handleClose}>
            Close
          </Button>
        </Modal.Actions>
      </Modal>
    );
  }

}


export default About;
