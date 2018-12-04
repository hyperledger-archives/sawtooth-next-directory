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
import ApprovalCard from '../../components/layouts/ApprovalCard';
import RolesList from '../../components/layouts/RolesList';


import './Packs.css';
import glyph from '../../images/header-glyph-pack.png';


/**
 *
 * @class         Packs
 * @description   Packs component
 *
 *
 */
export class Packs extends Component {

  static propTypes = {
    getRole: PropTypes.func,
  };


  componentDidMount () {
    const { getPack, packId } = this.props;
    packId && !this.pack && getPack(packId);
  }


  componentDidUpdate (prevProps) {
    const { getPack, packId } = this.props;
    if (prevProps.packId !== packId) !this.pack && getPack(packId);
  }


  render () {
    const { packId, packFromId } = this.props;

    this.pack = packFromId(packId);
    if (!this.pack) return null;

    return (
      <Grid id='next-requester-grid'>

        <Grid.Column
          id='next-requester-grid-track-column'
          width={11}>
          <TrackHeader
            glyph={glyph}
            waves
            title={this.pack.name}
            {...this.props}/>
          <div id='next-requester-packs-content'>
            { this.request &&
              this.request.status === 'OPEN' &&
              <ApprovalCard
                request={this.request}
                {...this.props}/>
            }
            <Container id='next-requester-packs-description-container'>
              <Label>Description</Label>
              <div id='next-requester-packs-description'>
                {this.pack.description}
              </div>
            </Container>
            <Label>Roles</Label>
            <RolesList activePack={this.pack} {...this.props}/>
          </div>
        </Grid.Column>

        <Grid.Column
          id='next-requester-grid-converse-column'
          width={5}>
          <Chat
            type={0}
            title={this.pack.name + ' Conversations'}
            activeRole={this.pack} {...this.props}/>
        </Grid.Column>

      </Grid>
    );
  }

}


const mapStateToProps = (state, ownProps) => {
  const { params } = ownProps.match;
  const { packs } = state.requester;

  return {
    packId: RequesterSelectors.idFromSlug(state, packs, params.id),
  };
}

const mapDispatchToProps = (dispatch) => {
  return {};
}


export default connect(mapStateToProps, mapDispatchToProps)(Packs);
