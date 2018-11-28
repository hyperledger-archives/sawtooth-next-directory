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
import PropTypes from 'prop-types';


import './App.css';
import Browse from '../browse/Browse';
import Header from '../../components/layouts/Header';
import Login from '../login/Login';
import Signup from '../signup/Signup';
import Waves from '../../components/layouts/Waves';


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
 *
 */
class App extends Component {

  static propTypes = {
    isAuthenticated: PropTypes.bool,
    routes: PropTypes.func
  };


  /**
   *
   * Hydrate user object
   *
   */
  componentDidMount () {
    const { isAuthenticated } = this.props;
    isAuthenticated && this.hydrate();
  }


  componentDidUpdate (prevProps) {
    const {
      me,
      id,
      isAuthenticated,
      isSocketOpen,
      sendMessage } = this.props;

    if (!isAuthenticated) return;

    // On receiving new props, if user authentication
    // state changes, we know that a user has logged in,
    // so get hydrate user and recommended objects
    if (prevProps.isAuthenticated !== isAuthenticated) {
      this.hydrate();
    }

    if (prevProps.isSocketOpen !== isSocketOpen) {
      sendMessage({do: "CREATE", user_id: id, message: "hi"});
    }

    // After the user object is populated, the following
    // will get the info required to display data in the
    // sidebar.
    //
    // ! Note this will be outmoded after API changes
    //
    if (prevProps.me !== me) {
      this.hydrateSidebar();
    }
  }


  hydrate () {
    const { getBase, getMe, getOpenProposals } = this.props;

    getMe();
    getBase();
    getOpenProposals();
  }


  // proposals is array of objects of form { object_id, proposal_id }
  hydrateSidebar () {
    const { getProposals, getRoles, me, roles } = this.props;

    // * (1) Map proposals and memberOf to ID array
    let foo = [
      ...me.proposals,
      ...me.memberOf
    ].map((item) =>
      typeof item  === 'object' ?
        item['object_id'] :
        item)

    // * (2) Find roles we don't already have loaded in
    if (roles) {
      foo = foo.filter(item =>
        roles.find(role => role.id === item));
    }

    let bar = me.proposals.map(item =>
        item['proposal_id']);

    // * (3) Load roles not in
    getProposals(bar);
    getRoles(foo);
  }


  renderNav() {
    return this.routes.map((route, index) => (
      route.nav &&
      <Route
        key={index}
        path={route.path}
        exact={route.exact}
        render={route.nav}
      />
    ));
  }


  renderMain() {
    return this.routes.map((route, index) => (
      <Route
        key={index}
        path={route.path}
        exact={route.exact}
        render={route.main}
      />
    ));
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
        <Grid.Column id='next-outer-grid-nav'>
          { this.renderNav() }
        </Grid.Column>
        <Grid.Column id='next-inner-grid-main'>
          <Waves {...this.props}/>
          { this.renderMain() }
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
            <Route exact path='/signup' component={Signup}/>
            { !isAuthenticated && <Redirect to='/login'/> }
            <Route exact path='/browse' component={Browse}/>
            <Route render={() => ( this.renderGrid() )}/>
          </Switch>
        </div>
      </Router>
    );
  }

}


const mapStateToProps = (state) => appState(state);
const mapDispatchToProps = (dispatch) => appDispatch(dispatch);


export default connect(mapStateToProps, mapDispatchToProps)(App);
