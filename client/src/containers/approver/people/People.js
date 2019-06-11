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


import Chat from 'components/chat/Chat';
import TrackHeader from 'components/layouts/TrackHeader';
import PeopleNav from './PeopleNav';
import Organization from './Organization';
import UserRoles from './UserRoles';
import OrganizationList from './OrganizationList';


import './People.css';


/**
 *
 * @class         People
 * @description   People component
 *
 */
class People extends Component {

  state = {
    searchInput:    '',
    searchStart:    1,
    searchLimit:    20,
    searchTypes:    ['user'],
    activeIndex:    0,
    activeUser:     null,
  };


  /**
  * Component teardown
  */
  componentWillUnmount () {
    const { clearSearchData } = this.props;
    clearSearchData();
  }


  /**
   * Switch between Roles and People views
   * @param {number} activeIndex Current screen index
   */
  setFlow = (activeIndex) => {
    window.scrollTo(0, 0);
    this.setState({ activeIndex });
  };


  /**
   * Handle user change event
   * @param {object} activeUser User ID
   */
  handleUserSelect = (activeUser) => {
    activeUser && this.setState({ activeUser });
  };


  handleOnBehalfOf = () => {
    const { setOnBehalfOf } = this.props;
    const { activeUser } = this.state;
    setOnBehalfOf(activeUser);
  }


  /**
   * Set search input state
   * @param {string} searchInput Search input value
   */
  setSearchInput = (searchInput) => {
    this.setState({ searchInput });
  }


  /**
   * Set search start state
   * @param {string} searchStart Search start value
   */
  setSearchStart = (searchStart) => {
    this.setState({ searchStart });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { fetchingSearchResults } = this.props;
    const {
      activeIndex,
      activeUser,
      searchInput,
      searchLimit,
      searchStart,
      searchTypes } = this.state;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={12}>
          <TrackHeader
            inverted
            title='People'
            subtitle='Browse all of the people within your organization'
            {...this.props}/>
          <div id='next-approver-people-content'>
            <PeopleNav
              fetchingSearchResults={fetchingSearchResults}
              searchInput={searchInput}
              searchLimit={searchLimit}
              searchTypes={searchTypes}
              setSearchInput={this.setSearchInput}
              setSearchStart={this.setSearchStart}
              activeIndex={activeIndex}
              setFlow={this.setFlow}
              {...this.props}/>
            <div>
              { activeIndex === 0 &&
                <OrganizationList
                  fetchingSearchResults={fetchingSearchResults}
                  searchInput={searchInput}
                  searchLimit={searchLimit}
                  searchStart={searchStart}
                  searchTypes={searchTypes}
                  setSearchStart={this.setSearchStart}
                  handleUserSelect={this.handleUserSelect}
                  {...this.props}/>
              }
              { activeIndex === 1 &&
                <Organization
                  activeUser={activeUser}
                  showPeers
                  handleUserSelect={this.handleUserSelect}
                  {...this.props}/>
              }
              { activeIndex === 2 &&
                <UserRoles
                  activeUser={activeUser}
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
            type='PEOPLE'
            handleOnBehalfOf={this.handleOnBehalfOf}
            activeUser={activeUser}
            activeIndex={activeIndex}
            handleUserSelect={this.handleUserSelect}
            setFlow={this.setFlow}
            {...this.props}/>
        </Grid.Column>
      </Grid>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    fetchingOrganization:  state.approver.fetchingOrganization,
    fetchingPeople:        state.user.fetchingPeople,
    fetchingSearchResults: state.search.fetching,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(People);
