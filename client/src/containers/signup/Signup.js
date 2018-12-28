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
import AuthActions, { AuthSelectors } from 'redux/AuthRedux';
import SignupForm from 'components/forms/SignupForm';
import logo from 'images/next-logo-billboard.png';


import * as storage from 'services/Storage';
import * as utils from 'services/Utils';


/**
 *
 * @class         Signup
 * @description   Component encapsulating the signup landing page
 *
 */
class Signup extends Component {

  static propTypes = {
    history:                PropTypes.object,
    isAuthenticated:        PropTypes.bool,
    recommendedPacks:       PropTypes.array,
    recommendedRoles:       PropTypes.array,
    signup:                 PropTypes.func.isRequired,
  };


  /**
   * Entry point to perform tasks required to render
   * component
   */
  componendDidMount () {
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
    const { history,
      isAuthenticated,
      recommendedPacks,
      recommendedRoles } = this.props;
    if(isAuthenticated) {
      history.push(
        storage.getViewState() ?
          '/approval/pending/individual' :
          utils.createHomeLink(recommendedPacks, recommendedRoles)
      );
    }
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render() {
    const { signup } = this.props;

    return (
      <div id='next-login-container'>
        <Grid container centered columns={2}>
          <Grid.Column id='next-login-column'>
            <Header inverted textAlign='center'>
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
    isAuthenticated: AuthSelectors.isAuthenticated(state),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    signup: (name, username, password, email) =>
      dispatch(AuthActions.signupRequest(name, username, password, email)),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(Signup);
