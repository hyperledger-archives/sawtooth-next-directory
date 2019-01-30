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
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Grid, Header, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './Login.css';
import logo from 'images/next-logo-billboard.png';
import { AuthActions, AuthSelectors } from 'state';
import LoginForm from './LoginForm';


import * as storage from 'services/Storage';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


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


  state = { authSource: null };


  themes = ['flux'];


  /**
   * Entry point to perform tasks required to render
   * component
   */
  componentDidMount () {
    theme.apply(this.themes);
    this.setState({ authSource: storage.getAuthSource() || 'next' });
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @param {object} prevState State before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps, prevState) {
    const { authSource } = this.state;
    this.init();

    if (prevState.authSource !== authSource) {
      if (authSource === 'ldap')
        storage.setAuthSource('ldap');
      else
        storage.setAuthSource('next');
    }
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    const { history } = this.props;
    !history.location.pathname.includes('signup') &&
      theme.remove(this.themes);
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
   * Set authentication source
   * @param {string} authSource Authentication source
   */
  setAuthSource = (authSource) => {
    this.setState({ authSource });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { login } = this.props;
    const { authSource } = this.state;

    return (
      <div id='next-login-container'>
        <Grid container centered columns={1}>
          <Grid.Column id='next-login-column'>
            <Header inverted textAlign='center'>
              <Image centered src={logo} id='next-login-logo'/>
            </Header>
            <LoginForm
              authSource={authSource}
              setAuthSource={this.setAuthSource}
              submit={login}/>
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
    login: (username, password, authSource) =>
      dispatch(AuthActions.loginRequest(username, password, authSource)),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(Login);
