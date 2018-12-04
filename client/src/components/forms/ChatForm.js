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
/*

Chat form
Component encapsulating a reusable chat form
suitable for composing within containers where chat
functionality is required */


import React, { Component } from 'react';
import { Button, Form, Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';


/**
 *
 * @class       ChatForm
 * @description Component encapsulating a reusable chat form
 *              suitable for composing within containers where chat
 *              functionality is required
 *
 */
export default class ChatForm extends Component {

  static propTypes = {
    actions:          PropTypes.object.isRequired,
    disabled:         PropTypes.bool,
    messages:         PropTypes.array,
    refreshOnNextSocketReceive: PropTypes.func,
    submit:           PropTypes.func.isRequired,
  };


  state = { message: '', isDraft: null };


  /**
   * Called whenever Redux state changes. Determine whether or not
   * the chat form should display a draft text area.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { messages } = this.props;

    if (messages !== prevProps.messages) {
      try {
        this.setState({
          isDraft: messages[0].buttons[0].payload.startsWith('/send'),
        });
      } catch {}
    }

  }


  /**
   * Reset form to default state
   */
  reset () {
    this.setState({ message: '', isDraft: null });
  }


  /**
   * Tell app to refresh to refresh when next message received
   * and send message to parent handler for dispatch
   * @param {string} message Message to send
   * @param {boolean} shouldRefresh If app should refresh on next
   *                                message received
   */
  handleSubmit (message, shouldRefresh) {
    const { refreshOnNextSocketReceive, submit } = this.props;
    shouldRefresh && refreshOnNextSocketReceive(true);
    submit(message);
    this.reset();
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
  }


  /**
   * Create intent payload to send back to chatbot engine,
   * inserting the current message to send in the body if
   * the intend is /send. Otherwise, the payload is the original
   * intent from the the button payload.
   *
   * @param {string} payload Payload in button object
   *                         sent rom chatbot engine
   *                 @example "Yes, please.", "No, thanks.",
   *                 '/send{"reason": "..."}')
   * @returns {string}
   */
  createPayload = (payload) => {
    const { message } = this.state;
    if (!payload.startsWith('/') || payload.indexOf('{') === -1) return payload;

    let demarcation = payload.indexOf('{');
    let parsed = JSON.parse(
      payload.substring(demarcation, payload.length)
    );
    if (parsed.reason) {
      parsed.reason = message;
      return payload.substring(0, demarcation) + JSON.stringify(parsed);
    }
    return payload;
  }


  /**
   * Render chat view action buttons
   * @returns {JSX}
   */
  renderActions () {
    const { disabled, messages } = this.props;
    const { isDraft } = this.state;

    return (
      <div id='next-chat-actions'>
        { messages && messages[0] && messages[0].buttons &&
          messages[0].buttons.map((button, index) => (
            <Button
              key={index}
              className='next-chat-action-button'
              circular
              size='medium'
              disabled={disabled}
              onClick={() =>
                this.handleSubmit(this.createPayload(button.payload), isDraft)}>

              { !disabled &&
                <span>{button.title}</span>
              }
              { disabled &&
                <span></span>
              }
            </Button>
          ))
        }
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { message, isDraft } = this.state;

    return (
      <div>
        { !isDraft &&
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
        </div>
        }
        { isDraft &&
        <div id='next-chat-form-draft-container'>
          <Form
            onSubmit={() =>
              this.handleSubmit(`/send{"reason": "${message}"}`, true)}>
            <Form.TextArea id='next-chat-form-draft-textarea'
              placeholder='Draft your message...'
              name='message'
              value={message}
              onChange={this.handleChange}/>
          </Form>
        </div>
        }
        {this.renderActions()}
      </div>
    );
  }

}
