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
import { Grid, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './PackApprovalList.css';
import * as utils from 'services/Utils';


/**
 *
 * @class         PackApprovalList
 * @description   This layout formats the display of an open request's
 *                current approval status. It displays who owns the resource,
 *                when the request was opened, and approval status.
 *
 */
class PackApprovalList extends Component {

  static propTypes = {
    proposals:          PropTypes.array,
    roles:              PropTypes.array,
    userFromId:         PropTypes.func,
  }


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
  }


  /**
   * Render user info
   * @param {string} userId User ID
   * @returns {JSX}
   */
  renderUserInfo = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    if (!user) return null;
    return (
      <div>
        { user.name &&
          <div>
            {user.name}
          </div>
        }
        {user.email &&
          <div>
            {user.email}
          </div>
        }
      </div>
    );
  }


  /**
   * Render status info
   * @param {string} status Status of proposal
   * @returns {JSX}
   */
  renderStatus (status) {
    return (
      <div>
        <div className='next-pack-approval-list-status'>
          { status === 'CONFIRMED' && <span>
            Approved
          </span> }
          { status === 'OPEN' && <span>
            Pending
          </span> }
          { status === 'REJECTED' && <span>
            Rejected
          </span> }
          <span
            className='next-pack-approval-list-status-emoji'
            role='img'
            aria-label=''>
            { status === 'CONFIRMED' && '👍' }
            { status === 'OPEN' && '🙇' }
            { status === 'REJECTED' && '😩' }
          </span>
        </div>
      </div>
    );
  }


  /**
   * Render role and approver info
   * @param {object} proposal Proposal
   * @returns {JSX}
   */
  renderProposalSegment (proposal) {
    const { roles } = this.props;
    if (!roles) return null;
    const role = roles.find(role => role.id === proposal.object);

    return (
      <Segment key={proposal.object}>
        <Grid columns={3} padded='vertically' id='next-pack-approval-list-grid'>
          <Grid.Column width={5}>
            {role && role.name}
          </Grid.Column>
          <Grid.Column width={7}>
            { proposal.approvers && proposal.approvers.map(approver => (
              <div
                key={approver}
                id='next-pack-approval-list-approvers'
                className='pull-left'>
                {this.renderUserInfo(approver)}
              </div>
            ))}
          </Grid.Column>
          <Grid.Column width={4}>
            {this.renderStatus(proposal.status)}
          </Grid.Column>
        </Grid>
      </Segment>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { proposals } = this.props;
    if (!proposals) return null;

    return (
      <div id='next-pack-approval-list-container'>
        { proposals.map(proposal => (
          this.renderProposalSegment(proposal)
        ))}
      </div>
    );
  }

}


export default PackApprovalList;
