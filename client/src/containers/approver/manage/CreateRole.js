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
import { Link } from 'react-router-dom';
import { Button, Form, Grid } from 'semantic-ui-react';


import './CreateRole.css';
import TrackHeader from '../../../components/layouts/TrackHeader';


/**
 *
 * @class         CreateRole
 * @description   Create new role component
 *
 */
class CreateRole extends Component {

  state = { name: '', validName: null };


  /**
   * Create a new role
   * @param {string} name Name of role
   */
  createRole = () => {
    const { name } = this.state;
    const { createRole, id } = this.props;
    createRole({
      name:           name,
      owners:         [id],
      administrators: [id],
    });
  }


  /**
   * Handle form change event
   * @param {object} event Event passed by Semantic UI
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value });
    this.validate(name, value);
  }


  /**
   * Validate create role form
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  validate = (name, value) => {
    name === 'name' &&
      this.setState({ validName: value.length > 4 });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { validName } = this.state;
    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Roles'
            button={() =>
              <Button as={Link} to='/approval/manage/roles'>Exit</Button>}
            {...this.props}/>
          <div id='next-approver-manage-content'>
            <Form>
              <Form.Input
                id='next-approver-manage-content-form'
                autoFocus
                error={validName === false}
                name='name'
                placeholder='Name'
                onChange={this.handleChange}/>
            </Form>
            <Button
              as={Link}
              to='/approval/manage/roles'
              disabled={!validName}
              onClick={this.createRole}>
                Done
            </Button>
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default CreateRole;
