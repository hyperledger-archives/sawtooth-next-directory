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
import { Card, Grid } from 'semantic-ui-react';


import './Manage.css';
import TrackHeader from '../../../components/layouts/TrackHeader';


/**
 *
 * @class         Manage
 * @description   Manage component
 *
 */
class Manage extends Component {

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader inverted title='Manage' {...this.props}/>
          <div id='next-approver-manage-content'>
            <Grid stackable>
              <Grid.Row columns={3}>
                <Grid.Column>
                  <Card
                    fluid
                    as={Link}
                    to='manage/roles'
                    header='Roles'
                    description={`
                      Create a new role, modify an existing one,
                      or delete one.
                    `}/>
                </Grid.Column>
                <Grid.Column>
                  <Card
                    fluid
                    as={Link}
                    to='manage/packs'
                    header='Packs'
                    description={`
                      Create, modify, or delete an existing pack.
                    `}/>
                </Grid.Column>
                <Grid.Column>
                  <Card
                    fluid
                    as={Link}
                    to='manage/delegations'
                    header='Delegations'
                    description={`
                      Setup or modify a temporary or permanent delegation.
                    `}/>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row columns={3}>
                <Grid.Column>
                  <Card
                    fluid
                    as={Link}
                    to='manage/hierarchical'
                    header='Hierarchical'
                    description={`
                      Setup who can approve on your behalf.
                    `}/>
                </Grid.Column>
                <Grid.Column>
                  <Card
                    fluid
                    as={Link}
                    to='/manage/alerts'
                    header='Alerts'
                    description={`
                      Manage what you get alerts for and alert frequency.
                    `}/>
                </Grid.Column>
                <Grid.Column>
                </Grid.Column>
              </Grid.Row>
            </Grid>

            <Card.Group itemsPerRow={3}>
            </Card.Group>

          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default Manage;
