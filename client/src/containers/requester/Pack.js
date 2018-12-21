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
import PackApproval from './PackApproval';
import PackApprovalList from './PackApprovalList';
import RolesList from '../../components/layouts/RolesList';


import './Pack.css';
import glyph from '../../images/header-glyph-pack.png';


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

    return (
      <Grid id='next-requester-grid'>
        <Grid.Column
          id='next-requester-grid-track-column'
          width={12}>
          <TrackHeader
            inverted
            glyph={glyph}
            waves
            title={this.pack.name}
            {...this.props}/>
          <div id='next-requester-packs-content'>
            { this.proposals && this.proposals.length > 0 &&
              <div>
                <PackApproval
                  proposals={this.proposals}
                  {...this.props}/>
                <PackApprovalList
                  proposals={this.proposals}
                  {...this.props}/>
              </div>
            }
            <Container id='next-requester-packs-description-container'>
              <div id='next-requester-packs-description'>
                {this.pack.description}
              </div>
            </Container>
            <RolesList activePack={this.pack} {...this.props}/>
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
  const { packs } = state.requester;

  return {
    packId: id,
    proposalIds: RequesterSelectors.proposalIdFromSlug(
      state, packs, id, 'pack'
    ),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(Pack);
