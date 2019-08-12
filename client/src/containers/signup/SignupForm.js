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
  Container,
  Form,
  Header,
  Icon,
  Input,
  Label,
  Message,
  Popup,
  Transition } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';


/**
 *
 * @class         SignupForm
 * @description   Component encapsulating the signup form
 *
 */
class SignupForm extends Component {

  static propTypes = {
    error:            PropTypes.object,
    pendingSignup:    PropTypes.bool,
    submit:           PropTypes.func,
  };


  state = {
    activeIndex:    0,
    username:       '',
    password:       '',
    validUsername:  null,
    validPassword:  null,
  };


  /**
   * Called whenever Redux state changes. Set password field
   * focus manually after transition.
   * @param {object} prevProps Props before update
   * @param {object} prevState State before update
   */
  componentDidMount () {
    setTimeout(() => this.usernameRef.focus(), 300);
  }

  /**
   * Called whenever Redux state changes. Set password field
   * focus manually after transition.
   * @param {object} prevProps Props before update
   * @param {object} prevState State before update
   */
  componentDidUpdate (prevProps) {
    const { error, pendingSignup } = this.props;
    if (prevProps.pendingSignup && !pendingSignup && !error)
      this.setFlow(1);
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
    const { error, pendingSignup, submit } = this.props;
    const {
      activeIndex,
      username,
      password,
      validUsername,
      validPassword } = this.state;

    const hide = 0;
    const show = 1000;

    const usernameHint1 = `Your Cloud Account will be created
      based on your T-Mobile GSM1900 account. All of the
      information from your existing GSM1900 profile will be
      copied to create your new Cloud Account.`;
    const usernameHint2 = `To simplify things, your Cloud Account
      ID will be the same as your GSM1900 ID.`;
    const passwordHint = `Please note that the password for your
      Cloud Account will differ from your GSM1900 password and will
      be emailed to you after successful sign up. You need to provide
      your correct Cloud Account credentials to access all the servers
      and services hosted within the T-Mobile public cloud. Therefore,
      please make sure you enter the correct Cloud Account password.`;

    return (
      <div className='form-default'>
        <Transition
          visible={activeIndex === 0}
          animation='fade up'
          duration={{ hide, show }}>
          <div id='next-signup-form-1'>
            { error &&
              <div id='next-signup-form-error'>
                <Message
                  error
                  size='small'
                  icon='exclamation triangle'
                  content={error.message}/>
              </div>
            }
            <Form onSubmit={() => submit(username, password)}>
              <Form.Field>
                <span id='next-username-prefix'>
                  GSM1900\
                </span>
                <Input
                  ref={ref => this.usernameRef = ref}
                  id='next-username-signup-input'
                  autoFocus
                  placeholder='JSmith'
                  error={validUsername === false}
                  name='username'
                  type='text'
                  value={username}
                  onChange={this.handleChange}>
                  <input/>
                  <Popup
                    wide
                    basic
                    size='mini'
                    position='top right'
                    trigger={
                      <Icon
                        className='next-signup-input-tooltip'
                        circular
                        size='small'
                        name='info'/>
                    }>
                    {usernameHint1}
                    &nbsp;
                    <strong>
                      {usernameHint2}
                    </strong>
                  </Popup>
                </Input>
                <Label className='next-signup-username-hint'>
                  {usernameHint1}
                  &nbsp;
                  <strong>
                    {usernameHint2}
                  </strong>
                </Label>
              </Form.Field>
              <Form.Field id='next-signup-form-password'>
                <Input
                  id='next-password-signup-input'
                  error={validPassword === false}
                  name='password'
                  type='password'
                  placeholder='Enter your GSM1900 password'
                  value={password}
                  onChange={this.handleChange}/>
                <Label>
                  {passwordHint}
                </Label>
              </Form.Field>
              <Container textAlign='center'>
                <Form.Button
                  loading={pendingSignup}
                  animated
                  fluid
                  disabled={pendingSignup || !validUsername || !validPassword}>
                  <Button.Content visible>
                    Sign Up
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
          animation='fade right'
          duration={{ hide, show }}>
          <div>
            <Header as='h2' icon id='next-signup-success-container'>
              <div>
                <span role='img' aria-label=''>
                  🛫
                </span>
              </div>
              Request for CORP account sent!
              <Header.Subheader>
                You will receive an email shortly containing credentials for
                your new CORP account. You can then use those credentials to
                sign into NEXT Directory. If you do not receive an email,
                please contact your administrator.
              </Header.Subheader>
            </Header>
          </div>
        </Transition>
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    error: state.auth.error,
    pendingSignup: state.auth.pendingSignup,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(SignupForm);
