/* Copyright 2019 Contributors to Hyperledger Sawtooth

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
import {
  Grid,
  Header,
  Icon,
  Placeholder,
  Table } from 'semantic-ui-react';


import './Rejected.css';
import Chat from 'components/chat/Chat';
import TrackHeader from 'components/layouts/TrackHeader';
import ApprovedNav from 'components/nav/ApprovedNav';
import glyph from 'images/glyph-individual.png';
import Avatar from 'components/layouts/Avatar';


import * as utils from 'services/Utils';


/**
 *
 * @class         Rejected
 * @description   Rejected component
 *
 */
class Rejected extends Component {

  state = { column: null, direction: null, selectedProposal: {} };


  /**
   * Entry point to perform tasks required to render
   * component. On load, get rejected proposals.
   */
  componentDidMount () {
    const { getRejectedProposals } = this.props;
    getRejectedProposals();
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { rejectedProposals } = this.props;
    if (prevProps.rejectedProposals !== rejectedProposals) this.init();
  }


  /**
   * Determine which roles and users are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const {
      getRoles,
      getUsers,
      roles,
      rejectedProposals,
      users } = this.props;

    if (!rejectedProposals) return;

    let diff = roles && rejectedProposals.filter(
      proposal => !roles.find(role => role.id === proposal.object)
    );
    let diff2 = users && rejectedProposals.filter(
      proposal => !users.find(user => user.id === proposal.opener)
    );
    let diff3 = users && rejectedProposals.filter(
      proposal => !users.find(user => user.id === proposal.closer)
    );
    diff = roles ?
      diff.map(proposal => proposal.object) :
      rejectedProposals.map(proposal => proposal.object);
    diff2 = users ?
      diff2.map(proposal => proposal.opener) :
      rejectedProposals.map(proposal => proposal.opener);
    diff3 = users ?
      diff3.map(proposal => proposal.closer) :
      rejectedProposals.map(proposal => proposal.closer);

    diff && diff.length > 0 && getRoles(diff);
    diff2 && diff2.length > 0 && getUsers([...new Set(diff2)], true);
    diff3 && diff3.length > 0 && getUsers([...new Set(diff3)], true);
  }


  /**
   * Get role name from role ID
   * @param {string} roleId Role ID
   * @returns {string}
   */
  roleName = (roleId) => {
    const { roleFromId } = this.props;
    const role = roleFromId(roleId);
    return role && role.name;
  };


  /**
   * Get user name from user ID
   * @param {string} userId User ID
   * @returns {string}
   */
  userName = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    return user && user.name;
  };


  /**
   * Get user email from user ID
   * @param {string} userId User ID
   * @returns {string}
   */
  userEmail = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    return user && user.email;
  };



  /**
   * Sort
   */
  handleSort = () => {
    // Not yet implemented
  };


  /**
   * Set selected proposal
   * @param {object} selectedProposal Proposal clicked on in table
   */
  setSelectedProposal = (selectedProposal) => {
    this.setState({ selectedProposal });
  }


  /**
   * Render placeholder graphics
   * @returns {JSX}
   */
  renderPlaceholder = () => {
    return (
      <div id='next-approver-rejected-placeholder'>
        { Array(2).fill(0).map((item, index) => (
          <Placeholder fluid key={index}>
            <Placeholder.Header>
              <Placeholder.Line length='full'/>
              <Placeholder.Line/>
            </Placeholder.Header>
          </Placeholder>
        ))}
      </div>
    );
  }


  /**
   * Render rejected proposals table
   * @returns {JSX}
   */
  renderTable () {
    const { rejectedProposals } = this.props;
    const { column, direction } = this.state;

    return (
      <Table
        sortable
        selectable
        singleLine
        striped
        padded='very'
        className='cursor-pointer'>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell
              sorted={column === 'role_name' ? direction : null}
              onClick={this.handleSort('role_name')}>
              Role Name
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'requester' ? direction : null}
              onClick={this.handleSort('requester')}>
              Requester
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'requester_email' ? direction : null}
              onClick={this.handleSort('requester_email')}>
              Requester Email
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'rejected_date' ? direction : null}
              onClick={this.handleSort('rejected_date')}>
              Rejected On
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'closer' ? direction : null}
              onClick={this.handleSort('closer')}>
              Rejected By
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          { rejectedProposals && rejectedProposals.map(proposal => (
            <Table.Row
              key={proposal.id}
              onClick={() => this.setSelectedProposal(proposal)}>
              <Table.Cell>
                {this.roleName(proposal.object)}
              </Table.Cell>
              <Table.Cell>
                <Header as='h4' className='next-approver-rejected-table-user'>
                  <Avatar
                    userId={proposal.opener}
                    size='small'
                    {...this.props}/>
                  <Header.Content>
                    {this.userName(proposal.opener)}
                  </Header.Content>
                </Header>
              </Table.Cell>
              <Table.Cell className='next-approver-rejected-table-email'>
                {this.userEmail(proposal.opener)}
                <Icon name='info circle' color='grey'/>
              </Table.Cell>
              <Table.Cell>
                {utils.formatDate(proposal.closed_date)}
              </Table.Cell>
              <Table.Cell>
                <Header as='h4' className='next-approver-rejected-table-user'>
                  <Avatar
                    userId={proposal.closer}
                    size='small'
                    {...this.props}/>
                  <Header.Content>
                    {this.userName(proposal.closer)}
                  </Header.Content>
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { rejectedProposals } = this.props;
    const { selectedProposal } = this.state;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={12}>
          <TrackHeader
            inverted
            glyph={glyph}
            title='Rejected Requests'
            {...this.props}/>
          <div id='next-approver-rejected-content'>
            <ApprovedNav/>
            { !rejectedProposals &&
              this.renderPlaceholder()
            }
            { rejectedProposals && rejectedProposals.length > 0 &&
              this.renderTable()
            }
            { rejectedProposals && rejectedProposals.length === 0 &&
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  You haven&#39;t rejected any items
                </Header.Content>
              </Header>
            }
          </div>
        </Grid.Column>
        <Grid.Column
          id='next-approver-grid-converse-column'
          width={4}>
          <Chat
            disabled={true}
            hideButtons
            selectedProposal={selectedProposal}
            subtitle={this.roleName(selectedProposal.object)}
            title={this.userName(selectedProposal.opener)}
            type='APPROVER' {...this.props}/>
        </Grid.Column>
      </Grid>
    );
  }

}


const mapStateToProps = (state) => {
  return {};
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(Rejected);
