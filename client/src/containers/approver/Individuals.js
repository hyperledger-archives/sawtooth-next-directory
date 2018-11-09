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
import PeopleList from '../../components/layouts/proposals/PeopleList';


import './Individuals.css';


/**
 *
 * @class Individuals
 * Individuals component
 *
 */
class Individuals extends Component {

  componentDidMount () {
    const { getOpenProposals } = this.props;

    getOpenProposals();
  }


  render () {
    const { openProposals } = this.props;

    return (
      <Grid id='next-approver-grid'>

        <Grid.Column
          id='next-approver-grid-track-column'
          width={10}>

          <TrackHeader title='Individuals' {...this.props}/>
          <div id='next-approver-individuals-content'>
            { openProposals && openProposals.length !== 0 ?
              <PeopleList {...this.props}/> :
              <Header as='h2' textAlign='center' disabled>
                <Header.Content>No items</Header.Content>
              </Header>
            }
          </div>

        </Grid.Column>
        <Grid.Column
          id='next-approver-grid-converse-column'
          width={6}>
          <Chat {...this.props}/>
        </Grid.Column>

      </Grid>
    );
  }

}


const mapStateToProps = (state) => {
  return {};
}

const mapDispatchToProps = (dispatch) => {
  return {};
}

export default connect(mapStateToProps, mapDispatchToProps)(Individuals);


Individuals.proptypes = {
  getOpenProposals: PropTypes.func
};
