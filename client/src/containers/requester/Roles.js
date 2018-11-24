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


import './Roles.css';
import glyph from '../../images/header-glyph-role.png';


/**
 *
 * @class         Roles
 * @description   Roles component
 *
 *
 */
export class Roles extends Component {

  static propTypes = {
    getProposal: PropTypes.func,
    getRole: PropTypes.func,
  };


  componentDidMount () {
    const { getProposal, getRole, proposalId, roleId } = this.props;
    roleId && !this.role && getRole(roleId);
    proposalId && !this.request && getProposal(proposalId);
  }


  /**
   *
   * Switch pack on ID change
   *
   *
   */
  componentWillReceiveProps (newProps) {
    const { getProposal, getRole, proposalId, roleId } = this.props;

    if (newProps.roleId !== roleId) {
      !this.role && getRole(newProps.roleId);
    }

    if (newProps.proposalId !== proposalId) {
      proposalId && !this.request && getProposal(newProps.proposalId);
    }
  }


  render () {
    const {
      me,
      proposalFromId,
      proposalId,
      roleId,
      roleFromId } = this.props;

    this.role = roleFromId(roleId);
    this.request = proposalFromId(proposalId);

    if (!this.role) return null;

    const membersCount = [...this.role.members, ...this.role.owners].length;
    const subtitle = `${membersCount} ${membersCount > 1 ? 'members' : 'member'}`;
    const isOwner = me && !!this.role.owners.find(owner => owner === me.id);

    return (
      <Grid id='next-requester-grid'>

        <Grid.Column
          id='next-requester-grid-track-column'
          width={11}>
          <TrackHeader
            glyph={glyph}
            waves
            title={this.role.name}
            subtitle={subtitle}
            {...this.props}/>
          <div id='next-requester-roles-content'>
            { this.request &&
              this.request.status === 'OPEN' &&
              <ApprovalCard
                request={this.request}
                {...this.props}/>
            }
            <Container id='next-requester-roles-description'>
              Lorem ipsum dolor sit amet.
            </Container>
            <MemberList {...this.props}
              members={this.role.members}
              owners={this.role.owners}/>
          </div>
        </Grid.Column>

        <Grid.Column
          id='next-requester-grid-converse-column'
          width={5}>
          <Chat
            type={0}
            disabled={isOwner}
            title={this.role.name + ' Conversations'}
            activeRole={this.role} {...this.props}/>
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


export default connect(mapStateToProps, mapDispatchToProps)(Roles);
