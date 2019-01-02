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


import { RequesterSelectors } from 'state';
import Chat from 'components/chat/Chat';
import TrackHeader from 'components/layouts/TrackHeader';
import PackApproval from './PackApproval';
import PackApprovalList from './PackApprovalList';
import RolesList from './RolesList';


import './Pack.css';
import glyph from 'images/header-glyph-pack.png';
import * as utils from 'services/Utils';


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


  init = () => {
    const { getPack, packId, packFromId } = this.props;
    packId && !packFromId(packId) && getPack(packId);
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      packId,
      packFromId,
      proposalsFromIds,
      proposalIds } = this.props;

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
            subtitle={this.pack && utils.countLabel(
              this.pack.roles.length, 'role')
            }
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
    packId: id,
    proposalIds: RequesterSelectors.packProposalIds(state, id),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(Pack);
