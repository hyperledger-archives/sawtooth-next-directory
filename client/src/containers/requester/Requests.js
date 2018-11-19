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
import { Container, Grid } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import { RequesterSelectors } from '../../redux/RequesterRedux';


import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import ApprovalCard from '../../components/layouts/ApprovalCard';
import MemberList from '../../components/layouts/MemberList';


import './Requests.css';


/**
 *
 * @class Requests
 * *Your Requests* component
 *
 */
export class Requests extends Component {

  componentDidMount () {
    const { getRole, getProposal, roleId, proposalId } = this.props;

    roleId && !this.role && getRole(roleId);
    proposalId && !this.request && getProposal(proposalId);
  }


  /**
   *
   * Switch pack on ID change
   * TODO: Fix double request
   *
   *
   */
  componentWillReceiveProps (newProps) {
    const { getRole, getProposal, roleId, proposalId } = this.props;

    if (newProps.roleId !== roleId) {
      getRole(newProps.roleId);
    }

    if (newProps.proposalId !== proposalId) {
      getProposal(newProps.proposalId);
    }
  }


  render () {
    const {
      proposalId,
      proposalFromId,
      roleId,
      roleFromId } = this.props;

    this.role = roleFromId(roleId);
    this.request = proposalFromId(proposalId);
    if (!this.role || !this.request) return null;


    return (
      <Grid id='next-requester-grid'>

        <Grid.Column
          id='next-requester-grid-track-column'
          width={11}>

          <TrackHeader
            roleImage
            waves
            title={this.role && this.role.name}
            {...this.props}/>

          <div id='next-requester-requests-content'>
            <ApprovalCard request={this.request} {...this.props}/>
            <Container id='next-requester-requests-description'>
              Lorem ipsum dolor sit amet.
            </Container>
            <MemberList {...this.props}
              members={this.role && this.role.members}
              owners={this.role && this.role.owners}/>
          </div>

        </Grid.Column>
        <Grid.Column
          id='next-requester-grid-converse-column'
          width={5}>
          <Chat disabled {...this.props}/>
        </Grid.Column>

      </Grid>
    );
  }

}



const mapStateToProps = (state, ownProps) => {
  const { id } = ownProps.match.params;
  const { roles } = state.requester;

  return {
    roleId: RequesterSelectors.idFromSlug(state, roles, id),
    proposalId: RequesterSelectors.idFromSlug(
      state,
      roles,
      id,
      'proposal_id'
    )
  };
}

const mapDispatchToProps = (dispatch) => {
  return {};
}

export default connect(mapStateToProps, mapDispatchToProps)(Requests);


Requests.proptypes = {
  getRole: PropTypes.func,
  getProposal: PropTypes.func,
};
