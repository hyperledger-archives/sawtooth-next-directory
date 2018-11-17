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
import { Grid } from 'semantic-ui-react';


import ApproverActions from '../../redux/ApproverRedux';
import { UserSelectors } from '../../redux/UserRedux';


import './Manage.css';
import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import CreateModal from '../../components/modals/manage/Create';


/**
 *
 * @class Manage
 * Manage component
 *
 */
class Manage extends Component {

  createRole = (name) => {
    const { createRole, userId } = this.props;

    createRole({
      name:           name,
      owners:         [userId],
      administrators: [userId]
    });
  }

  render () {
    return (
      <Grid id='next-approver-grid'>

        <Grid.Column
          id='next-approver-grid-track-column'
          width={11}>
          <TrackHeader title='Manage' {...this.props}/>
          <div id='next-approver-manage-content'>
            <CreateModal submit={this.createRole}/>
          </div>
        </Grid.Column>
        <Grid.Column
          id='next-approver-grid-converse-column'
          width={5}>
          <Chat {...this.props}/>
        </Grid.Column>

      </Grid>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    error:  state.approver.error,
    userId: UserSelectors.id(state),
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    createRole: (payload) => dispatch(ApproverActions.createRoleRequest(payload)),
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(Manage);
