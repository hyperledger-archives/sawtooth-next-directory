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
import {
  Button,
  Container,
  Header,
  Placeholder,
  Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import Avatar from 'components/layouts/Avatar';
import './OrganizationList.css';


/**
 *
 * @class         OrganizationList
 * @description   Component encapsulating the member list
 *
 *
 */
class OrganizationList extends Component {

  static propTypes = {
    fetchingPeople:     PropTypes.bool,
    getPeople:          PropTypes.func,
    getUsers:           PropTypes.func,
    handleUserSelect:   PropTypes.func,
    id:                 PropTypes.string,
    members:            PropTypes.array,
    owners:             PropTypes.array,
    users:              PropTypes.array,
  };


  state = {
    start: 0,
    limit: 25,
  };


  /**
   * Entry point to perform tasks required to render component.
   * Get first page of all users.
   */
  componentDidMount   () {
    const { handleUserSelect, id } = this.props;
    handleUserSelect(id);
    this.loadNext(0);
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {

  }


  /**
   * Load next set of data
   * @param {number} start Loading start index
   */
  loadNext = (start) => {
    const { getPeople, people } = this.props;
    const { limit } = this.state;
    if (start === undefined || start === null)
      start = this.state.start;

    if (people && people.length >= limit)
      start = people.length;

    getPeople(start, limit);
    this.setState({ start: start + limit });
  }


  /**
   * Render placeholder graphics
   * @returns {JSX}
   */
  renderPlaceholder = () => {
    return Array(4).fill(0).map((item, index) => (
      <div key={index} className='next-member-list-placeholder'>
        <Placeholder inverted fluid>
          <Placeholder.Header image>
            <Placeholder.Line length='full'/>
            <Placeholder.Line length='long'/>
          </Placeholder.Header>
        </Placeholder>
      </div>
    ));
  }


  /**
   * Render segment containing person info
   * @param {object} person Person in organization to render
   * @returns {JSX}
   */
  renderPersonSegment (person) {
    const { handleUserSelect, id } = this.props;
    return (
      <Segment
        onClick={() => handleUserSelect(person.id)}
        className='no-padding minimal'>
        <Header as='h3' className='next-member-list-person-info'>
          <div>
            <Avatar userId={person.id} size='medium' {...this.props}/>
          </div>
          <div>
            {person.name}
            {person.id === id && ' (You)'}
            {person.email &&
            <Header.Subheader>
              {person.email}
            </Header.Subheader>
            }
          </div>
        </Header>
        { person.memberOf &&
          <div className='next-member-list-person-role-count'>
            <h1>
              {person.memberOf.length}
            </h1>
            <span>
              { person.memberOf.length > 1 ||
                person.memberOf.length === 0 ? 'Roles' : 'Role'
              }
            </span>
          </div>
        }
      </Segment>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      fetchingPeople,
      me,
      people,
      peopleTotalCount } = this.props;

    return (
      <div id='next-approver-people-list-container'>
        { me && this.renderPersonSegment(me) }
        { people && people.map((person, index) =>
          <div className='next-approver-people-list-item' key={index}>
            {this.renderPersonSegment(person)}
          </div>
        )}
        {fetchingPeople && this.renderPlaceholder()}
        { people && people.length < peopleTotalCount &&
          <Container
            id='next-people-load-next-button'
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


export default OrganizationList;
