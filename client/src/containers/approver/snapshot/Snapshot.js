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
import { Link } from 'react-router-dom';
import { Header, Button} from 'semantic-ui-react';
import PropTypes from 'prop-types';

import './Snapshot.css';
import SnapshotCard from './SnapshotCard';


/**
 *
 * @class         Snapshot
 * @description   Snapshot component
 *
 *
 */
class Snapshot extends Component {

  static propTypes = {
    openProposalsByRole:   PropTypes.object,
    openProposalsByUser:   PropTypes.object,
  };


  state = {
    snapshotData: [{ roleCount: '0', roleStatus: ''},
      { roleCount: '9', roleStatus: 'About to Expire', isimageNeeded: true},
      { roleCount: '3', roleStatus: 'Delegated'},
      { roleCount: '5', roleStatus: 'Unattended Since 1 Week'},
      { roleCount: '3', roleStatus: 'Escalated'},
      { roleCount: '18', roleStatus: 'Messages'}],
  };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    const { openProposalsByUser, openProposalsByRole } = this.props;
    const { snapshotData } = this.state;
    const copyofSnapshotData = [...snapshotData];
    const numberofRoles =  openProposalsByUser ?
      Object.keys(openProposalsByUser).length : '0';
    copyofSnapshotData[0].roleCount = numberofRoles;
    const pendingRoles =  openProposalsByRole ? 'Pending across ' +
      Object.keys(openProposalsByRole).length  + ' roles'
      : 'Pending across 0 roles';
    copyofSnapshotData[0].roleStatus = pendingRoles;
    this.setState({ snapshotData: copyofSnapshotData });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { snapshotData } = this.state;
    return (
      <div className='snapshot-main-container'>
        <div className='snapshot-header'>
          <Header id='next-snapshot-header'>
            Requests Snapshot
          </Header>
          <Button id='next-snapshot-button'
            as={Link}
            icon='close'
            size='huge'
            to='/approval/manage'/>
        </div>
        <div className='snapshot-sub-container'>
          {snapshotData.map((event, index) => (
            <SnapshotCard
              key= {index}
              isimageNeeded = {event.isimageNeeded}
              roleCount = {event.roleCount}
              roleStatus = {event.roleStatus}
            />
          ))}
        </div>
      </div>
    );
  }

};


export default Snapshot;
