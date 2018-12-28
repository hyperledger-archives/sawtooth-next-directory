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
import {
  Container,
  Form,
  Label,
  Input,
  Transition } from 'semantic-ui-react';
import PropTypes from 'prop-types';


/**
 *
 * @class         SignupForm
 * @description   Component encapsulating the signup form
 *
 */
export default class SignupForm extends Component {

  static propTypes = {
    submit: PropTypes.func.isRequired,
  };


  state = {
    activeIndex:    0,
    name:           '',
    email:          '',
    username:       '',
    password:       '',
    validName:      null,
    validEmail:     null,
    validUsername:  null,
    validPassword:  null,
  };


  /**
   * Handle form change event
   * @param {object} event Event passed by Semantic UI
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value });
    this.validate(name, value);
  }


  /**
   * Set current view based on index
   * @param {number} index View index
   */
  setFlow = (index) => {
    this.setState({ activeIndex: index });
  }


  /**
   * Validate signup form input
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  validate = (name, value) => {
    name === 'name' &&
      this.setState({ validName: value.length > 4 });
    name === 'email' &&
      this.setState({ validEmail: /\S+@\S+\.\S+/.test(value) });
    name === 'username' &&
      this.setState({ validUsername: value.length > 4 });
    name === 'password' &&
      this.setState({ validPassword: value.length > 5 });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { submit } = this.props;
    const {
      activeIndex,
      name,
      email,
      username,
      password,
      validName,
      validEmail,
      validUsername,
      validPassword } = this.state;

    const hide = 0;
    const show = 300;

    return (
      <div className='form-inverted'>
        <Transition
          visible={activeIndex === 0}
          animation='fade up'
          duration={{ hide, show }}>
          <div>
            <Form id='next-signup-form-1' onSubmit={() => this.setFlow(1)}>
              <Form.Field>
                <Input
                  id='next-name-signup-input'
                  autoFocus
                  placeholder='Name'
                  error={validName === false}
                  name='name'
                  type='text'
                  value={name}
                  onChange={this.handleChange}/>
              </Form.Field>
              <Form.Field>
                <Input
                  id='next-email-signup-input'
                  placeholder='Email'
                  error={validEmail === false}
                  name='email'
                  type='email'
                  value={email}
                  onChange={this.handleChange}/>
              </Form.Field>
              <Form.Field>
                <Input
                  id='next-username-signup-input'
                  placeholder='User ID'
                  error={validUsername === false}
                  name='username'
                  type='text'
                  value={username}
                  onChange={this.handleChange}/>
              </Form.Field>
              <Container textAlign='center'>
                <Form.Button
                  content='Next'
                  disabled={!validName || !validEmail || !validUsername}
                  icon='right arrow'
                  labelPosition='right'/>
              </Container>
            </Form>
          </div>
        </Transition>
        <Transition
          visible={activeIndex === 1}
          animation='fade down'
          duration={{ hide, show }}>
          <div>
            <Form id='next-password-signup-form'
              onSubmit={() => submit(name, username, password, email)}>
              <Form.Button
                id='next-signup-form-back-button'
                content='Back'
                type='button'
                icon='left arrow'
                labelPosition='left'
                onClick={() => this.setFlow(0)}/>
              <Form.Field id='next-signup-form-password'>
                <Input
                  id='next-password-signup-input'
                  autoFocus
                  error={validPassword === false}
                  name='password'
                  type='password'
                  placeholder='Password'
                  value={password}
                  onChange={this.handleChange}/>
                <Label>
                  Password must be at least 6 characters
                </Label>
              </Form.Field>
              <Container textAlign='center'>
                <Form.Button
                  content='Sign Up'
                  disabled={!validPassword}
                  icon='right arrow'
                  labelPosition='right'/>
              </Container>
            </Form>
          </div>
        </Transition>
      </div>
    );
  }

}
