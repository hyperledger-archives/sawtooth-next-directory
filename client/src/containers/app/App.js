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


import './App.css';
import Login from '../login/Login';
import Home from '../home/Home';
import ApproverHome from '../approver-home/ApproverHome';
import Browse from '../browse/Browse';
import Batch from '../batch/Batch';
import Roles from '../roles/Roles';
import Individuals from '../individuals/Individuals';
import Frequent from '../frequent/Frequent';
import Expiring from '../expiring/Expiring';
import Header from '../../components/Header';
import RequesterNav from '../../components/RequesterNav';
import ApproverNav from '../../components/ApproverNav';


import { AuthSelectors } from '../../redux/AuthRedux';
import HomeActions, { HomeSelectors } from '../../redux/RequesterRedux';


let routes;


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

  constructor(props) {
    super(props);
    this.configureRoutes();
  }


  /**
   * 
   * Create an array of routes
   * 
   * The routes in this array are destructured from the declarative
   * syntax due to the added complexity of navigation and state.
   * 
   * State is sent top-down via this.props to the main and nav
   * components.
   * 
   */
  configureRoutes () {
    routes = [
      {
        exact: true,
        path: '/home',
        main: () => <Home {...this.props}/>,
        nav: () => <RequesterNav {...this.props}/>
      },
      {
        exact: true,
        path: '/approval-home',
        main: () => <ApproverHome {...this.props}/>,
        nav: () => <ApproverNav {...this.props}/>
      },
      {
        exact: true,
        path: '/approval-home/batch',
        main: () => <Batch {...this.props}/>,
        nav: () => <ApproverNav {...this.props}/>
      },
      {
        exact: true,
        path: '/approval-home/roles',
        main: () => <Roles {...this.props}/>,
        nav: () => <ApproverNav {...this.props}/>
      },
      {
        exact: true,
        path: '/approval-home/individuals',
        main: () => <Individuals {...this.props}/>,
        nav: () => <ApproverNav {...this.props}/>
      },
      {
        exact: true,
        path: '/approval-home/frequent',
        main: () => <Frequent {...this.props}/>,
        nav: () => <ApproverNav {...this.props}/>
      },
      {
        exact: true,
        path: '/approval-home/expiring',
        main: () => <Expiring {...this.props}/>,
        nav: () => <ApproverNav {...this.props}/>
      }
    ];
  }


  render () {
    const { isAuthenticated } = this.props;

    return (
      <Router>
        <div className='next-container'>
          <Header/>
          <Switch>
            <Route exact path='/login' component={Login}/>
            <Route exact path='/browse' component={Browse}/>
            { !isAuthenticated &&  <Redirect to='/login'/> }
            </Switch>

            { isAuthenticated &&
              <Grid className='next-outer-grid'>
                <Grid.Column id='next-outer-grid-nav' width={4} only='computer'>
                  {routes.map((route, index) => (
                    route.nav &&
                    <Route
                      key={index}
                      path={route.path}
                      exact={route.exact}
                      render={route.nav}
                    />
                  ))}
                </Grid.Column>
                <Grid.Column width={12}>
                  {routes.map((route, index) => ( 
                    <Route
                      key={index}
                      path={route.path}
                      exact={route.exact}
                      render={route.main}
                    />
                  ))}
                </Grid.Column>
              </Grid>
            }
        </div>
      </Router>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    isAuthenticated: AuthSelectors.isAuthenticated(state),
    activePack: HomeSelectors.activePack(state)
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getPackRequest: (id) => dispatch(HomeActions.getPackRequest(id))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
