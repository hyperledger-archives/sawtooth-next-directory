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


import Chat from '../../../components/chat/Chat';
import TrackHeader from '../../../components/layouts/TrackHeader';
import PeopleNav from './PeopleNav';
import Organization from './Organization';
import OrganizationList from './OrganizationList';


import './People.css';
import glyph from '../../../images/header-glyph-individual.png';


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
    this.setState({ activeUser });
  };


  handleOnBehalfOf = () => {
    const { setOnBehalfOf } = this.props;
    const { activeUser } = this.state;
    console.log('activeUser: ');
    console.log(activeUser);
    setOnBehalfOf(activeUser);
  }


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
          <TrackHeader
            inverted
            glyph={glyph}
            title='People'
            {...this.props}/>
          <div id='next-approver-people-content'>
            <PeopleNav
              activeIndex={activeIndex}
              setFlow={this.setFlow}/>
            <div>
              { activeIndex === 0 &&
                <OrganizationList {...this.props}/>
                // <h1>All people</h1>
              }
              { activeIndex === 1 &&
                <Organization
                  handleUserSelect={this.handleUserSelect}
                  {...this.props}/>
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
            handleOnBehalfOf={this.handleOnBehalfOf}
            activeUser={activeUser}
            {...this.props}/>
        </Grid.Column>
      </Grid>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    fetchingAllUsers: state.user.fetchingAllUsers,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(People);
