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
import {
  Button,
  Container,
  Grid,
  Header,
  Icon,
  Placeholder } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './RoleSelectGrid.css';
import Avatar from 'components/layouts/Avatar';
import RoleSelectGridNav from 'components/nav/RoleSelectGridNav';
import * as utils from 'services/Utils';


/**
 *
 * @class         RoleSelectGrid
 * @description   Component encapsulating a role selection grid
 *                used for associating roles with a given pack.
 */
class RoleSelectGrid extends Component {

  static propTypes = {
    fetchingAllRoles: PropTypes.bool,
    getAllRoles:      PropTypes.func,
    handleClick:      PropTypes.func,
    roles:            PropTypes.array,
    rolesTotalCount:  PropTypes.number,
    selectedRoles:    PropTypes.array,
  };


  state = {
    searchInput:    '',
    searchStart:    1,
    searchLimit:    20,
    searchTypes:    ['role'],
    start:          0,
    limit:          25,
  };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    this.loadNext(0);
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { roles } = this.props;
    if (roles && prevProps.roles.length !== roles.length)
      this.init();
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    const { clearSearchData } = this.props;
    clearSearchData();
  }


  /**
   * Determine which owners are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const { getUsers, roles, users } = this.props;
    if (!roles) return;
    const owners = [
      ...new Set(
        roles.map(role => role.owners).flat()
      ),
    ];
    const diff = owners.filter(userId =>
      !users || !users.find(user => user.id === userId)
    );
    diff && getUsers(diff, true);
  }


  /**
   * Load next set of data
   * @param {number} start Loading start index
   */
  loadNext = (start) => {
    const { getAllRoles } = this.props;
    const { limit } = this.state;
    if (start === undefined || start === null)
      start = this.state.start;

    getAllRoles(start, limit);
    this.setState({ start: start + limit });
  }


  /**
   * Load next set of search data
   * @param {number} start Loading start index
   */
  loadNextSearch = () => {
    const { search } = this.props;
    const {
      searchInput,
      searchLimit,
      searchStart,
      searchTypes } = this.state;

    const query = {
      query: {
        search_input: searchInput,
        search_object_types: searchTypes,
        page_size: searchLimit,
        page: searchStart + 1,
      },
    };

    this.setState({ searchStart: searchStart + 1 });
    search('browse', query);
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
   * Render placeholder graphics
   * @returns {JSX}
   */
  renderPlaceholder = () => {
    return Array(6).fill(0).map((item, index) => (
      <Grid.Column key={index} width={5}>
        <Placeholder fluid className='contrast'>
          <Placeholder.Header>
            <Placeholder.Line length='full'/>
          </Placeholder.Header>
          <Placeholder.Paragraph>
            <Placeholder.Line length='medium'/>
            <Placeholder.Line length='short'/>
          </Placeholder.Paragraph>
        </Placeholder>
      </Grid.Column>
    ));
  }


  /**
   * Render role owner(s) info
   * @param {array} owners Array of owners of
   *                       a given role
   * @returns {JSX}
   */
  renderOwners = (owners) => {
    const { userFromId } = this.props;
    if (!owners.length) return null;
    const user = userFromId(owners[0]);
    return (
      <div className='next-role-select-grid-owners'>
        <Avatar
          userId={owners[0]}
          size='small'
          {...this.props}/>
        <div className='next-role-select-grid-owner-label'>
          {user && user.name}
        </div>
      </div>
    );
  }


  /**
   * Render role toggle button
   * @param {string} role Role
   * @returns {JSX}
   */
  renderRoleToggle = (role) => {
    const { handleClick, selectedRoles } = this.props;
    return (
      <div>
        <Button
          fluid
          toggle
          className='toggle-card gradient'
          active={selectedRoles.includes(role.id)}
          onClick={() => handleClick(role.id)}
          size='massive'>
          <h3>
            {role.name}
          </h3>
          { role.owners &&
            this.renderOwners(role.owners)
          }
          { selectedRoles.includes(role.id) &&
            <Icon name='check' color='pink'/>
          }
        </Button>
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      fetchingAllRoles,
      fetchingSearchResults,
      roles,
      roleSearchData,
      rolesTotalCount,
      totalSearchPages } = this.props;
    const {
      limit,
      searchInput,
      searchLimit,
      searchStart,
      searchTypes } = this.state;

    const showSearchData = !utils.isWhitespace(searchInput);

    return (
      <div id='next-role-select-grid-container'>
        <RoleSelectGridNav
          fetchingSearchResults={fetchingSearchResults}
          searchInput={searchInput}
          searchLimit={searchLimit}
          searchTypes={searchTypes}
          setSearchInput={this.setSearchInput}
          setSearchStart={this.setSearchStart}
          {...this.props}/>
        <Grid centered columns={3} id='next-role-select-grid'>
          { showSearchData && roleSearchData &&
            roleSearchData.map(role => (
              <Grid.Column key={role.id} width={5}>
                {this.renderRoleToggle(role)}
              </Grid.Column>
            ))
          }
          { !showSearchData &&
            roles &&
            (roles.length >= limit || !fetchingAllRoles) &&
            roles.map(role => (
              <Grid.Column key={role.id} width={5}>
                {this.renderRoleToggle(role)}
              </Grid.Column>
            ))
          }
          { (fetchingAllRoles || fetchingSearchResults) &&
            this.renderPlaceholder()
          }
        </Grid>
        { roles && roles.length === 0 && !fetchingAllRoles &&
          <Container
            id='next-role-select-grid-no-items'
            textAlign='center'>
            <Header as='h3' textAlign='center' color='grey'>
              <Header.Content>
                No roles available
              </Header.Content>
            </Header>
          </Container>
        }
        { showSearchData &&
          !fetchingAllRoles &&
          !fetchingSearchResults &&
          (!roleSearchData || roleSearchData.length === 0) &&
          <Container
            id='next-role-select-grid-no-results'
            textAlign='center'>
            <Header as='h3' textAlign='center' color='grey'>
              <Header.Content>
                No search results
              </Header.Content>
            </Header>
          </Container>
        }
        { showSearchData &&
          totalSearchPages > 1 &&
          searchStart < totalSearchPages &&
          <Container
            id='next-role-select-grid-load-next-button'
            textAlign='center'>
            <Button size='large' onClick={() => this.loadNextSearch()}>
              More Results
            </Button>
          </Container>
        }
        { roles && (roles.length < rolesTotalCount) &&
          <Container
            id='next-role-select-grid-load-next-button'
            textAlign='center'>
            <Button size='large' onClick={() => this.loadNext()}>
              Load More
            </Button>
          </Container>
        }
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    fetchingAllRoles: state.requester.fetchingAllRoles,
    fetchingSearchResults: state.search.fetching,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(RoleSelectGrid);
