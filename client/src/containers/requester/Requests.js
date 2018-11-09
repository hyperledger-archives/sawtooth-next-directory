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

    if (roleId && proposalId) {
      getRole(roleId);
      getProposal(proposalId);
    }
  }


  /**
   *
   * Switch pack on ID change
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
    const { activeRole } = this.props;

    return (
      <Grid id='next-requester-grid'>

        <Grid.Column
          id='next-requester-grid-track-column'
          width={10}>

          <TrackHeader
            roleImage
            waves
            title={activeRole && activeRole.name}
            {...this.props}/>

          <div id='next-requester-requests-content'>
            <ApprovalCard {...this.props}/>
            <Container id='next-requester-description'>
              Lorem ipsum dolor sit amet.
            </Container>
            <MemberList {...this.props}
              members={activeRole && activeRole.members}
              owners={activeRole && activeRole.owners}/>
          </div>

        </Grid.Column>
        <Grid.Column
          id='next-requester-grid-converse-column'
          width={6}>
          <Chat {...this.props}/>
        </Grid.Column>

      </Grid>
    );
  }

}



const mapStateToProps = (state, ownProps) => {
  const { id } = ownProps.match.params;
  const { requests } = state.user;

  return {
    roleId: RequesterSelectors.idFromSlug(requests, id),
    proposalId: RequesterSelectors.idFromSlug(requests, id, 'proposal_id')
  };
}

const mapDispatchToProps = (dispatch) => {
  return {};
}

export default connect(mapStateToProps, mapDispatchToProps)(Requests);


Requests.proptypes = {
  getRole: PropTypes.func,
  getProposal: PropTypes.func,
  activeRole: PropTypes.arrayOf(PropTypes.shape(
    {
      name: PropTypes.string
    }
  ))
};
