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
 * @class         ApprovalCard
 * @description   This card formats the display of an open request's
 *                current approval status. It displays who owns the resource,
 *                when the request was opened, and approval status
 *
 */
class ApprovalCard extends Component {

  static propTypes = {
    getUser:            PropTypes.func,
    request:            PropTypes.object,
    users:              PropTypes.array,
  }


  /**
   * Entry point to perform tasks required to render component.
   * The card displays conditionally, requiring 'request' to be
   * passed as a prop.
   */
  componentDidMount () {
    const { request, getUser, users } = this.props;
    if (!request) return;

    request.appprovers &&
    request.appprovers.map((userId) => {
      return users && users.find((user) => user.id === userId) ?
        undefined :
        getUser(userId)
    })
  }


  /**
   * Display the open request's approvers
   * @param {string} userId Approver's user ID
   * @returns {JSX}
   */
  renderApprover (userId) {
    const { users } = this.props;

    if (!users) return null;
    const user = users.find((user) => user.id === userId);
    return (
      <div id='next-approval-approver' key={userId}>
        {user && user.name}
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { request } = this.props;
    if (!request) return null;

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
                { request.approvers &&
                  request.approvers.map((approver) => (
                    this.renderApprover(approver)
                  )) }
              </Grid.Column>
            </Grid>
          </Card.Content>
        </Card>
      </div>
    );
  }

}


export default ApprovalCard;
