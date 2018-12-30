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


import './RoleSelectGrid.css';


/**
 *
 * @class         RoleSelectGrid
 * @description   Create new pack component
 *
 */
class RoleSelectGrid extends Component {

  state = {  };


  /**
   * Handle change event
   * @param {object} event Event passed by Semantic UI
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    return (
      <Grid id='next-role-select-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <h1>Role select grid</h1>
        </Grid.Column>
      </Grid>
    );
  }

}


export default RoleSelectGrid;
