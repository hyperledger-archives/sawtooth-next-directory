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


import './Individuals.css';
import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import IndividualsNav from '../../components/nav/IndividualsNav';
import PeopleList from '../../components/layouts/proposals/PeopleList';
import RoleList from '../../components/layouts/proposals/RoleList';
import { selectRoles, selectUser } from './IndividualsHelper';


/**
 *
 * @class       Individuals
 * @description Individuals component
 *
 *
 */
class Individuals extends Component {

  state = {
    selectedRoles:      [],
    selectedUsers:      [],
    selectedProposals:  [],
    activeIndex:        0,
  };


  componentDidMount () {
    const { getOpenProposals, openProposals } = this.props;
    !openProposals && getOpenProposals();
  }


  setFlow = (index) => {
    this.setState({
      selectedRoles:      [],
      selectedUsers:      [],
      selectedProposals:  [],
      activeIndex:        index,
    });
  };


  /**
   *
   * Handle proposal change event
   *
   * When a proposal is checked or unchecked, select or deselect
   * the parent user, taking into account the currently
   * checked sibling proposals.
   *
   *
   */
  handleChange = (event, data) => {
    const {
      selectedRoles,
      selectedProposals,
      selectedUsers } = this.state;

    const { openProposalsByUser } = this.props;

    const { roles, proposals } = selectRoles(
      data.checked,
      data.proposals,
      selectedProposals,
      selectedRoles
    ).next().value;

    const { users } = selectUser(
      data.checked,
      data.user,
      openProposalsByUser[data.user]
        .filter(proposal => proposals
          .includes(proposal.id)),
      selectedUsers
    ).next().value;

    this.setState({
      selectedRoles:      roles,
      selectedProposals:  proposals,
      selectedUsers:      users,
    });
  };


  render () {
    const { openProposals } = this.props;
    const {
      activeIndex,
      selectedProposals,
      selectedRoles,
      selectedUsers } = this.state;

    return (
      <Grid id='next-approver-grid'>

        <Grid.Column id='next-approver-grid-track-column' width={11}>
          <TrackHeader
            title='Individual Requests'
            subtitle={openProposals && openProposals.length + ' pending'}
            {...this.props}/>
          <div id='next-approver-individuals-content'>
            <IndividualsNav
              activeIndex={activeIndex}
              setFlow={this.setFlow}/>
            { openProposals && openProposals.length !== 0 &&
              <div>
                { activeIndex === 0 &&
                  <RoleList {...this.props}/>
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
              <Header as='h3' textAlign='center'>
                <Header.Content>No pending items</Header.Content>
              </Header>
            }
          </div>
        </Grid.Column>

        <Grid.Column
          id='next-approver-grid-converse-column'
          width={5}>
          <Chat
            type={1}
            selectedProposals={selectedProposals}
            selectedRoles={selectedRoles}
            selectedUsers={selectedUsers}
            handleChange={this.handleChange}
            {...this.props}/>
        </Grid.Column>

      </Grid>
    );
  }

}


const mapStateToProps = (state) => {
  return {};
}

const mapDispatchToProps = (dispatch) => {
  return {};
}

export default connect(mapStateToProps, mapDispatchToProps)(Individuals);


Individuals.proptypes = {
  getOpenProposals: PropTypes.func
};
