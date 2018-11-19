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
import MemberList from '../../components/layouts/MemberList';


import './Recommended.css';


/**
 *
 * @class Recommended
 * *Recommended* component
 *
 */
export class Recommended extends Component {

  componentDidMount () {
    const { getRole, roleId } = this.props;
    roleId && !this.role && getRole(roleId);
  }


  /**
   *
   * Switch pack on ID change
   *
   *
   */
  componentWillReceiveProps (newProps) {
    const { getRole, roleId } = this.props;

    if (newProps.roleId !== roleId) {
      !this.role && getRole(newProps.roleId);
    }
  }


  render () {
    const { roleId, roleFromId, me } = this.props;

    this.role = roleFromId(roleId);

    if (!this.role) return null;

    const membersCount = [...this.role.members, ...this.role.owners].length;
    const subtitle = `${membersCount} ${membersCount > 1 ? 'members' : 'member'}`;
    const isOwner = me && !!this.role.owners.find(owner => owner === me.id);

    return (
      <Grid id='next-requester-grid'>

        {/* Left pane */}
        <Grid.Column
          id='next-requester-grid-track-column'
          width={11}>
          <TrackHeader
            roleImage
            waves
            title={this.role.name}
            subtitle={subtitle}
            {...this.props}/>
          <div id='next-requester-recommended-content'>
            <Container id='next-requester-recommended-description'>
              Lorem ipsum dolor sit amet.
            </Container>
            <MemberList {...this.props}
              members={this.role.members}
              owners={this.role.owners}/>
          </div>
        </Grid.Column>

        {/* Right pane */}
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


Recommended.proptypes = {
  getRole: PropTypes.func
};


const mapStateToProps = (state, ownProps) => {
  const { params } = ownProps.match;
  const { roles } = state.requester;

  return {
    roleId: RequesterSelectors.idFromSlug(state, roles, params.id)
  };
}

const mapDispatchToProps = (dispatch) => {
  return {};
}


export default connect(mapStateToProps, mapDispatchToProps)(Recommended);
