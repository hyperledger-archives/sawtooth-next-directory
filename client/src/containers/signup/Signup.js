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
import { Grid, Header, Image } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './Signup.css';
import AuthActions, { AuthSelectors } from '../../redux/AuthRedux';
import SignupForm from '../../components/forms/SignupForm';
import * as utils from '../../services/Utils';
import logo from '../../images/next-logo-billboard.png';


/**
 *
 * @class         Signup
 * @description   Component encapsulating the signup landing page
 *
 */
class Signup extends Component {

  static propTypes = {
    isAuthenticated: PropTypes.bool,
    signup: PropTypes.func.isRequired
  };


  componentWillMount() {
    const { history, isAuthenticated, recommended } = this.props;

    const homeLink = recommended && recommended[0] ?
      `/roles/${utils.createSlug(recommended[0].name)}` :
      '/';

    isAuthenticated && history.push(homeLink);
  }


  componentWillReceiveProps(newProps) {
    const { history, recommended } = this.props;

    const homeLink = recommended && recommended[0] ?
    `/roles/${utils.createSlug(recommended[0].name)}` :
    '/';

    newProps.isAuthenticated && history.push(homeLink);
  }


  render() {
    const { signup } = this.props;

    return (
      <div id='next-login-container'>
        <Grid container centered columns={2}>
          <Grid.Column id='next-login-column'>
            <Header color='grey' textAlign='center'>
              <Image centered src={logo} id='next-login-logo'/>
              <h1>Create an account</h1>
            </Header>
            <SignupForm submit={signup}/>
          </Grid.Column>
        </Grid>
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    error: state.auth.error,
    isAuthenticated: AuthSelectors.isAuthenticated(state)
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    signup: (name, username, password, email) =>
      dispatch(AuthActions.signupRequest(name, username, password, email))
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(Signup);
