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
import { Grid, Icon, Sidebar, Menu } from 'semantic-ui-react';
import { BrowserRouter as Router, Route, Redirect, Switch } from 'react-router-dom';
import PropTypes from 'prop-types';


import './App.css';
import Browse from '../browse/Browse';
import Header from '../../components/layouts/Header';
import Login from '../login/Login';


import { appDispatch, appState } from './AppHelper';


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

  state = { isSideBarVisible: false };


  handleSidebarHide = () => {
    this.setState({ isSideBarVisible: false });
  }


  handleShowClick = () => {
    const { isSideBarVisible } = this.state;
    this.setState({ isSideBarVisible: !isSideBarVisible });
  }


  /**
   *
   * Hydrate user object
   *
   */
  componentDidMount () {
    const { isAuthenticated } = this.props;
    isAuthenticated && this.hydrate();
  }


  componentWillReceiveProps (newProps) {
    const { me, isAuthenticated } = this.props;

    if (!newProps.isAuthenticated) return;

    // On receiving new props, if user authentication
    // state changes, we know that a user has logged in,
    // so get hydrate user and recommended objects
    if (newProps.isAuthenticated !== isAuthenticated) {
      this.hydrate();
    }

    // After the user object is populated, the following
    // will get the info required to display data in the
    // sidebar.
    //
    // ! Note this will be outmoded after API changes
    //
    if (newProps.me !== me) {
      this.hydrateSidebar(newProps);
    }
  }


  hydrate () {
    const { getBase, getMe } = this.props;

    getMe();
    getBase();
  }


  hydrateSidebar (newProps) {
    const { getRoles, roles } = this.props;

    let foo = [
      ...newProps.me.proposals,
      ...newProps.me.memberOf
    ].map((item) =>
      typeof item  === 'object' ?
        item['object_id'] :
        item)

    if (roles) {
      foo = foo.filter(item =>
        roles.find(role => role.id === item));
    }

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
    const { isSideBarVisible } = this.state;

    return (
      <Grid id='next-outer-grid'>

        <Grid.Column
          id='next-outer-grid-nav'
          only='computer'>
          { this.renderNav() }
        </Grid.Column>

        <Grid.Column
          id='next-inner-grid-main'
          only='computer'>
          { this.renderMain() }
        </Grid.Column>

        <Grid.Column
          mobile={16}
          tablet={16}
          id='next-inner-grid-main'
          only='tablet mobile'>
          <Sidebar.Pushable>
            <Sidebar
              as={Menu}
              animation='overlay'
              inverted
              onHide={this.handleSidebarHide}
              vertical
              visible={isSideBarVisible}
              width='wide'>
              <div id='next-hamburger-wrapper'>
                { this.renderNav() }
              </div>
            </Sidebar>
            <Sidebar.Pusher dimmed={isSideBarVisible}>
              { this.renderMain() }
            </Sidebar.Pusher>
          </Sidebar.Pushable>
        </Grid.Column>

        <div id='next-hamburger-icon'>
          <Icon onClick={this.handleShowClick} name='bars'/>
        </div>
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
            <Route exact path='/signup' component={Login}/>

            { !isAuthenticated && <Redirect to='/login'/> }

            <Route exact path='/' render={() => (
              isAuthenticated ?
                (<Redirect to='/home'/>) :
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


const mapStateToProps = (state) => appState(state);
const mapDispatchToProps = (dispatch) => appDispatch(dispatch);


export default connect(mapStateToProps, mapDispatchToProps)(App);
