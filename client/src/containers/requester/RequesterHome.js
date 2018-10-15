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
import { Grid } from 'semantic-ui-react';


import TrackHeader from '../../components/layouts/TrackHeader';


import PropTypes from 'prop-types';


import './RequesterHome.css';


/**
 * 
 * @class RequesterHome
 * Component encapsulating the requester home, which serves as the
 * default landing page after login. 
 * 
 */
export default class RequesterHome extends Component {

  /**
   * 
   * Hydrate base data
   * 
   */
  componentDidMount () {
    const { getBase } = this.props;
    getBase();
  }


  render () {
    return (
      <Grid id='next-requester-grid' celled='internally'>
        <Grid.Column
          id='next-requester-grid-track-column'
          width={16}>
          <TrackHeader title='Home' {...this.props}/>
        </Grid.Column>
      </Grid>
    );
  }

}


RequesterHome.proptypes = {
  activePack: PropTypes.arrayOf(PropTypes.shape(
    {
      id: PropTypes.string,
      description: PropTypes.string,
      roles: PropTypes.arrayOf(PropTypes.shape(
        {
          id: PropTypes.string,
          name: PropTypes.string,
          email: PropTypes.email
        }  
      ))
    }
  ))
};
