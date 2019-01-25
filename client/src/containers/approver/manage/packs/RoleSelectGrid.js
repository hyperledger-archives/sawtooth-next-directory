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
import RoleSelectGridNav from 'components/nav/RoleSelectGridNav';


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
    start: 0,
    limit: 25,
  };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    this.loadNext(0);
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
          {role.name}
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
      roles,
      rolesTotalCount } = this.props;
    const { limit } = this.state;
    return (
      <div>
        <RoleSelectGridNav/>
        <Grid centered columns={3} id='next-role-select-grid'>
          { roles && (roles.length >= limit || !fetchingAllRoles) &&
            roles.map(role => (
              <Grid.Column key={role.id} width={5}>
                {this.renderRoleToggle(role)}
              </Grid.Column>
            ))}
          { fetchingAllRoles &&
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
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(RoleSelectGrid);
