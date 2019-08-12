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
import { Link } from 'react-router-dom';
import {
  Button,
  Container,
  Form,
  Icon,
  Label,
  Input,
  Message,
  Transition } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';


/**
 *
 * @class         LoginForm
 * @description   Component encapsulating the login form
 *
 */
class LoginForm extends Component {

  static propTypes = {
    error:          PropTypes.object,
    pendingLogin:   PropTypes.bool,
    resetErrors:    PropTypes.func,
    submit:         PropTypes.func,
  };


  state = {
    activeIndex: 0, username: '', password: '',
    validUsername:  null,
    validPassword:  null,
    validEmail:     null,
    resetEmail:     '',
  };


  /**
   * Called whenever Redux state changes. Set password field
   * focus manually after transition.
   * @param {object} prevProps Props before update
   * @param {object} prevState State before update
   */
  componentDidUpdate (prevProps, prevState) {
    const { activeIndex } = this.state;
    if (prevState.activeIndex === 0 && activeIndex === 1)
      setTimeout(() => this.passwordRef.focus(), 300);
  }


  /**
   * Handle form change event
   * @param {object} event Event passed by Semantic UI
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  handleChange = (event, { name, value }) => {
    const { error } = this.props;
    error && this.handleDismiss();
    this.setState({ [name]: value });
    this.validate(name, value);
  }


  /**
   * Set current view
   * @param {number} index View index
   */
  setFlow = (index) => {
    this.setState({ activeIndex: index });
  }


  /**
   * Validate login form input
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  validate = (name, value) => {
    name === 'username' &&
      this.setState({ validUsername: value.length > 0 });
    name === 'password' &&
      this.setState({ validPassword: value.length > 0 });
    name === 'resetEmail' &&
      this.setState({ validEmail: /\S+@\S+\.\S+/.test(value) });
  }


  /**
   * Dismiss error message
   */
  handleDismiss = () => {
    const { resetErrors } = this.props;
    resetErrors();
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { error, pendingLogin, submit } = this.props;
    const {
      activeIndex,
      username,
      password,
      resetEmail,
      validUsername,
      validPassword,
      validEmail } = this.state;

    const hide = 0;
    const show = 300;

    return (
      <div className='form-default'>
        <Transition
          visible={activeIndex === 0}
          animation='fade up'
          duration={{ hide, show }}>
          <div id='next-login-form-1'>
            { error &&
              <div id='next-login-form-error'>
                <Message
                  error
                  size='small'
                  icon='exclamation triangle'
                  content={error.message}/>
              </div>
            }
            <Form id='next-login-form'
              onSubmit={() => submit(username, password)}>
              <Form.Field>
                <Label>
                  USERNAME
                </Label>
                <Input
                  id='next-username-input'
                  autoFocus
                  placeholder='Username'
                  error={validUsername === false}
                  name='username'
                  type='text'
                  value={username}
                  onChange={this.handleChange}/>
              </Form.Field>
              <Form.Field>
                <Label>
                  PASSWORD
                </Label>
                <Input
                  id='next-password-input'
                  ref={ref => this.passwordRef = ref}
                  error={validPassword === false}
                  name='password'
                  type='password'
                  placeholder='Password'
                  value={password}
                  onChange={this.handleChange}/>
                {/* <Button
                    id='next-login-form-forgot-password'
                    className='link'
                    type='button'
                    onClick={() => this.setFlow(1)}>
                  Forgot Password? */}
                {/* </Button> */}
                { process.env.REACT_APP_ENABLE_NEXT_BASE_USE === '1' &&
                <Label>
                  <div id='next-login-new-account-container'>
                    Don&apos;t have an account?
                    <Link to='/signup'>
                      Sign Up
                    </Link>
                  </div>
                </Label>
                }
              </Form.Field>
              <Container textAlign='center'>
                <Form.Button
                  id='next-login-form-submit'
                  loading={pendingLogin}
                  animated
                  fluid
                  disabled={pendingLogin || !validUsername || !validPassword}>
                  <Button.Content visible>
                    Login
                  </Button.Content>
                  <Button.Content hidden>
                    <Icon name='arrow right'/>
                  </Button.Content>
                </Form.Button>
              </Container>
            </Form>
          </div>
        </Transition>
        <Transition
          visible={activeIndex === 1}
          animation='fade up'
          duration={{ hide, show }}>
          <div>
            <Form id='next-login-form-reset-password'
              onSubmit={() => this.setFlow(0)}>
              <Form.Field >
                <Input
                  autoFocus
                  name='resetEmail'
                  type='text'
                  placeholder='Email'
                  value={resetEmail}
                  onChange={this.handleChange}/>
              </Form.Field>
              <Container textAlign='center'>
                <Form.Button
                  content='Reset Password'
                  disabled={!validEmail}
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


const mapStateToProps = (state) => {
  return {
    error: state.auth.error,
    pendingLogin: state.auth.pendingLogin,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(LoginForm);
