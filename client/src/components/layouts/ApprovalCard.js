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
import { Card, Grid } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './ApprovalCard.css';


/**
 * 
 * @class ApprovalCard
 * Component encapsulating the approval card
 * 
 */
export default class ApprovalCard extends Component {
 

  render () {
    return (
      <div id=''>
        <Card>
          <Card.Header>
            <span role='img' aria-label=''>🙇</span>
            <div>Awaiting approval</div>
          </Card.Header>
          <Card.Content extra>
            <Grid columns={3} padded='vertically'>
              <Grid.Column>
                Request ID
              </Grid.Column>
              <Grid.Column>
                Request Date
              </Grid.Column>
              <Grid.Column>
                Approver
              </Grid.Column>
            </Grid>
          </Card.Content>
        </Card>
      </div>
    );
  }

}


ApprovalCard.proptypes = {
  activePack: PropTypes.arrayOf(PropTypes.shape(
    {
      description: PropTypes.string,
      roles: PropTypes.arrayOf(PropTypes.shape(
        {
          name: PropTypes.string
        }  
      ))
    }
  ))
};
