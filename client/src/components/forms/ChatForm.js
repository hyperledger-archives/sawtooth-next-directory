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
import { Button, Form, Icon } from 'semantic-ui-react';


import PropTypes from 'prop-types';


/**
 *
 * @class ChatForm
 * Component encapsulating a reusable chat form suitable for
 * composing within containers where chat functionality is required
 *
 * TODO: Add validation to forms
 *
 */
export default class ChatForm extends Component {

  constructor (props) {
    super(props);

    this.state = { message: '' };
  }

 
  /**
   *
   * @param event   Event passed by Semantic UI
   * @param name    Name of form element derived from 'name' HTML attribute
   * @param value   Value of form field
   *
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value });
  }


  handleSubmit (action) {
    const { submit } = this.props;
    const { message } = this.state;

    submit(message, action);
    this.reset();
  }



  reset () {
    this.setState({ message: '' });
  }


  renderActions () {
    const { actions } = this.props;

    return (
      <div id='next-chat-actions'>
        { actions &&
          actions.action_types.map((action, index) => (
            <Button
              key={index}
              icon
              onClick={() => this.handleSubmit(action)}
            >
              {action.type === 0 && <Icon name='check circle' /> }
              {action.type === 1 && <Icon name='x' /> }
              {action.action_text}
            </Button>
          ))
        }
      </div>
    )
  }


  render () {
    const { message } = this.state;

    return (
      <div>

        <Form onSubmit={() => this.handleSubmit(message)}>
          <Form.Input
            icon
            fluid
            placeholder='Say something...'
            name='message'
            value={this.state.message}
            onChange={this.handleChange}
          >
            <input />
            <Icon
              link
              name='paper plane'
              onClick={() => this.handleSubmit(message)}
            />
          </Form.Input>
        </Form>

        {this.renderActions()}

      </div>
    );
  }

}
