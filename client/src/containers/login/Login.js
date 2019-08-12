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
import { Button, Container, Grid, Header, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './Login.css';
import logo from 'images/next-logo-primary.png';
import cloud from 'images/cloud.svg';
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


  themes = ['flux'];


  /**
   * Entry point to perform tasks required to render
   * component
   */
  componentDidMount () {
    const { resetErrors } = this.props;
    theme.apply(this.themes);
    resetErrors();
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @returns {undefined}
   */
  componentDidUpdate () {
    this.init();
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
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { login } = this.props;

    return (
      <div id='next-login-container'>
        <div id='next-login-panel'>
          <Grid container centered columns={1}>
            <Grid.Column id='next-login-column'>
              <Header textAlign='center'>
                <Image centered src={logo} id='next-login-logo'/>
                <h1>
                  SIGN IN
                </h1>
              </Header>
              <LoginForm
                submit={login}
                {...this.props}/>
              { process.env.REACT_APP_ENABLE_LDAP_SYNC === '1' &&
                <Container
                  id='next-login-new-account-container'
                  textAlign='center'>
                  <div>
                    Don&apos;t have a CORP ID?
                    <div>
                      <Button
                        as={Link}
                        to='/signup'
                        id='next-login-signup-link'
                        content='Sign up'
                        type='button'
                        icon='chevron right'
                        labelPosition='right'/>
                    </div>
                  </div>
                </Container>
              }
            </Grid.Column>
          </Grid>
        </div>
        <Container id='next-login-watermark' fluid textAlign='left'>
          <Image src={cloud}/>
        </Container>
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
    login: (username, password) =>
      dispatch(AuthActions.loginRequest(username, password)),
    resetErrors: () => dispatch(AuthActions.resetErrors()),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(Login);
