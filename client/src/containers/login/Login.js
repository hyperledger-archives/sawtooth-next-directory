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
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Grid, Header, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './Login.css';
import logo from 'images/next-logo-billboard.png';
import { AuthActions, AuthSelectors } from 'state';
import LoginForm from 'components/forms/LoginForm';


import * as utils from 'services/Utils';
import * as storage from 'services/Storage';


/**
 *
 * @class         Login
 * @description   Component encapsulating the login landing page
 *
 *
 */
class Login extends Component {

  static propTypes = {
    history:                PropTypes.object,
    isAuthenticated:        PropTypes.bool,
    login:                  PropTypes.func.isRequired,
    recommendedPacks:       PropTypes.array,
    recommendedRoles:       PropTypes.array,
  };


  /**
   * Entry point to perform tasks required to render
   * component
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    this.init();
  }


  /**
   * On authentication, determine home URL and redirect
   */
  init () {
    const {
      history,
      isAuthenticated,
      recommendedPacks,
      recommendedRoles } = this.props;
    isAuthenticated && history.push(
      storage.getViewState() ?
        '/approval/pending/individual' :
        utils.createHomeLink(recommendedPacks, recommendedRoles)
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { login } = this.props;

    return (
      <div id='next-login-container'>
        <Grid container centered columns={1}>
          <Grid.Column id='next-login-column'>
            <Header inverted textAlign='center'>
              <Image centered src={logo} id='next-login-logo'/>
              <h1>
                Sign in to NEXT Directory
              </h1>
            </Header>
            <LoginForm submit={login}/>
          </Grid.Column>
        </Grid>
        <div id='next-login-new-account-container'>
          <Link to='/signup'>
            Create an account
          </Link>
        </div>
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    error: state.auth.error,
    isAuthenticated: AuthSelectors.isAuthenticated(state),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    login: (email, password) =>
      dispatch(AuthActions.loginRequest(email, password)),
    attemptSignup: (name, username, password, email) =>
      dispatch(AuthActions.signupRequest(name, username, password, email)),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(Login);
