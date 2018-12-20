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


import './People.css';
import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import PeopleNav from '../../components/nav/PeopleNav';
import Organization from '../../components/layouts/Organization';


/**
 *
 * @class         People
 * @description   People component
 *
 */
class People extends Component {

  state = {
    activeIndex:    0,
    activeUser:     null,
  };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    document.querySelector('body').classList.add('dark');
    document.querySelector('body').classList.add('minimal');
  }


  /**
  * Component teardown
  */
  componentWillUnmount () {
    document.querySelector('body').classList.remove('dark');
    document.querySelector('body').classList.remove('minimal');
  }


  /**
   * Switch between Roles and People views
   * @param {number} activeIndex Current screen index
   */
  setFlow = (activeIndex) => {
    this.setState({ activeIndex });
  };


  /**
   * Handle user change event
   * @param {object} activeUser User ID
   */
  handleUserSelect = (activeUser) => {
    console.log(activeUser);
    this.setState({ activeUser });
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { activeIndex, activeUser } = this.state;
    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={12}>
          <TrackHeader title='People' {...this.props}/>
          <div id='next-approver-people-content'>
            <PeopleNav
              activeIndex={activeIndex}
              setFlow={this.setFlow}/>
            <div>
              { activeIndex === 0 &&
                <Organization
                  handleUserSelect={this.handleUserSelect}
                  {...this.props}/>
              }
              { activeIndex === 1 &&
                <h1>All people</h1>
              }
            </div>
          </div>
        </Grid.Column>
        <Grid.Column
          id='next-approver-grid-converse-column'
          width={4}>
          <Chat
            disabled
            type='APPROVER'
            organization
            activeUser={activeUser}
            {...this.props}/>
        </Grid.Column>
      </Grid>
    );
  }

}


const mapStateToProps = (state) => {
  return {};
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(People);
