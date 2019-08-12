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
import { Grid } from 'semantic-ui-react';
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  Switch } from 'react-router-dom';
import PropTypes from 'prop-types';


import './App.css';
import Browse from 'containers/browse/Browse';
import Login from 'containers/login/Login';
import Signup from 'containers/signup/Signup';
import Header from 'components/layouts/Header';
import Waves from 'components/layouts/Waves';
import NotFound from 'components/layouts/NotFound';
import Snapshot from 'containers/approver/snapshot/Snapshot';


import { appDispatch, appState } from './AppHelper';


/**
 *
 * @class         App
 * @description   Component encapsulating navigation. Route pathways
 *                are composed from two top-level components, creating
 *                one nav and one main area per component.
 *
 *                Component communication should be done only using
 *                the Redux store.
 */
class App extends Component {

  static propTypes = {
    isAuthenticated: PropTypes.bool,
    routes: PropTypes.func,
  };


  /**
   * Entry point to perform tasks required to render
   * component. If authenticated, hydate data and open socket.
   */
  componentDidMount () {
    const { isAuthenticated, openSocket } = this.props;
    isAuthenticated && this.hydrate();
    if (isAuthenticated) {
      openSocket('chatbot');
      openSocket('feed');

      // TODO: Needs more logic
      // this.wait = setTimeout(forceSocketError, SOCKET_TIMEOUT);
    }
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const {
      closeSocket,
      me,
      isSocketOpen,
      isAuthenticated,
      isRefreshing,
      stopRefresh,
      openSocket } = this.props;

    if (!isAuthenticated) {
      isSocketOpen('chatbot') && closeSocket('chatbot');
      isSocketOpen('feed') && closeSocket('feed');
      return;
    }

    // On receiving new props, if user authentication
    // state changes, we know that a user has logged in,
    // so get hydrate user and recommended objects
    if (prevProps.isAuthenticated !== isAuthenticated) {
      openSocket('chatbot');
      openSocket('feed');
      this.hydrate();
    }

    if (prevProps.isRefreshing !== isRefreshing) {
      this.hydrate();
      stopRefresh();
    }

    // After the user object is populated, the following
    // will get the info required to display data in the
    // sidebar.
    if (prevProps.me !== me)
      this.hydrateSidebar();

    // TODO: Needs more logic
    // if (messages !== prevProps.messages)
    //   clearTimeout(this.wait);
  }


  /**
   * Update user, recommended resources, and open requests
   */
  hydrate () {
    const { getBase, getMe, getOpenProposals } = this.props;

    getMe();
    getBase();
    getOpenProposals();
  }


  /**
   * Get open request, role, and pack data needed to
   * display resource names in the navbar
   */
  hydrateSidebar () {
    const {
      getPacks,
      getProposals,
      getRoles,
      me,
      packs,
      roles,
      defaultUser } = this.props;

    const user = defaultUser ? defaultUser : me;

    // Populate proposal ID array
    const proposalIds = user.proposals.map(
      item => item.proposal_id
    );

    // Populate role ID array
    let roleIds = [
      ...user.proposals,
      ...user.memberOf,
    ].map(item =>
      typeof item  === 'object' ?
        item.object_id :
        item);

    // Populate pack ID array
    let packIds = user && user.proposals.map(
      item => item.pack_id
    ).filter(item => item);

    // Find packs and roles not loaded in
    if (roles && roles.length) {
      roleIds = roleIds.filter(
        item => !roles.find(role => role.id === item)
      );
    }
    if (packs & packs.length) {
      packIds = packIds.filter(
        item => !packs.find(pack => pack.id === item)
      );
    }

    // Fetch roles, packs, and proposals
    getProposals(proposalIds);
    getPacks([...new Set(packIds)]);
    getRoles(roleIds);
  }


  /**
   * Render grid system
   * Create a 2-up top-level grid structure that separates the
   * sidebar from main content. Each route is mapped via its own
   * route component.
   *
   * @param {function}  nav Nav component
   * @param {function} main Main component
   * @param {object}  props React Router props
   * @returns {JSX}
   */
  renderGrid (nav, main, props) {
    return (
      <Grid id='next-outer-grid'>
        <Grid.Column id='next-outer-grid-nav'>
          { nav(props) }
        </Grid.Column>
        <Grid.Column id='next-inner-grid-main'>
          <Waves {...this.props}/>
          { main(props) }
        </Grid.Column>
      </Grid>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { isAuthenticated, routes } = this.props;
    this.routes = routes(this.props);

    return (
      <Router>
        <div id='next-global-container'>
          <Header {...this.props}/>
          <Switch>
            <Route exact path='/login' component={Login}/>
            { process.env.REACT_APP_ENABLE_LDAP_SYNC === '1' &&
              <Route exact path='/signup' component={Signup}/>
            }
            { !isAuthenticated && <Redirect to='/login'/> }
            <Route
              exact
              path='/browse'
              render={() => <Browse {...this.props}/>}/>
            <Route
              exact
              path='/snapshot'
              render={() => <Snapshot {...this.props}/>}/>
            { this.routes &&
              this.routes.map((route, index) => (
                <Route
                  key={index}
                  path={route.path}
                  exact={route.exact}
                  render={props =>
                    this.renderGrid(route.nav, route.main, props)
                  }/>
              ))}
            <Route render={() => <NotFound {...this.props}/>}/>
          </Switch>
        </div>
      </Router>
    );
  }

}


const mapStateToProps = (state) => appState(state);
const mapDispatchToProps = (dispatch) => appDispatch(dispatch);
export default connect(mapStateToProps, mapDispatchToProps)(App);
