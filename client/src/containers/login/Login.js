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
import { Grid } from 'semantic-ui-react';


import PropTypes from 'prop-types';


import './Login.css';
import AuthActions, { AuthSelectors } from '../../redux/AuthRedux';
import LoginForm from '../../components/forms/LoginForm';
import SignupForm from '../../components/forms/SignupForm';
import Toast from '../../components/toast/toast';


/**
 * 
 * @class Login
 * Component encapsulating the login landing page.
 * 
 */
class Login extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isToastOpen: false,
      toastMessage: ''
    }
    this.closeToast = this.closeToast.bind(this);
  }

  componentWillMount() {
    const { isAuthenticated } = this.props;
    if (isAuthenticated) {
      this.props.history.push('/home');
    }
  }

  /**
   * 
   * Once the user is authenticated, redirect to landing page
   * 
   * @param {*} newProps 
   * 
   */
  componentWillReceiveProps(newProps) {
    this.props = newProps;
    if (newProps.isAuthenticated) {

      // TODO: Consider pulling from a user-saved cache
      this.props.history.push('/home');
    }
    if (newProps.error) {
      /**
       * Open toast to display the error response
       * 
       */
      this.setState({
        isToastOpen: true,
        toastMessage: newProps.error
      });
    }
  }

  closeToast() {
    this.setState({
      isToastOpen: false,
      toastMessage: ''
    })
  }

  render() {
    const { attemptLogin, attemptSignup } = this.props;
    const { isToastOpen, toastMessage } = this.state;

    let formDom = (this.props.location.pathname === '/sign-up' ? <SignupForm submit={attemptSignup} /> : <LoginForm submit={attemptLogin} />);

    return (
      <Grid centered columns={2}>
        <Grid.Column className='next-login-column'>
          {formDom}
        </Grid.Column>
        <Toast
          open={isToastOpen}
          close={this.closeToast}
          message={toastMessage}
          timeout={10000}
          title='Authentication Error' />
      </Grid>
    );
  }

}


Login.prototypes = {
  isAuthenticated: PropTypes.bool,
  attemptLogin: PropTypes.func.isRequired
};


const mapStateToProps = (state) => {
  return {
    error: state.auth.error,
    isAuthenticated: AuthSelectors.isAuthenticated(state)
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    attemptLogin: (email, password) => dispatch(AuthActions.loginRequest(email, password)),
    attemptSignup: (name, username, password, email) => dispatch(AuthActions.signupRequest(name, username, password, email))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Login);
