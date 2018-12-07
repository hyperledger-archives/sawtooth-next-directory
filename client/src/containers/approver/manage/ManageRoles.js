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
import { Link } from 'react-router-dom';
import { Button, Grid } from 'semantic-ui-react';


import './ManageRoles.css';
import TrackHeader from '../../../components/layouts/TrackHeader';


/**
 *
 * @class         ManageRoles
 * @description   Manage component
 *
 */
class ManageRoles extends Component {

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { me } = this.props;
    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            title='Roles'
            button={() =>
              <Button as={Link} to='roles/create'>Create New Role</Button>}
            {...this.props}/>
          <div id='next-approver-manage-content'>
            { me && me.administratorOf.length > 0 ?
              <h1>Roles you created:</h1> :
              <h1>You haven&apos;t created any roles</h1>
            }
            { me && me.administratorOf.map(roleId => (
              <span key={roleId}>{roleId}</span>
            ))
            }
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default ManageRoles;
