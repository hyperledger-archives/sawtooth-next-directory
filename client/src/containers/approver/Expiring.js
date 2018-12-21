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
import { Grid } from 'semantic-ui-react';


import './Expiring.css';
import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';


/**
 *
 * @class         Expiring
 * @description   Expiring component
 *
 */
class Expiring extends Component {

  /**
   * Entry point to perform tasks required to render
   * component. On load, get open proposals.
   */
  componentDidMount () {
    document.querySelector('body').classList.add('minimal');
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    document.querySelector('body').classList.remove('minimal');
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={12}>
          <TrackHeader title='About to Expire' {...this.props}/>
        </Grid.Column>
        <Grid.Column
          id='next-approver-grid-converse-column'
          width={4}>
          <Chat type='APPROVER' {...this.props}/>
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

export default connect(mapStateToProps, mapDispatchToProps)(Expiring);
