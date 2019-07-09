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
import {
  Button,
  Form,
  Grid,
  Header,
  Input,
  Label,
  Loader } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './EditUser.css';
// import PeopleNav from './PeopleNav';
import Avatar from 'components/layouts/Avatar';
import TrackHeader from 'components/layouts/TrackHeader';
import * as theme from 'services/Theme';


/**
 *
 * @class         EditUser
 * @description   Manage component
 *
 */
class EditUser extends Component {

  themes = ['contrast', 'magenta'];


  static propTypes = {
    editUser:              PropTypes.func,
    userFromId:            PropTypes.func,
    userId:                PropTypes.string,
  };


  state = {
    name:           '',
    email:          '',

    // Assume valid from server
    validName:      true,
    validEmail:     true,
  };


  /**
   * Entry point to perform tasks required to render
   * component.
   */
  componentDidMount () {
    theme.apply(this.themes);
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps, ) {
    const { userId, users } = this.props;
    if (prevProps.userId !== userId)
      this.init();
    if (prevProps.users && users &&
        prevProps.users.length !== users.length)
      this.init();
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Determine which roles are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const { getUser, userId, userFromId } = this.props;
    const { name, email } = this.state;

    const user = userFromId(userId);
    !user && getUser(userId);

    if (user && !name && !email)
      this.setState({ name: user.name, email: user.email });

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
   * Validate form input
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  validate = (name, value) => {
    // name === 'name' &&
    //   this.setState({ validName: value.length > 4 });
    name === 'email' &&
      this.setState({ validEmail: /\S+@\S+\.\S+/.test(value) });
  }


  enableSave = () => {
    const { userFromId, userId } = this.props;
    const { name, email, validEmail, validName } = this.state;

    const user = userFromId(userId);
    if (!user) return null;

    return (name !== user.name || email !== user.email) &&
      validEmail && validName;
  }


  /**
   * Edit user
   * @returns {undefined}
   */
  editUser = () => {
    const { userId, editUser, userFromId } = this.props;
    const { name, email } = this.state;

    const user = userFromId(userId);
    if (!user) return null;

    const payload = {
      next_id: userId,
      name,
      email,
      username: user.username,
    };

    editUser(payload);
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { fetchingEditUser, userId, userFromId } = this.props;
    const { email, name, validEmail, validName } = this.state;

    const user = userFromId(userId);
    if (!user) return null;

    return (
      <Grid id='next-approver-grid'>
        <Grid.Column
          id='next-approver-grid-track-column'
          width={16}>
          <TrackHeader
            inverted
            title='Edit User'
            subtitle="Modify a user's information"
            button={() =>
              <Button
                disabled={fetchingEditUser || !this.enableSave()}
                id='next-people-edit-user-save-button'
                onClick={() => this.editUser()}
                size='huge'
                content='Save'/>}
            {...this.props}/>
          <div id='next-people-edit-user-content'>
            {/* <PeopleNav
              // activeIndex={activeIndex}
              // setFlow={this.setFlow}
              {...this.props}/> */}
            <div>
              <Loader/>
              <Header as='h1'>
                <Avatar userId={userId} size='small' {...this.props}/>
                <Header.Content>
                  {user.name}
                </Header.Content>
              </Header>
              <Form id='next-edit-user-form' onSubmit={() => this.editUser()}>
                <span className='next-edit-user-form-label'>
                  Basic Info
                </span>
                <hr className='next-edit-user-form-hr'/>
                <Form.Group widths='equal'>
                  <Form.Field>
                    <Input
                      id='next-edit-user-input'
                      autoFocus
                      // placeholder={user.name}
                      error={validName === false}
                      name='name'
                      type='text'
                      onChange={this.handleChange}
                      value={name}/>
                  </Form.Field>
                  <Form.Field>
                    <Input
                      id='next-edit-user-input'
                      autoFocus
                      // placeholder={user.email}
                      error={validEmail === false}
                      name='email'
                      type='text'
                      onChange={this.handleChange}
                      value={email}/>
                    { !validEmail &&
                      <Label className='next-username-signup-hint'>
                        Please enter a valid email.
                      </Label>
                    }
                  </Form.Field>
                </Form.Group>
              </Form>
            </div>
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


const mapStateToProps = (state, ownProps) => {
  const { id } = ownProps.match.params;
  return {
    fetchingEditUser: state.user.fetchingEditUser,
    userId: id,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};


export default connect(mapStateToProps, mapDispatchToProps)(EditUser);
