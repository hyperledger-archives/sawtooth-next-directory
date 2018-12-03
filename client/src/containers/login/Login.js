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
import { Container, Grid, Header, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import AuthActions, { AuthSelectors } from '../../redux/AuthRedux';
import LoginForm from '../../components/forms/LoginForm';
import * as utils from '../../services/Utils';


import './Login.css';
import logo from '../../images/next-logo-billboard.png';


/**
 *
 * @class         Login
 * @description   Component encapsulating the login landing page
 *
 *
 */
class Login extends Component {

  static propTypes = {
    history:              PropTypes.object,
    isAuthenticated:      PropTypes.bool,
    login:                PropTypes.func.isRequired,
    recommended:          PropTypes.array,
  };


  componentDidMount () {
    const { history, isAuthenticated, recommended } = this.props;

    const homeLink = recommended && recommended[0] ?
      `/roles/${utils.createSlug(recommended[0].name)}` :
      '/';

    isAuthenticated && history.push(homeLink);
  }


  componentDidUpdate (prevProps) {
    const { history, isAuthenticated, recommended } = this.props;

    const homeLink = recommended && recommended[0] ?
      `/roles/${utils.createSlug(recommended[0].name)}` :
      '/';

    isAuthenticated && history.push(homeLink);
  }


  render() {
    const { login } = this.props;

    return (
      <div id='next-login-container'>
        <Grid container centered columns={1}>
          <Grid.Column id='next-login-column'>
            <Header color='grey' textAlign='center'>
              <Image centered src={logo} id='next-login-logo'/>
              <h1>Sign in to NEXT Directory</h1>
            </Header>
            <LoginForm submit={login}/>
          </Grid.Column>
        </Grid>
        <Container id='next-login-new-account-container' textAlign='center'>
          <span>New to NEXT Directory?</span>
          <Link to='/signup'>Create an account</Link>
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
}

const mapDispatchToProps = (dispatch) => {
  return {
    login: (email, password) =>
      dispatch(AuthActions.loginRequest(email, password)),
    attemptSignup: (name, username, password, email) =>
      dispatch(AuthActions.signupRequest(name, username, password, email)),
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(Login);
