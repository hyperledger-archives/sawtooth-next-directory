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

  /**
   *
   * Hydrate data
   *
   */
  componentDidMount () {
    const { activeProposal, getUser, users } = this.props;

    if (!activeProposal) {
      return;
    }

    activeProposal.appprovers &&
    activeProposal.appprovers.map((userId) => {
      return users && users.find((user) => user.id === userId) ?
        undefined :
        getUser(userId)
    })
  }


  renderApprover (userId, index) {
    const { users } = this.props;

    if (!users) return null;
    const user = users.find((user) => user.id === userId);
    return (<div key={index}>{user.name}</div>);
  }


  render () {
    const { activeProposal } = this.props;

    if (!activeProposal) {
      return null;
    }

    return (
      <div id='next-approval-container'>
        <Card fluid>
          <Card.Header id='next-approval-status'>
            <span id='next-approval-status-emoji' role='img' aria-label=''>
              🙇
            </span>
            <h3>Awaiting approval</h3>
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
                Approver(s)
                { activeProposal.approvers &&
                  activeProposal.approvers.map((approver, index) => (
                  this.renderApprover(approver, index)
                )) }
              </Grid.Column>
            </Grid>
          </Card.Content>
        </Card>
      </div>
    );
  }

}


ApprovalCard.proptypes = {
  activeRole: PropTypes.arrayOf(PropTypes.shape(
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
