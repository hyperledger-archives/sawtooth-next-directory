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
import { Container, Grid, Header } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import { RequesterActions, RequesterSelectors } from 'state';


import Chat from 'components/chat/Chat';
import TrackHeader from 'components/layouts/TrackHeader';
import PackApproval from './PackApproval';
import PackApprovalList from './PackApprovalList';
import RolesList from './RolesList';
import MemberList from '../role/MemberList';


import './Pack.css';
import glyph from 'images/glyph-pack.png';


/**
 *
 * @class         Pack
 * @description   Pack component
 *
 *
 */
export class Pack extends Component {

  static propTypes = {
    getRole: PropTypes.func,
  };


  /**
   * Entry point to perform tasks required to render component.
   * Fetch pack if not loaded in client.
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
    const { packId } = this.props;
    if (prevProps.packId !== packId) this.init();
  }


  /**
   * Fetch pack if not loaded in client
   */
  init () {
    const { getPack, packId, packFromId, resetErrors } = this.props;
    resetErrors();
    packId && !packFromId(packId) && getPack(packId);
  }


  isOwner = () => {
    const { me } = this.props;
    return me && !!this.pack.owners.find(owner => owner === me.id);
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      error,
      packId,
      packFromId,
      proposalsFromIds,
      proposalIds } = this.props;

    if (error) {
      return (
        <div id='next-not-found-pack-container'>
          <Header as='h1'>
            <span role='img' aria-label=''>
              🤯
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

    this.pack = packFromId(packId);
    if (!this.pack) return null;
    this.proposals = proposalsFromIds(proposalIds);

    const showApprovalCard = this.proposals && this.proposals.length &&
      this.proposals.some(proposal => proposal.status !== 'CONFIRMED');

    return (
      <Grid id='next-requester-grid'>
        <Grid.Column
          id='next-requester-grid-track-column'
          width={12}>
          <TrackHeader
            inverted
            glyph={glyph}
            waves
            // subtitle={this.pack && utils.countLabel(
            //   this.pack.roles.length, 'role')
            // }
            title={this.pack.name}
            {...this.props}/>
          <div id='next-requester-packs-content'>
            { showApprovalCard &&
              <div>
                <PackApproval
                  proposals={this.proposals}
                  {...this.props}/>
                <PackApprovalList
                  proposals={this.proposals}
                  {...this.props}/>
              </div>
            }
            <Container
              className={showApprovalCard ? '' : 'next-margin-1'}
              id='next-requester-packs-description-container'>
              <div id='next-requester-packs-description'>
                <h5>
                  DESCRIPTION
                </h5>
                {this.pack.description || 'No description available.'}
              </div>
            </Container>
            <Container id='next-requester-packs-owner-list-container'>
              <h5>
                OWNERS
                {this.pack.owners.length === 0 && ' (0)'}
              </h5>
              <MemberList {...this.props}
                isOwner
                members={this.pack.owners}/>
            </Container>
            <Container id='next-requester-packs-roles-list-container'>
              <h5>
                ROLES
              </h5>
              <RolesList activePack={this.pack} {...this.props}/>
            </Container>
          </div>
        </Grid.Column>
        <Grid.Column
          id='next-requester-grid-converse-column'
          width={4}>
          <Chat
            type='REQUESTER'
            title={this.pack.name + ' Conversations'}
            activePack={this.pack} {...this.props}/>
        </Grid.Column>
      </Grid>
    );
  }

}


const mapStateToProps = (state, ownProps) => {
  const { id } = ownProps.match.params;

  return {
    error: state.requester.error,
    packId: id,
    proposalIds: RequesterSelectors.packProposalIds(state, id),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    resetErrors: () => dispatch(RequesterActions.resetErrors()),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(Pack);
