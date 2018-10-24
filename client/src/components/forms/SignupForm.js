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
 * @class SignupForm
 * Component encapsulating sign-up form suitable for creating new users
 * 
 */
export default class SignupForm extends Component {

  constructor (props) {
    super(props);

    // TODO: Consider moving to Redux
    this.state = { username: '', password: '', name: '', email: '' };
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
    const { username, password, name, email  } = this.state;

    return (
      <Form onSubmit={() => submit(name, username, password, email)}>
        <Form.Input
          label='Name'
          placeholder='Name'
          name='name'
          onChange={this.handleChange}/>
        <Form.Input
          label='User Name'
          placeholder='user name'
          name='username'
          onChange={this.handleChange}/>
        <Form.Input
          label='Password'
          placeholder='Password'
          name='password'
          type='password'
          onChange={this.handleChange}/>
        <Form.Input
          label='Email'
          placeholder='email'
          name='email'
          type='email'
          onChange={this.handleChange}/>
        <Form.Button content='Sign Up'/>

        <Link to = '/login'>
            <Button>Return to Login</Button>
        </Link>
      </Form>
    );
  }
  
}


SignupForm.proptypes = {
  submit: PropTypes.func.isRequired
};
