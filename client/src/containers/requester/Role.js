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
import { Container, Grid, Label } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import { RequesterSelectors } from '../../redux/RequesterRedux';


import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import RoleApproval from './RoleApproval';
import MemberList from '../../components/layouts/MemberList';


import './Role.css';
import glyph from '../../images/header-glyph-role.png';


/**
 *
 * @class         Role
 * @description   Role component
 *
 *
 */
export class Role extends Component {

  static propTypes = {
    getProposal: PropTypes.func,
    getRole: PropTypes.func,
  };


  /**
   * Entry point to perform tasks required to render
   * component. Get detailed info for current role and if the
   * role is in approval state, get proposal info.
   */
  componentDidMount () {
    const { getProposal, getRole, proposalId, roleId } = this.props;

    // TODO: Only get if not loaded
    roleId && !this.role && getRole(roleId);
    proposalId && !this.request && getProposal(proposalId);
  }


  /**
   * Called whenever Redux state changes. If role or proposal state
   * changes, update info.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { getProposal, getRole, proposalId, roleId } = this.props;

    // TODO: Only get if not loaded
    if (prevProps.roleId !== roleId) !this.role && getRole(roleId);
    if (prevProps.proposalId !== proposalId) {
      proposalId &&
      !this.request && getProposal(proposalId);
    }
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      me,
      proposalFromId,
      proposalId,
      roleId,
      roleFromId } = this.props;

    this.role = roleFromId(roleId);
    if (!this.role) return null;
    this.request = proposalFromId(proposalId);

    const membersCount = [...this.role.members, ...this.role.owners].length;
    const isOwner = me && !!this.role.owners.find(owner => owner === me.id);
    const subtitle = `${membersCount} ${membersCount > 1 ?
      'members' :
      'member'}`;

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
              <RoleApproval
                request={this.request}
                {...this.props}/>
            }
            <Container id='next-requester-roles-description-container'>
              <Label>Roles</Label>
              <div id='next-requester-roles-description'>
                Lorem ipsum dolor sit amet.
              </div>
            </Container>
            <Label>Members</Label>
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
    ),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(Role);
