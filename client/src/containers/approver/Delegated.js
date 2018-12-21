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
import { Grid, Header } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import IndividualsNav from '../../components/nav/IndividualsNav';
import PeopleList from '../../components/layouts/proposals/PeopleList';
import RoleList from '../../components/layouts/proposals/RoleList';
import { syncAll } from './IndividualsHelper';


import './Delegated.css';
import glyph from '../../images/header-glyph-individual.png';


/**
 *
 * @class         Delegated
 * @description   Individual requests component
 *
 */
class Delegated extends Component {

  static propTypes = {
    getOpenProposals: PropTypes.func,
  };


  state = {
    selectedRoles:      [],
    selectedUsers:      [],
    selectedProposals:  [],
    activeIndex:        0,
  };


  /**
   * Entry point to perform tasks required to render
   * component. On load, get open proposals.
   */
  componentDidMount () {
    const { getOpenProposals, openProposals, onBehalfOf } = this.props;
    !openProposals && getOpenProposals(onBehalfOf);
    document.querySelector('body').classList.add('minimal');
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    document.querySelector('body').classList.remove('minimal');
  }


  /**
   * Switch between Roles and People views
   * @param {number} activeIndex Current screen index
   */
  setFlow = (activeIndex) => {
    this.setState({ activeIndex });
  };


  reset = () => {
    this.setState({
      selectedRoles:      [],
      selectedUsers:      [],
      selectedProposals:  [],
    });
  }


  /**
   * Handle proposal change event
   * When a proposal is checked or unchecked, select or deselect
   * the parent user, taking into account the currently
   * checked sibling proposals.
   * @param {object} event Event passed on change
   * @param {object} data  Attributes passed on change
   */
  handleChange = (event, data) => {
    const sync = syncAll.call(
      this,
      data.checked,
      data.role,
      data.proposal,
      data.user,
    );

    const { roles, proposals } = sync.next().value;
    const { users } = sync.next().value;

    this.setState({
      selectedRoles:      roles,
      selectedProposals:  proposals,
      selectedUsers:      users,
    });
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { openProposals, userFromId } = this.props;
    const {
      activeIndex,
      selectedProposals,
      selectedRoles,
      selectedUsers } = this.state;

    const user = selectedUsers && userFromId(selectedUsers[0]);
    const title = user && user.name;
    const subtitle = `${selectedProposals.length}
      ${selectedProposals.length > 1 ? 'requests' : 'request'}
      selected`;

    return (
      <Grid id='next-approver-grid'>

        <Grid.Column id='next-approver-grid-track-column' width={12}>
          <TrackHeader
            glyph={glyph}
            title='Delegated Requests'
            subtitle={openProposals && openProposals.length + ' pending'}
            {...this.props}/>
          <div id='next-approver-delegated-content'>
            <IndividualsNav
              activeIndex={activeIndex}
              setFlow={this.setFlow}/>
            { openProposals && openProposals.length !== 0 &&
              <div>
                { activeIndex === 0 &&
                  <RoleList
                    selectedProposals={selectedProposals}
                    selectedRoles={selectedRoles}
                    handleChange={this.handleChange}
                    {...this.props}/>
                }
                { activeIndex === 1 &&
                  <PeopleList
                    selectedProposals={selectedProposals}
                    selectedUsers={selectedUsers}
                    handleChange={this.handleChange}
                    {...this.props}/>
                }
              </div>
            }
            { openProposals && openProposals.length === 0 &&
              <Header as='h3' textAlign='center' color='grey'>
                <Header.Content>No pending items</Header.Content>
              </Header>
            }
          </div>
        </Grid.Column>

        <Grid.Column
          id='next-approver-grid-converse-column'
          width={4}>
          <Chat
            type='APPROVER'
            title={title}
            subtitle={subtitle}
            groupBy={activeIndex}
            disabled={!openProposals ||
              (openProposals && openProposals.length === 0)}
            selectedProposals={selectedProposals}
            selectedRoles={selectedRoles}
            selectedUsers={selectedUsers}
            handleChange={this.handleChange}
            reset={this.reset}
            {...this.props}/>
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

export default connect(mapStateToProps, mapDispatchToProps)(Delegated);

