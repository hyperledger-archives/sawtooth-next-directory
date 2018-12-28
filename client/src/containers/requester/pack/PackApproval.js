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
import { Card, Grid, Label } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './PackApproval.css';
import * as utils from 'services/Utils';


/**
 *
 * @class         PackApproval
 * @description   This layout formats the display of an open request's
 *                current approval status. It displays who owns the resource,
 *                when the request was opened, and approval status.
 *
 */
class PackApproval extends Component {

  static propTypes = {
    getUser:            PropTypes.func,
    proposals:          PropTypes.array,
    users:              PropTypes.array,
  }


  state = { approved: 0, pending: 0, rejected: 0 };


  /**
   * Entry point to perform tasks required to render component.
   * The card displays conditionally, requiring 'proposals' to be
   * passed as a prop.
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes. If proposals prop is changed,
   * update info.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { proposals } = this.props;
    if (!utils.arraysEqual(prevProps.proposals, proposals)) this.init();
  }


  /**
   * On load, get users not loaded in and tabulate status counts
   */
  init () {
    const { proposals, getUser, users } = this.props;
    if (!proposals) return;

    let pending = 0;
    let approved = 0;
    let rejected = 0;

    proposals.forEach(proposal => {
      proposal.appprovers &&
      proposal.appprovers.map((userId) => {
        return users && users.find((user) => user.id === userId) ?
          undefined :
          getUser(userId);
      });

      if (proposal.status === 'OPEN') pending += 1;
      if (proposal.status === 'CONFIRMED') approved += 1;
      if (proposal.status === 'REJECTED') rejected += 1;
    });

    this.setState({ approved, pending, rejected });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { proposals } = this.props;
    const { approved, pending, rejected } = this.state;
    if (!proposals) return null;

    return (
      <div id='next-pack-approval-container'>
        <Card fluid>
          <Card.Header id='next-pack-approval-status'>
            <Grid columns={4} padded='vertically'>
              <Grid.Column id='next-pack-approval-request-info'>
                <div>Request ID</div>
                <div>Request Date</div>
              </Grid.Column>
              <Grid.Column>
                <h1>{approved}</h1>
                <Label circular color='grey'>
                  <span
                    className='next-pack-approval-status-emoji'
                    role='img'
                    aria-label=''>
                    👍
                  </span>
                  Approved
                </Label>
              </Grid.Column>
              <Grid.Column>
                <h1>{pending}</h1>
                <Label circular color='grey'>
                  <span
                    className='next-pack-approval-status-emoji'
                    role='img'
                    aria-label=''>
                    🙇
                  </span>
                  Pending
                </Label>
              </Grid.Column>
              <Grid.Column>
                <h1>{rejected}</h1>
                <Label circular color='grey'>
                  <span
                    className='next-pack-approval-status-emoji'
                    role='img'
                    aria-label=''>
                    😩
                  </span>
                  Rejected
                </Label>
              </Grid.Column>
            </Grid>
          </Card.Header>
        </Card>
      </div>
    );
  }

}


export default PackApproval;
