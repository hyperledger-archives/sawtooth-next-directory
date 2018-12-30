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
import { Button, Form, Grid, Transition } from 'semantic-ui-react';


import './CreatePack.css';
import TrackHeader from 'components/layouts/TrackHeader';
import RoleSelectGrid from './RoleSelectGrid';
import * as theme from 'services/Theme';


/**
 *
 * @class         CreatePack
 * @description   Create new pack component
 *
 */
class CreatePack extends Component {

  state = { activeIndex: 0, name: '', validName: null };
  themes = ['minimal', 'contrast'];


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    theme.apply(this.themes);
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Create a new pack
   * @param {string} name Name of pack
   */
  createPack = () => {
    const { name } = this.state;
    const { createPack, id } = this.props;
    createPack({
      name,
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
   * Set current view
   * @param {number} index View index
   */
  setFlow = (index) => {
    this.setState({ activeIndex: index });
  }


  /**
   * Validate create pack form
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
    const { activeIndex, validName } = this.state;

    const hide = 0;
    const show = 300;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            title='Packs'
            button={() =>
              <Button
                id='next-approver-manage-exit-button'
                as={Link}
                icon='close'
                size='huge'
                to='/approval/manage/packs'/>}
            {...this.props}/>
          <div id='next-approver-manage-content'>
            {/* <CreatePackForm/>
          </div> */}
            <Transition
              visible={activeIndex === 0}
              animation='fade right'
              duration={{ hide, show }}>
              <div id='next-approver-manage-create-pack-view-1'>
                <Form>
                  <Form.Input
                    id='next-approver-manage-content-form'
                    label='Title'
                    autoFocus
                    error={validName === false}
                    name='name'
                    placeholder='Title'
                    onChange={this.handleChange}/>
                  <Form.TextArea
                    label='Description'
                    name='description'
                    placeholder='Description'/>
                </Form>
              </div>
            </Transition>
            <Transition
              visible={activeIndex === 1}
              animation='fade left'
              duration={{ hide, show }}>
              <div id='next-approver-manage-create-pack-view-2'>
                <RoleSelectGrid/>
              </div>
            </Transition>
            <div id='next-approver-manage-create-pack-toolbar'>
              { activeIndex === 0 &&
                <Button
                  primary
                  size='large'
                  id='next-approver-manage-create-pack-done-button'
                  disabled={!validName}
                  content='Next'
                  onClick={() => this.setFlow(1)}/>
              }
              { activeIndex === 1 &&
                <div>
                  <Button
                    size='large'
                    id='next-approver-manage-create-pack-back-button'
                    content='Back'
                    onClick={() => this.setFlow(0)}/>
                  <Button
                    primary
                    size='large'
                    as={Link}
                    to={'/approval/manage/packs'}
                    id='next-approver-manage-create-pack-done-button'
                    disabled={!validName}
                    content='Done'
                    onClick={this.createPack}/>
                </div>
              }
            </div>
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default CreatePack;
