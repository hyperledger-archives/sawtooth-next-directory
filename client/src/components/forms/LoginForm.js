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
import { Link } from 'react-router-dom';
import { Container, Form, Label, Image, Input } from 'semantic-ui-react';
import PropTypes from 'prop-types';



/**
 *
 * @class       LoginForm
 * @description Component encapsulating the login flow
 *
 *
 *
 */
export default class LoginForm extends Component {

  static propTypes = {
    submit: PropTypes.func.isRequired
  };


  state = {
    activeIndex: 0, username: '', password: '',
    validUsername:  null,
    validPassword:  null,
  };


  /**
   *
   * @param event   Event passed by Semantic UI
   * @param name    Name of form element derived from 'name' HTML attribute
   * @param value   Value of form field
   *
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value });
    this.validate(name, value);
  }


  setFlow = (index) => {
    this.setState({ activeIndex: index });
  }


  validate = (name, value) => {
    name === 'username' &&
      this.setState({ validUsername: value.length > 0 });
    name === 'password' &&
      this.setState({ validPassword: value.length > 0 });
  }


  render () {
    const { submit } = this.props;
    const {
      activeIndex,
      username,
      password,
      validUsername,
      validPassword } = this.state;

    return (
      <div className='form-inverted'>
      { activeIndex === 0 &&
        <div>
          <Form onSubmit={() => this.setFlow(1)}>
            <Form.Field>
              <Input
                autoFocus
                placeholder='User ID'
                error={validUsername === false}
                name='username'
                type='text'
                value={username}
                onChange={this.handleChange} />
              <Label>
                <Link to='/'>Forgot User ID?</Link>
              </Label>
            </Form.Field>
            <Container textAlign='center'>
              <Form.Button
                content='Next'
                disabled={!validUsername}
                icon='right arrow'
                labelPosition='right' />
            </Container>
          </Form>
        </div>
      }
      { activeIndex === 1 &&
        <div>
          <Form onSubmit={() => submit(username, password)}>
            <Container textAlign='center'>
              <Image
                avatar
                src='http://i.pravatar.cc/150?img=31'
                size='tiny' />
            </Container>
            <Form.Button
              id='next-login-form-back-button'
              content='Back'
              type='button'
              icon='left arrow'
              labelPosition='left'
              onClick={() => this.setFlow(0)} />
            <Form.Field id='next-login-form-password'>
              <Input
                autoFocus
                error={validPassword === false}
                name='password'
                type='password'
                placeholder='Password'
                value={password}
                onChange={this.handleChange} />
              <Label>
                <Link to='/'>Forgot Password?</Link>
              </Label>
            </Form.Field>
            <Container textAlign='center'>
              <Form.Button
                content='Login'
                disabled={!validPassword}
                icon='right arrow'
                labelPosition='right' />
            </Container>
          </Form>
        </div>
      }
      </div>
    );
  }

}
