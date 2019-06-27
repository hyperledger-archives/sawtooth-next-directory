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
import './Confirm.css';


/**
 *
 * @class         Confirm
 * @description   Confirm modal
 *
 */
class Confirm extends Component {

  static propTypes = {
    body:             PropTypes.string,
    handleClose:      PropTypes.func,
    handleConfirm:    PropTypes.func,
    heading:          PropTypes.string,
    showModal:        PropTypes.bool,
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      body,
      handleConfirm,
      handleClose,
      heading,
      showModal } = this.props;

    return (
      <Modal
        open={showModal}
        onClose={handleClose}
        size='mini'>
        <Header
          id='next-confirm-modal-header'
          icon='info circle'
          content='Confirm'/>
        <Modal.Content id='next-confirm-modal-content'>
          <Header
            as='h3'
            content={heading}/>
          <span>
            {body}
          </span>
        </Modal.Content>
        <Modal.Actions id='next-confirm-modal-actions'>
          <Button size='large' onClick={handleClose}>
            No
          </Button>
          <Button primary size='large' onClick={handleConfirm}>
            Yes
          </Button>
        </Modal.Actions>
      </Modal>
    );
  }

}


export default Confirm;
