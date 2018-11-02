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


import Chat from '../../components/chat/Chat';
import RolesList from '../../components/layouts/RolesList';
import TrackHeader from '../../components/layouts/TrackHeader';


import './Roles.css';


/**
 *
 * @class Roles
 * Roles component
 *
 */
class Roles extends Component {
  render() {
    return (
      <Grid id="next-approver-grid" celled="internally">

        <Grid.Column
          id="next-approver-grid-track-column"
          width={10}
        >
          <TrackHeader title="Roles" {...this.props} />
          <RolesList {...this.props} />
        </Grid.Column>
        <Grid.Column
          id="next-approver-grid-converse-column"
          width={6}
        >
          <Chat {...this.props} />
        </Grid.Column>

      </Grid>
    );
  }
}


const mapStateToProps = state => ({});

const mapDispatchToProps = dispatch => ({});

export default connect(mapStateToProps, mapDispatchToProps)(Roles);
