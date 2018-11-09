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
import { Form, Button } from 'semantic-ui-react';

import { Link } from 'react-router-dom';


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
    this.state = { username: '', password: '', error: false };
  }


  /**
   *
   * @param event   Event passed by Semantic UI
   * @param name    Name of form element derived from 'name' HTML attribute
   * @param value   Value of form field
   *
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value, error: false });
  }

  /**
   * function returns true if any form field is empty
   * 
   */
  isFormValidated(){
    const { username, password } = this.state;

    if(username.length<4 || password.length<4) {
      this.setState({
        error: true
      });
      return false;
    } else {
      return true;
    }
  }

  /**
   * 
   * @param username   value of username field of the form.
   * @param password    value of password field of the form.
   * 
   */
  submitForm(username, password) {
    const { submit } = this.props;

    if(this.isFormValidated()){
      submit(username, password);
    }

  }


  render () {
    const { username, password, error } = this.state;

    return (
      <Form onSubmit={() => this.submitForm(username, password)}>
        <Form.Input
          label='User ID'
          placeholder='User ID'
          name='username'
          onChange={this.handleChange}
          error={error}/>
        <Form.Input
          label='Password'
          placeholder='Password'
          name='password'
          type='password'
          onChange={this.handleChange}
          error={error}/>
        <Form.Button content='Login'/>
        <Link to="/signup">
          <Button>Sign up</Button>
        </Link>
      </Form>
    );
  }

}


LoginForm.proptypes = {
  submit: PropTypes.func.isRequired
};
