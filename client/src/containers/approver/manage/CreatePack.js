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


import './CreatePack.css';
import TrackHeader from '../../../components/layouts/TrackHeader';


/**
 *
 * @class         CreatePack
 * @description   Create new role component
 *
 */
class CreatePack extends Component {

  state = { name: '', validName: null };


  /**
   * Create a new pack
   * @param {string} name Name of pack
   */
  createPack = () => {
    const { name } = this.state;
    const { createPack, userId } = this.props;
    createPack({
      name:           name,
      owners:         [userId],
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
            title='Packs'
            button={() =>
              <Button as={Link} to='/approval/manage/packs'>Exit</Button>}
            {...this.props}/>
          <div id='next-approver-manage-content'>
            <Form>
              <Form.Input
                autoFocus
                id='next-approver-manage-content-pack-form'
                error={validName === false}
                name='name'
                placeholder='Name'
                onChange={this.handleChange}/>
            </Form>
            <Button
              as={Link}
              to='/approval/manage/packs'
              disabled={!validName}
              onClick={this.createPack}>
                Done
            </Button>
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default CreatePack;
