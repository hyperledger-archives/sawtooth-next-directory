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
import { Form } from 'semantic-ui-react';


import PropTypes from 'prop-types';


/**
 * 
 * @class LoginForm
 * Component encapsulating a reusable login form suitable for
 * composing within containers where login functionality is required
 * 
 */
export default class LoginForm extends Component {

  constructor (props) {
    super(props);

    // TODO: Consider moving to Redux
    this.state = { username: '', password: '' };
  }


  /**
   * 
   * @param event   Event passed by Semantic UI
   * @param name    Name of form element derived from 'name' HTML attribute
   * @param value   Value of form field
   * 
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value });
  }

  
  render () {
    const { submit } = this.props;
    const { username, password } = this.state;

    return (
      <Form onSubmit={() => submit(username, password)}>
        <Form.Input
          label='User ID'
          placeholder='User ID'
          name='username'
          onChange={this.handleChange}/>
        <Form.Input
          label='Password'
          placeholder='Password'
          name='password'
          type='password'
          onChange={this.handleChange}/>
        <Form.Button content='Login'/>
      </Form>
    );
  }
  
}


LoginForm.proptypes = {
  submit: PropTypes.func.isRequired
};
