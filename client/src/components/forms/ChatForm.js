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

  static propTypes = {
    actions:          PropTypes.object.isRequired,
    disabled:         PropTypes.bool,
    messages:         PropTypes.array,
    submit:           PropTypes.func.isRequired,
  };


  constructor (props) {
    super(props);

    this.state = { message: '' };
  }


  reset () {
    this.setState({ message: '' });
  }


  handleSubmit (message) {
    const { submit } = this.props;
    submit(message);
    this.reset();
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


  renderActions () {
    const { disabled, messages } = this.props;

    return (
      <div id='next-chat-actions'>
        { messages && messages[0] && messages[0].buttons &&
          messages[0].buttons.map((button, index) => (
            <Button
              key={index}
              animated='fade'
              className='next-chat-action-button'
              circular
              size='medium'
              disabled={disabled}
              onClick={() => this.handleSubmit(button.payload)}>

              { !disabled &&
                <span>
                  <Button.Content visible>
                    {button.title}
                  </Button.Content>
                </span>
              }
              { disabled &&
                <span></span>
              }
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
            onChange={this.handleChange}>
            <input autoComplete='off'/>
            <Icon
              link
              name='paper plane'
              onClick={() => this.handleSubmit(message)}/>
          </Form.Input>
        </Form>

        {this.renderActions()}

      </div>
    );
  }

}
