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
import { BrowserRouter as Router, Route, Redirect, Switch } from 'react-router-dom';


import Login from '../login/Login';
import Header from '../../components/layouts/Header';
import Browse from '../browse/Browse';
import './App.css';


import AuthActions,{ AuthSelectors } from '../../redux/AuthRedux';
import ChatActions, { ChatSelectors } from '../../redux/ChatRedux';
import RequesterActions, { RequesterSelectors } from '../../redux/RequesterRedux';
import UserActions, { UserSelectors } from '../../redux/UserRedux';


import PropTypes from 'prop-types';


/**
 *
 * @class App
 * Component encapsulating the navigation implementation based on
 * React Router. Routes pathways are composed from two top-level components
 * to provide one navigation container and one main area.
 *
 * Component communication should be synced only through the Redux store.
 *
 */
class App extends Component {

  /**
   *
   * Hydrate base data
   *
   */
  componentDidMount () {
    const { getBase, getUser, isAuthenticated } = this.props;

    if (isAuthenticated) {
      getUser();
      getBase();
    }

  }


  componentWillReceiveProps (newProps) {
    const { getBase, getUser, isAuthenticated } = this.props;

    if (newProps.isAuthenticated &&
      newProps.isAuthenticated !== isAuthenticated) {
      getUser();
      getBase();
    }

    if (!newProps.isAuthenticated) {

    }
  }


  /**
   *
   * Render grid system
   *
   * Create a 2-up top-level grid structure that separates the
   * sidebar from main content. Each route is mapped via its own
   * route component.
   *
   */
  renderGrid () {
    return (
      <Grid id='next-outer-grid'>
        <Grid.Column id='next-outer-grid-nav' width={3} only='computer'>
          { this.routes.map((route, index) => (
            route.nav &&
            <Route
              key={index}
              path={route.path}
              exact={route.exact}
              render={route.nav}
            />
          ))}
        </Grid.Column>
        <Grid.Column id='next-inner-grid-main' width={13}>
          { this.routes.map((route, index) => (
            <Route
              key={index}
              path={route.path}
              exact={route.exact}
              render={route.main}
            />
          ))}
        </Grid.Column>
      </Grid>
    )
  }


  render () {
    const { isAuthenticated, routes } = this.props;
    this.routes = routes(this.props);

    return (
      <Router>
        <div id='next-global-container'>
          <Header {...this.props}/>
          <Switch>
            <Route exact path='/login' component={Login}/>
            <Route exact path='/sign-up' component={Login}/>

            { !isAuthenticated && <Redirect to='/login'/> }

            <Route exact path='/' render={() => (
              isAuthenticated ?
                (<Redirect to="/home"/>) :
                (<Redirect to='/login'/>)
            )}/>

            <Route exact path='/browse' component={Browse}/>
            <Route render={() => ( this.renderGrid() )}/>
          </Switch>
        </div>
      </Router>
    );
  }

}


App.proptypes = {
  isAuthenticated: PropTypes.bool,
  routes: PropTypes.func
};


const logout = (dispatch) => {
  return dispatch(AuthActions.logoutRequest()) &&
         dispatch(UserActions.meReset())
}


const mapStateToProps = (state) => {
  return {
    isAuthenticated:  AuthSelectors.isAuthenticated(state),
    recommended:      RequesterSelectors.recommended(state),
    activePack:       RequesterSelectors.activePack(state),
    activeProposal:   RequesterSelectors.activeProposal(state),
    me:               UserSelectors.me(state),
    requests:         UserSelectors.requests(state),
    messages:         ChatSelectors.messages(state),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getUser:         () => dispatch(UserActions.meRequest()),
    getBase:         () => dispatch(RequesterActions.baseRequest()),
    getPack:         (id) => dispatch(RequesterActions.packRequest(id)),
    getProposal:     (id) => dispatch(RequesterActions.proposalRequest(id)),
    requestAccess:   (id, userId, reason) => {
      return dispatch(RequesterActions.accessRequest(id, userId, reason))
    },

    sendMessage:     (message) => dispatch(ChatActions.sendRequest(message)),
    getConversation: (id) => dispatch(ChatActions.conversationRequest(id)),

    logout:          () => logout(dispatch),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
