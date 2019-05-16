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
  Container,
  Form,
  Label,
  Icon,
  Input,
  Transition } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { AuthActions, AuthSelectors } from 'state';
import * as utils from 'services/Utils';

/**
 *
 * @class         SignupForm
 * @description   Component encapsulating the signup form
 *
 */
class SignupForm extends Component {

  static propTypes = {
    checkUserExists: PropTypes.func,
    resetUserExists: PropTypes.func,
    submit: PropTypes.func,
    userExists: PropTypes.bool,
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
    errorDisplay: true,
  };


  /**
   * Called whenever Redux state changes. Set password field
   * focus manually after transition.
   * @param {object} prevProps Props before update
   * @param {object} prevState State before update
   */
  componentDidMount () {
    const { resetUserExists } = this.props;
    resetUserExists();
  }

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
    this.setState({ [name]: value });
    this.validate(name, value);
  }

  /**
   * Handle form change event
   * @param {object} event Event passed by Semantic UI
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  usernameChange = (event, { name, value }) => {
    this.setState({ [name]: value });
    this.validate(name, value);
    this.setState({ errorDisplay: false});
  }


  /**
   * Set current view based on index
   * @param {number} index View index
   */
  setFlow = (index) => {
    this.setState({ activeIndex: index });
  }

  handleBlur = () => {
    const { checkUserExists } = this.props;
    const { name } = this.state;
    !utils.isWhitespace(name) && checkUserExists(name);
    setTimeout(() => {
      this.setState({ errorDisplay: true});
    }, 100);
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
    const { submit, userExists} = this.props;
    const {
      activeIndex,
      name,
      email,
      username,
      password,
      validName,
      validEmail,
      validUsername,
      errorDisplay,
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
                  onBlur={this.handleBlur}
                  onChange={this.usernameChange}/>
                { userExists && errorDisplay &&
                  <Label
                    id='next-signup-username-error'>
                    <Icon name='exclamation circle'/>
                      This username already exists.
                  </Label>
                }

                {!validName &&
                <Label className='next-name-signup-hint'>
                  Name must be at least 5 characters.
                </Label>}

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

                {!validUsername &&
                <Label className='next-username-signup-hint'>
                  Username must be at least 5 characters.
                </Label>}

              </Form.Field>
              <Container textAlign='center'>
                <Form.Button
                  content='Next'
                  disabled={!validName || !validEmail || !validUsername
                    || userExists}
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
                  ref={ref => this.passwordRef = ref}
                  id='next-password-signup-input'
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


const mapStateToProps = (state) => {
  return {
    userExists: AuthSelectors.userExists(state),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    checkUserExists: (name) =>
      dispatch(AuthActions.userExistsRequest(name)),
    resetUserExists: (name) => dispatch(AuthActions.resetUserExists()),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(SignupForm);
