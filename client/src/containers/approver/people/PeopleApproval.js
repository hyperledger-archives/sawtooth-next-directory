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
import { Grid, Header } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import Chat from 'components/chat/Chat';
import TrackHeader from 'components/layouts/TrackHeader';
import PeopleApprovalNav from 'components/nav/IndividualsNav';
import PeopleList from '../PeopleList';
import RoleList from '../RoleList';
import { syncAll } from '../IndividualsHelper';


import './PeopleApproval.css';
import glyph from 'images/header-glyph-individual.png';
import * as theme from 'services/Theme';


/**
 *
 * @class         PeopleApproval
 * @description   Individual requests component
 *
 */
class PeopleApproval extends Component {

  static propTypes = {
    getOpenProposals: PropTypes.func,
  };


  themes = ['dark', 'minimal'];


  state = {
    selectedRoles:      [],
    selectedUsers:      [],
    selectedProposals:  [],
    activeIndex:        0,
  };


  /**
   * Entry point to perform tasks required to render
   * component. On load, get open proposals.
   */
  componentDidMount () {
    const { getOpenProposals, getUser, onBehalfOf } = this.props;
    getOpenProposals(onBehalfOf);
    getUser(onBehalfOf);
    theme.apply(this.themes);
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Switch between Roles and People views
   * @param {number} activeIndex Current screen index
   */
  setFlow = (activeIndex) => {
    this.setState({ activeIndex });
  };


  reset = () => {
    this.setState({
      selectedRoles:      [],
      selectedUsers:      [],
      selectedProposals:  [],
    });
  }


  /**
   * Handle proposal change event
   * When a proposal is checked or unchecked, select or deselect
   * the parent user, taking into account the currently
   * checked sibling proposals.
   * @param {object} event Event passed on change
   * @param {object} data  Attributes passed on change
   */
  handleChange = (event, data) => {
    const sync = syncAll.call(
      this,
      data.checked,
      data.role,
      data.proposal,
      data.user,
    );

    const { roles, proposals } = sync.next().value;
    const { users } = sync.next().value;

    this.setState({
      selectedRoles:      roles,
      selectedProposals:  proposals,
      selectedUsers:      users,
    });
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { openProposals, onBehalfOf, users, userFromId } = this.props;
    const {
      activeIndex,
      selectedProposals,
      selectedRoles,
      selectedUsers } = this.state;

    const user = selectedUsers && userFromId(selectedUsers[0]);
    const title = user && user.name;
    const subtitle = `${selectedProposals.length}
      ${selectedProposals.length > 1 ? 'requests' : 'request'}
      selected`;

    const foo = users && users.find(user => user.id === onBehalfOf);
    const bar = `Pending Approvals (${foo && foo.name})`;

    return (
      <Grid id='next-approver-grid'>

        <Grid.Column id='next-approver-grid-track-column' width={12}>
          <TrackHeader
            inverted
            breadcrumb={[
              {name: 'People', slug: '/approval/people'},
              {
                name: 'Direct Report Approvals',
                slug: `/approval/people/${onBehalfOf}/pending`,
              },
            ]}
            glyph={glyph}
            title={foo && bar}
            {...this.props}/>
          <div id='next-approver-people-approval-content'>
            <PeopleApprovalNav
              activeIndex={activeIndex}
              setFlow={this.setFlow}/>
            <h3 id='next-approver-people-pending'>
              {openProposals && openProposals.length + ' pending'}
            </h3>
            { openProposals && openProposals.length !== 0 &&
              <div>
                { activeIndex === 0 &&
                  <RoleList
                    selectedProposals={selectedProposals}
                    selectedRoles={selectedRoles}
                    handleChange={this.handleChange}
                    {...this.props}/>
                }
                { activeIndex === 1 &&
                  <PeopleList
                    selectedProposals={selectedProposals}
                    selectedUsers={selectedUsers}
                    handleChange={this.handleChange}
                    {...this.props}/>
                }
              </div>
            }
            { openProposals && openProposals.length === 0 &&
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  Your direct report has no pending approvals
                </Header.Content>
              </Header>
            }
          </div>
        </Grid.Column>

        <Grid.Column
          id='next-approver-grid-converse-column'
          width={4}>
          <Chat
            type='APPROVER'
            formDisabled
            title={title}
            subtitle={subtitle}
            groupBy={activeIndex}
            disabled={!openProposals ||
              (openProposals && openProposals.length === 0)}
            selectedProposals={selectedProposals}
            selectedRoles={selectedRoles}
            selectedUsers={selectedUsers}
            handleChange={this.handleChange}
            reset={this.reset}
            {...this.props}/>
        </Grid.Column>

      </Grid>
    );
  }

}


const mapStateToProps = (state, ownProps) => {
  const { id } = ownProps.match.params;
  const { onBehalfOf } = ownProps;

  return {
    onBehalfOf: onBehalfOf || id,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(PeopleApproval);

