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
import { Grid, Header, Icon, Table } from 'semantic-ui-react';


import './Approved.css';
import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import ApprovedNav from '../../components/nav/ApprovedNav';


/**
 *
 * @class         Approved
 * @description   Approved component
 *
 */
class Approved extends Component {

  state = { column: null, direction: null, selectedProposal: {} };


  /**
   * Entry point to perform tasks required to render
   * component. On load, get confirmed proposals.
   */
  componentDidMount () {
    const { confirmedProposals, getConfirmedProposals } = this.props;
    document.querySelector('body').classList.add('minimal');
    !confirmedProposals && getConfirmedProposals();
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { confirmedProposals } = this.props;
    if (prevProps.confirmedProposals !== confirmedProposals) this.init();
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    document.querySelector('body').classList.remove('minimal');
  }


  /**
   * Determine which roles and users are not currently loaded
   * in the client and dispatches actions to retrieve them.
   */
  init () {
    const {
      getRoles,
      getUsers,
      roles,
      confirmedProposals,
      users } = this.props;

    if (!confirmedProposals) return;

    let diff = roles && confirmedProposals.filter(proposal =>
      roles.find(role => role.id !== proposal.object));
    let diff2 = users && confirmedProposals.filter(proposal =>
      users.find(user => user.id !== proposal.opener));

    diff = roles ?
      diff.map(proposal => proposal.object) :
      confirmedProposals.map(proposal => proposal.object);
    diff2 = users ?
      diff2.map(proposal => proposal.opener) :
      confirmedProposals.map(proposal => proposal.opener);

    diff && diff.length > 0 && getRoles(diff);
    diff2 && diff2.length > 0 && getUsers([...new Set(diff2)]);
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
   * Render confirmed proposals table
   * @returns {JSX}
   */
  renderTable () {
    const { confirmedProposals } = this.props;
    const { column, direction } = this.state;

    return (
      <Table sortable selectable>
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
              sorted={column === 'approved_date' ? direction : null}
              onClick={this.handleSort('approved_date')}>
              Approved On
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          { confirmedProposals && confirmedProposals.map(proposal => (
            <Table.Row
              key={proposal.id}
              onClick={() => this.setSelectedProposal(proposal)}>
              <Table.Cell>
                {this.roleName(proposal.object)}
              </Table.Cell>
              <Table.Cell>
                {this.userName(proposal.opener)}
              </Table.Cell>
              <Table.Cell className='next-approver-approved-table-email'>
                {this.userEmail(proposal.opener)}
                <Icon name='info circle' color='grey'/>
              </Table.Cell>
              <Table.Cell>
                Unavailable
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
    const { confirmedProposals } = this.props;
    const { selectedProposal } = this.state;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={12}>
          <TrackHeader title='Approved Requests' {...this.props}/>
          <div id='next-approver-approved-content'>
            <ApprovedNav/>
            { !confirmedProposals || confirmedProposals.length === 0 ?
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>
                  You haven&apos;t approved any items
                </Header.Content>
              </Header> :
              this.renderTable()
            }
          </div>
        </Grid.Column>
        <Grid.Column
          id='next-approver-grid-converse-column'
          width={4}>
          <Chat
            disabled={true}
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

export default connect(mapStateToProps, mapDispatchToProps)(Approved);
