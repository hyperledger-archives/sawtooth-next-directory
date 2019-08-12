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


import './Signup.css';
import { AuthActions, AuthSelectors } from 'state';
import SignupForm from './SignupForm';
import logo from 'images/next-logo-primary.png';
import cloud from 'images/cloud.svg';


import * as storage from 'services/Storage';
import * as theme from 'services/Theme';
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
    resetErrors:            PropTypes.func,
    signup:                 PropTypes.func.isRequired,
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
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    this.init();
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    const { history } = this.props;
    !history.location.pathname.includes('login') &&
      theme.remove(this.themes);
  }


  /**
   * On authentication, determine home URL and redirect
   */
  init () {
    const { history,
      isAuthenticated,
      recommendedPacks,
      recommendedRoles } = this.props;
    if (isAuthenticated) {
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
  render () {
    const { signup } = this.props;

    return (
      <div id='next-signup-container'>
        <div id='next-signup-panel'>
          <Grid container centered columns={2}>
            <Grid.Column id='next-signup-column'>
              <Header textAlign='center'>
                <Image centered src={logo} id='next-signup-logo'/>
                <h1>
                  SIGN UP
                </h1>
              </Header>
              <Button
                as={Link}
                to='/login'
                id='next-signup-back-button'
                content='Back to login'
                type='button'
                icon='chevron left'
                labelPosition='left'/>
              <Header as='h3' textAlign='center'>
                Request a CORP Account
              </Header>
              <SignupForm submit={signup}/>
            </Grid.Column>
          </Grid>
        </div>
        <Container id='next-signup-watermark' fluid textAlign='left'>
          <Image src={cloud}/>
        </Container>
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    isAuthenticated: AuthSelectors.isAuthenticated(state),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    resetErrors: () => dispatch(AuthActions.resetErrors()),
    signup: (username, password) =>
      dispatch(AuthActions.signupRequest(username, password)),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(Signup);
