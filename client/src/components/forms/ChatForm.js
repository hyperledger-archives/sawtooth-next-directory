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
import * as utils from '../../services/Utils';


/**
 *
 * @class       ChatForm
 * @description Component encapsulating a reusable chat form
 *              suitable for composing within containers where chat
 *              functionality is required
 *
 */
class ChatForm extends Component {

  static propTypes = {
    activePack:           PropTypes.object,
    activeRole:           PropTypes.object,
    approve:              PropTypes.func,
    disabled:             PropTypes.bool,
    messages:             PropTypes.array,
    refreshOnNextSocketReceive: PropTypes.func,
    reject:               PropTypes.func,
    send:                 PropTypes.func.isRequired,
    type:                 PropTypes.string,
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
      } catch {
        utils.noop();
      }
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
  handleSend (message, shouldRefresh) {
    const { refreshOnNextSocketReceive, send } = this.props;
    shouldRefresh && refreshOnNextSocketReceive(true);
    send(message);
    this.reset();
  }


  /**
   * Handle approval action
   * @param {number} action 0 (Reject) or 1 (Approve)
   */
  handleApprove = (action) => {
    const { approve, reject } = this.props;
    action === 0 && reject();
    action === 1 && approve();
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
    const { activePack, activeRole } = this.props;
    const { message } = this.state;
    if (!payload.startsWith('/') || payload.indexOf('{') === -1) return payload;

    let demarcation = payload.indexOf('{');
    let parsed = JSON.parse(
      payload.substring(demarcation, payload.length)
    );
    // Debugger;;

    if (parsed.resource_id) {
      parsed.resource_id = (activePack && activePack.id) ||
        (activeRole && activeRole.id);
    }
    if (parsed.resource_type) {
      parsed.resource_type = (activePack && 'PACK') ||
        (activeRole && 'ROLE');
    }
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
  renderRequesterActions () {
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
                this.handleSend(this.createPayload(button.payload), isDraft)}>

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
   * Render chat view approval buttons
   * @returns {JSX}
   */
  renderApproverActions () {
    const { disabled } = this.props;

    return (
      <div id='next-chat-actions'>
        <Button
          className='next-chat-action-button'
          circular
          size='medium'
          disabled={disabled}
          onClick={() => this.handleApprove(1)}>

          { !disabled &&
              <span>Approve</span>
          }
          { disabled &&
              <span></span>
          }
        </Button>
        <Button
          className='next-chat-action-button'
          circular
          size='medium'
          disabled={disabled}
          onClick={() => this.handleApprove(0)}>

          { !disabled &&
              <span>Reject</span>
          }
          { disabled &&
              <span></span>
          }
        </Button>
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { type } = this.props;
    const { message, isDraft } = this.state;

    return (
      <div>
        { !isDraft &&
        <div>
          <Form id='next-placeholder-chat'
            onSubmit={() => this.handleSend(message)}>
            <Form.Input
              id='next-chat-change'
              icon
              fluid
              placeholder='Say something...'
              name='message'
              value={this.state.message}
              onChange={this.handleChange}>
              <input autoComplete='off'/>
              <Icon
                link
                id='next-name-chat-submit'
                name='paper plane'
                onClick={() => this.handleSend(message)}/>
            </Form.Input>
          </Form>
        </div>
        }
        { isDraft &&
        <div id='next-chat-form-draft-container'>
          <Form
            onSubmit={() =>
              this.handleSend(`/send{"reason": "${message}"}`, true)}>
            <Form.TextArea id='next-chat-form-draft-textarea'
              placeholder='Draft your message...'
              name='message'
              value={message}
              onChange={this.handleChange}/>
          </Form>
        </div>
        }
        {type === 'REQUESTER' && this.renderRequesterActions()}
        {type === 'APPROVER' && this.renderApproverActions()}
      </div>
    );
  }
}


export default ChatForm;
