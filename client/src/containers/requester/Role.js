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
   * Entry point to perform tasks required to render component.
   * Fetch role if not loaded in client.
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { roleId } = this.props;
    if (prevProps.roleId !== roleId) this.init();
  }


  init = () => {
    const { getRole, roleId, roleFromId } = this.props;
    roleId && !roleFromId(roleId) && getRole(roleId);
  }


  isOwner = () => {
    const { me } = this.props;
    return me && !!this.role.owners.find(owner => owner === me.id);
  };


  subtitle = () => {
    const membersCount = [...this.role.members, ...this.role.owners].length;
    return `${membersCount} ${membersCount > 1 || membersCount === 0 ?
      'members' :
      'member'}`;
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      proposalFromId,
      proposalId,
      roleId,
      roleFromId } = this.props;

    this.role = roleFromId(roleId);
    if (!this.role) return null;
    this.proposal = proposalFromId(proposalId);

    return (
      <Grid id='next-requester-grid'>

        <Grid.Column
          id='next-requester-grid-track-column'
          width={12}>
          <TrackHeader
            inverted
            glyph={glyph}
            waves
            title={this.role.name}
            subtitle={this.subtitle()}
            {...this.props}/>
          <div id='next-requester-roles-content'>
            { this.proposal &&
              this.proposal.status !== 'CONFIRMED' &&
              <RoleApproval
                proposal={this.proposal}
                {...this.props}/>
            }
            <Container
              className={!this.proposal ? 'next-margin-1' : ''}
              id='next-requester-roles-description-container'>
              <div id='next-requester-roles-description'>
                <h5>DESCRIPTION</h5>
                {this.role.description || 'No description available.'}
              </div>
            </Container>
            <Container id='next-requester-roles-member-list-container'>
              <h5>MEMBERS</h5>
              <MemberList {...this.props}
                members={this.role.members}
                owners={this.role.owners}/>
            </Container>
          </div>
        </Grid.Column>

        <Grid.Column
          id='next-requester-grid-converse-column'
          width={4}>
          <Chat
            type='REQUESTER'
            disabled={this.isOwner()}
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
    roleId: id,
    proposalId: RequesterSelectors.proposalIdFromSlug(state, roles, id, 'role'),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(Role);
