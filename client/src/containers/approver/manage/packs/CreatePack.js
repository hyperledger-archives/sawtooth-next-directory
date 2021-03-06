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
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Form, Grid, Icon, Label } from 'semantic-ui-react';


import './CreatePack.css';
import { ApproverActions, ApproverSelectors } from 'state';
import TrackHeader from 'components/layouts/TrackHeader';
import RoleSelectGrid from './RoleSelectGrid';
import * as theme from 'services/Theme';
import * as utils from 'services/Utils';


/**
 *
 * @class         CreatePack
 * @description   Create new pack component
 *
 */
class CreatePack extends Component {

  state = {
    activeIndex:    0,
    description:    '',
    name:           '',
    selectedRoles:  [],
    validName:      null,
  };


  themes = ['contrast', 'magenta'];


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    const { resetPackExists } = this.props;
    theme.apply(this.themes);
    resetPackExists();
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Create a new pack
   */
  createPack = () => {
    const { description, name, selectedRoles } = this.state;
    const { createPack, id } = this.props;
    createPack({
      name,
      description,
      owners:         [id],
      administrators: [id],
      roles:          selectedRoles,
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


  handleBlur = () => {
    const { checkPackExists } = this.props;
    const { name } = this.state;
    !utils.isWhitespace(name) && checkPackExists(name);
  }


  /**
   * Handle click event
   * @param {string} roleId Selected role ID
   */
  handleClick = (roleId) => {
    this.setState(prevState => ({
      selectedRoles: (() => {
        const index = prevState.selectedRoles.indexOf(roleId);
        return index !== -1 ? [
          ...prevState.selectedRoles.slice(0, index),
          ...prevState.selectedRoles.slice(index + 1)] :
          [...prevState.selectedRoles, roleId];
      })(),
    }));
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
    const {
      activeIndex,
      description,
      name,
      selectedRoles,
      validName } = this.state;
    const { packExists } = this.props;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Create Pack'
            breadcrumb={[
              {name: 'Manage', slug: '/approval/manage'},
              {name: 'Packs', slug: '/approval/manage/packs'},
            ]}
            button={() =>
              <Button
                id='next-approver-manage-exit-button'
                as={Link}
                icon='close'
                size='huge'
                to='/approval/manage/packs'/>}
            {...this.props}/>
          <div id='next-approver-manage-create-pack-content'>
            { activeIndex === 0 &&
              <div id='next-approver-manage-create-pack-view-1'>
                <Form id='next-approver-manage-create-pack-form'>
                  <h3>
                    Title
                  </h3>
                  <Form.Input id='next-create-pack-title-field'
                    label='Create a descriptive name for your new pack.'
                    autoFocus
                    error={validName === false}
                    name='name'
                    value={name}
                    placeholder='My Awesome Pack'
                    onBlur={this.handleBlur}
                    onChange={this.handleChange}/>
                  { packExists &&
                    <Label
                      basic
                      id='next-approver-manage-create-pack-error-label'>
                      <Icon name='exclamation circle'/>
                      This pack name already exists.
                    </Label>
                  }
                  <h3>
                    Description
                  </h3>
                  <Form.TextArea
                    rows='6'
                    label={`Create a compelling description of your new pack
                            that clearly explains its intended use.`}
                    name='description'
                    value={description}
                    onChange={this.handleChange}
                    placeholder={
                      'A long time ago in a galaxy far, far away....'
                    }/>
                </Form>
              </div>
            }
            { activeIndex === 1 &&
              <div id='next-approver-manage-create-pack-view-2'>
                <RoleSelectGrid
                  handleClick={this.handleClick}
                  selectedRoles={selectedRoles}
                  {...this.props}/>
              </div>
            }
            <div id='next-approver-manage-create-pack-toolbar'>
              { activeIndex === 0 &&
                <Button
                  primary
                  size='large'
                  id='next-approver-manage-create-pack-done-button'
                  disabled={!validName || packExists}
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
                    disabled={!validName || packExists}
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


const mapStateToProps = (state) => {
  return {
    packExists: ApproverSelectors.packExists(state),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    checkPackExists: (name) =>
      dispatch(ApproverActions.packExistsRequest(name)),
    resetPackExists: (name) => dispatch(ApproverActions.resetPackExists()),
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(CreatePack);
