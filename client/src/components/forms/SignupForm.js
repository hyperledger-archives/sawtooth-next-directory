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
 * Component encapsulating signup form suitable for creating new users
 *
 */
export default class SignupForm extends Component {

  constructor (props) {
    super(props);

    // TODO: Consider moving to Redux
    this.state = { 
      username: { value: '', error: false }, 
      password: { value: '', error: false }, 
      name: { value: '', error: false }, 
      email: { value: '', error: false } 
    };

    this.isFormValidated = this.isFormValidated.bind(this);
  }


  /**
   *
   * @param event   Event passed by Semantic UI
   * @param name    Name of form element derived from 'name' HTML attribute
   * @param value   Value of form field
   *
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: {value: value, error: false} });
  }

  isFormValidated(){
    let errorCount = 0;

    Object.keys(this.state).map(field => {
      if(this.state[field].value.length < 4) {
        errorCount++;
        this.setState({
          [field]: {...this.state[field], error: true}
        });
      }
    });

    if(errorCount > 0){
      return false
    }else {
      return true
    }
  }

  submitForm() {
    const { submit } = this.props;
    const { username, password, name, email  } = this.state;

    if(this.isFormValidated()){
      submit(username.value, password.value, name.value, email.value);
    }
  }


  render () {
    const { username, password, name, email  } = this.state;

    return (
      <Form onSubmit={() => this.submitForm()}>
        <Form.Input
          label='Name'
          placeholder='Name'
          name='name'
          onChange={this.handleChange}
          error={name.error}
          />
        <Form.Input
          label='User Name'
          placeholder='user name'
          name='username'
          onChange={this.handleChange}
          error={username.error}/>
        <Form.Input
          label='Password'
          placeholder='Password'
          name='password'
          type='password'
          onChange={this.handleChange}
          error={password.error}/>
        <Form.Input
          label='Email'
          placeholder='email'
          name='email'
          type='email'
          onChange={this.handleChange}
          error={email.error}/>
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
