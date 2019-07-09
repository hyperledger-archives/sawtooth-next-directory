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
import { Button, Container, Grid, Header } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import { RequesterActions, RequesterSelectors } from 'state';


import Chat from 'components/chat/Chat';
import TrackHeader from 'components/layouts/TrackHeader';
import RoleApproval from './RoleApproval';
import MemberList from './MemberList';


import './Role.css';
import glyph from 'images/glyph-role.png';


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
    const { getRole, me, roleId } = this.props;

    if (prevProps.roleId !== roleId) this.init();

    if (me && me.memberOf && prevProps.me &&
        me.memberOf.length > prevProps.me.memberOf.length)
      getRole(roleId);
  }


  /**
   * Fetch role if not loaded in client
   */
  init () {
    const { getRole, resetErrors, roleId, roleFromId } = this.props;
    resetErrors();
    roleId && !roleFromId(roleId) && getRole(roleId);
  }


  /**
   * Determine if user owns current role
   * @returns {boolean}
   */
  isOwner = () => {
    const { me } = this.props;
    return me && !!this.role.owners.find(owner => owner === me.id);
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      error,
      manualExpire,
      proposalFromId,
      proposalId,
      roleId,
      roleFromId } = this.props;

    if (error && error.code === 404) {
      return (
        <div id='next-not-found-role-container'>
          <Header as='h1'>
            <span role='img' aria-label=''>
              😕
            </span>
            <Header.Subheader>
              {error.message}
              <div>
                {'(ERR CODE: '}
                {error.code}
                {')'}
              </div>
            </Header.Subheader>
          </Header>
        </div>
      );
    }

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
            // subtitle={
            //   this.role && utils.countLabel(
            //     this.role.members.length, 'member'
            //   )
            // }
            {...this.props}/>
          <div id='next-requester-roles-content'>
            { this.proposal &&
              this.proposal.status !== 'CONFIRMED' &&
              <RoleApproval
                proposal={this.proposal}
                {...this.props}/>
            }
            <Container
              className={this.proposal && this.proposal.status !== 'CONFIRMED' ?
                '' : 'next-margin-1'}
              id='next-requester-roles-description-container'>
              <div id='next-requester-roles-description'>
                <h5>
                  DESCRIPTION
                </h5>
                {this.role.description || 'No description available.'}
              </div>
            </Container>
            <Container id='next-requester-roles-owner-list-container'>
              <h5>
                OWNERS
                {this.role.owners.length === 0 && ' (0)'}
              </h5>
              <MemberList {...this.props}
                isOwner
                members={this.role.owners}/>
            </Container>
            <Container id='next-requester-roles-member-list-container'>
              <h5>
                MEMBERS
                {this.role.members.length === 0 && ' (0)'}
              </h5>
              <MemberList {...this.props}
                members={this.role.members}/>
            </Container>
          </div>
          <div id='next-requester-roles-manual-expire'>
            <Button
              basic
              size='tiny'
              icon='circle'
              onClick={() => manualExpire(roleId)}/>
          </div>
        </Grid.Column>
        <Grid.Column
          id='next-requester-grid-converse-column'
          width={4}>
          <Chat
            type='REQUESTER'
            title={this.role.name + ' Conversations'}
            activeRole={this.role} {...this.props}/>
        </Grid.Column>
      </Grid>
    );
  }

}


const mapStateToProps = (state, ownProps) => {
  const { id } = ownProps.match.params;
  return {
    error: state.requester.error,
    roleId: id,
    proposalId: RequesterSelectors.roleProposalId(state, id),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    resetErrors: () => dispatch(RequesterActions.resetErrors()),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(Role);
