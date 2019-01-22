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
import { Button, Form, Grid, Transition } from 'semantic-ui-react';


import './CreateDelegation.css';
import TrackHeader from 'components/layouts/TrackHeader';
import * as theme from 'services/Theme';
import SelectDelegatedRoles from './SelectDelegatedRoles';


/**
 *
 * @class         CreateDelegation
 * @description   Create new delegation component
 *
 */
class CreateDelegation extends Component {

  state = {
    activeIndex:      0,
    delegate:         '',
    delegateMessage:  '',
    requesterMessage: '',
    selectedRoles:    [],
    validDates:       null,
  };


  themes = ['minimal', 'contrast', 'magenta'];


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
   * Create a new delegation
   */
  createDelegation = () => {
    const {
      delegate,
      delegateMessage,
      requesterMessage,
      selectedRoles } = this.state;
    const { createDelegation, id } = this.props;
    createDelegation({
      id,
      delegate,
      delegateMessage,
      requesterMessage,
      roles: selectedRoles,
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
   * Validate create delegation form
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  validate = (name, value) => {
    // Not implemented
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      activeIndex,
      delegate,
      delegateMessage,
      requesterMessage,
      selectedRoles,
      validDates } = this.state;

    const hide = 0;
    const show = 700;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Create Delegation'
            breadcrumb={[
              {name: 'Manage', slug: '/approval/manage'},
              {name: 'Delegations', slug: '/approval/manage/delegations'},
            ]}
            button={() =>
              <Button
                id='next-approver-manage-exit-button'
                as={Link}
                icon='close'
                size='huge'
                to='/approval/manage/delegations'/>}
            {...this.props}/>
          <div id='next-approver-manage-create-delegation-content'>
            { activeIndex === 0 &&
              <Transition
                visible={activeIndex === 0}
                animation='fade right'
                duration={{ hide, show }}>
                <div id='next-approver-manage-create-delegation-view-1'>
                  <Grid container>
                    <Grid.Column width={6}>
                      <SelectDelegatedRoles
                        selectedRoles={selectedRoles}
                        {...this.props}/>
                    </Grid.Column>
                    <Grid.Column width={10}>
                      <Form id='next-approver-manage-create-delegation-form'>
                        <h3>
                          Delegate to
                        </h3>
                        <Form.Input id='next-create-delegation-title-field'
                          label='Select a delegate.'
                          autoFocus
                          name='delegate'
                          value={delegate}
                          placeholder='John Smith'
                          onChange={this.handleChange}/>
                        <Form.Group widths='equal'>
                          <Form.Input
                            fluid
                            label='From'
                            defaultValue='November 1st 2018'/>
                          <Form.Input
                            fluid
                            label='To'
                            defaultValue='November 1st 2019'/>
                        </Form.Group>
                        <div id='next-create-delegation-message-fields'>
                          <h3>
                            Message to the delegate
                          </h3>
                          <Form.TextArea
                            rows='3'
                            label='Lorem ipsum dolor sit amet.'
                            name='description'
                            value={delegateMessage}
                            onChange={this.handleChange}
                            placeholder={
                              'A long time ago in a galaxy far, far away....'
                            }/>
                          <h3>
                            Note to requesters
                          </h3>
                          <Form.TextArea
                            rows='3'
                            label='Lorem ipsum dolor sit amet.'
                            name='description'
                            value={requesterMessage}
                            onChange={this.handleChange}
                            placeholder={
                              'A long time ago in a galaxy far, far away....'
                            }/>
                        </div>
                      </Form>
                    </Grid.Column>
                  </Grid>
                </div>
              </Transition>
            }
            <Transition
              visible={activeIndex === 1}
              animation='fade left'
              duration={{ hide, show }}>
              <div id='next-approver-manage-create-delegation-view-2'>
                <h3>
                  Select Delegate
                </h3>
              </div>
            </Transition>
            <div id='next-approver-manage-create-delegation-toolbar'>
              { activeIndex === 0 &&
                <Button
                  primary
                  size='large'
                  id='next-approver-manage-create-delegation-done-button'
                  disabled={!validDates}
                  content='Next'
                  onClick={() => this.setFlow(1)}/>
              }
              { activeIndex === 1 &&
                <div>
                  <Button
                    size='large'
                    id='next-approver-manage-create-delegation-back-button'
                    content='Back'
                    onClick={() => this.setFlow(0)}/>
                  <Button
                    primary
                    size='large'
                    as={Link}
                    to={'/approval/manage/delegations'}
                    id='next-approver-manage-create-delegation-done-button'
                    disabled={!validDates}
                    content='Done'
                    onClick={this.createDelegation}/>
                </div>
              }
            </div>
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default CreateDelegation;
