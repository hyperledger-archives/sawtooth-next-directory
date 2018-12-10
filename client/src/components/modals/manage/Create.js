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
import { Button, Form, Header, Icon, Modal } from 'semantic-ui-react';
import PropTypes from 'prop-types';

/**
 *
 * @class         Create
 * @description   Component encapsulating the create role
 *
 */
export default class Create extends Component {

  static propTypes = {
    submit: PropTypes.func,
  };


  state = { name: '', validName: null, open: false };


  /**
   * Determine the change event triggered
   * @param {object} event   Event passed by Semantic UI
   *
   */
  handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;
    this.setState({ [name]: value }, () => {

      this.validate(name, value);
      this.checkFields();
    });
  }

  /**
   * Determine username and password fields
   *
   */
  checkFields() {
    if (this.state.username.length > 0 && this.state.password.length > 0)
      this.setState({ validFields: true });
    else
      this.setState({ validFields: false });

  }


  handleOpen = () => this.setState({ open: true });
  handleClose = () => this.setState({
    open: false,
    validName: null,
    name: '',
  });


  handleSubmit = () => {
    const { submit } = this.props;
    const { name } = this.state;

    this.handleClose();
    submit(name);
  }


  /**
   *
   * @param name   name of the field
   * @param value  value entered by the user
   *
   */

  validate = (name, value) => {
    name === 'name' &&
      this.setState({ validName: value.length > 4 });
  }

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render() {
    const { open, validName } = this.state;

    return (
      <Modal
        trigger={<Button id='next-open-modal-icon' icon='add'
          onClick={this.handleOpen} />}
        basic
        dimmer='inverted'
        size='mini'
        open={open}
        onClose={this.handleClose}>
        <Header icon='add' content='Create New Role' />
        <Modal.Content>
          <p>Create a new role.</p>
          <Form>
            <Form.Input
              autoFocus
              error={validName === false}
              name='name'
              placeholder='Name'
              onChange={this.handleChange} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button id='next-modal-close-button' basic color='red'
            onClick={this.handleClose}>
            <Icon name='remove' /> Close
          </Button>
          <Button
            id='next-modal-submit-button'
            color='green'
            disabled={!validName}
            onClick={this.handleSubmit}>
            <Icon name='add' /> Create
          </Button>
        </Modal.Actions>
      </Modal>
    );
  }

}
