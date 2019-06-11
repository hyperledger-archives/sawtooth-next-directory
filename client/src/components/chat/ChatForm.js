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
import { Button, Form, Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './ChatForm.css';


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
    activePack:                 PropTypes.object,
    activeRole:                 PropTypes.object,
    approve:                    PropTypes.func,
    disabled:                   PropTypes.bool,
    formDisabled:               PropTypes.bool,
    hideButtons:                PropTypes.bool,
    hideForm:                   PropTypes.bool,
    location:                   PropTypes.object,
    messages:                   PropTypes.array,
    messagesById:               PropTypes.func,
    refreshOnNextSocketReceive: PropTypes.func,
    reject:                     PropTypes.func,
    requestPack:                PropTypes.func,
    requestRole:                PropTypes.func,
    send:                       PropTypes.func.isRequired,
    socketMaxAttemptsReached:   PropTypes.bool,
    type:                       PropTypes.string,
  };


  state = { message: '', isDraft: null };


  /**
   * Entry point to perform tasks required to render component.
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { location, messages } = this.props;

    if (messages !== prevProps.messages)
      this.init();

    if (location.pathname !== prevProps.location.pathname) {
      this.init();
      this.setState({ message: '' });
    }
  }


  /**
   * Determine whether or not the chat form should display
   * a draft text area.
   */
  init () {
    const { activePack, activeRole, messagesById } = this.props;
    try {
      const resourceId = (activePack && activePack.id) ||
        (activeRole && activeRole.id);
      const isSend = messagesById(resourceId)[0]
        .buttons[0]
        .payload
        .startsWith('/request');
      this.setState({ isDraft: isSend });
    } catch (error) {
      this.setState({ isDraft: false });
    }
  }


  /**
   * Reset form to default state
   */
  reset () {
    this.setState({ message: '', isDraft: null });
  }


  /**
   * Send message to parent handler for dispatch
   * @param {string}  message Message to send
   * @param {boolean} shouldRefresh DEPRECATED
   *                  If app should refresh on next
   *                  message received
   */
  handleSend = (message, shouldRefresh) => {
    const { refreshOnNextSocketReceive, send } = this.props;
    shouldRefresh && refreshOnNextSocketReceive(true);
    send(message);
    this.reset();
  }


  /**
   * Given the socket is experiencing errors, send manual
   * request to parent handler
   * @param {string} message Message to send
   */
  handleManualSend = (message) => {
    const { activePack, requestRole, requestPack } = this.props;
    activePack ? requestPack(message) : requestRole(message);
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
   * inserting the current message to send in the body given
   * the intent is /request_access. Otherwise, the payload
   * is the original intent from the the button payload.
   *
   * @param {string} payload Payload in button object
   *                         sent from chatbot engine
   *                 @example "Yes, please.", "No, thanks.",
   *                 '/request_access{"reason": "..."}')
   * @returns {string}
   */
  createPayload = (payload) => {
    const { activePack, activeRole } = this.props;
    const { message } = this.state;
    if (!payload.startsWith('/') || payload.indexOf('{') === -1)
      return payload;

    const demarcation = payload.indexOf('{');
    const parsed = JSON.parse(
      payload.substring(demarcation, payload.length)
    );

    // Clear chatbot error state
    parsed.batch_status = '1';

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
    const {
      activePack,
      activeRole,
      disabled,
      messagesById,
      socketMaxAttemptsReached } = this.props;
    const { message } = this.state;

    const resource = activePack || activeRole;
    const activeMessages = resource && messagesById(resource.id);

    return (
      <div id='next-chat-actions'>
        { activeMessages && activeMessages[0] &&
          !socketMaxAttemptsReached && activeMessages[0].buttons &&
          activeMessages[0].buttons.map((button, index) => (
            <Button
              key={index}
              className={`next-chat-action-button
                ${index < 1 ? 'primary' : 'basic'}`}
              circular
              size='medium'
              disabled={disabled}
              onClick={() =>
                this.handleSend(this.createPayload(button.payload), false)}>

              { !disabled &&
                <span>
                  {button.title}
                </span>
              }
              { disabled &&
                <span></span>
              }
            </Button>
          ))
        }
        { socketMaxAttemptsReached &&
          <Button fluid onClick={() => this.handleManualSend(message)}>
            Send Request
          </Button>
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
          primary
          size='medium'
          disabled={disabled}
          onClick={() => this.handleApprove(1)}>

          { !disabled &&
            <span>
              Approve
            </span>
          }
          { disabled &&
            <span></span>
          }
        </Button>
        <Button
          className='next-chat-action-button'
          circular
          basic
          size='medium'
          disabled={disabled}
          onClick={() => this.handleApprove(0)}>

          { !disabled &&
            <span>
              Reject
            </span>
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
    const {
      formDisabled,
      hideButtons,
      hideForm,
      socketMaxAttemptsReached,
      type } = this.props;
    const { message, isDraft } = this.state;
    const isManual = type === 'REQUESTER' && socketMaxAttemptsReached;

    return (
      <div>
        { !isDraft && !isManual && !hideForm &&
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
              <input disabled={formDisabled} autoComplete='off'/>
              <Icon
                link
                id='next-chat-form-submit-icon'
                name='paper plane'
                onClick={() => this.handleSend(message)}/>
            </Form.Input>
          </Form>
        </div>
        }
        { (isDraft || isManual) &&
        <div id='next-chat-form-draft-container'>
          <Form
            onSubmit={() => this.handleSend(this.createPayload(
              `/request_access${JSON.stringify(
                {reason: '', resource_id: '', resource_type: ''}
              )}`), false)}>
            <Form.TextArea id='next-chat-form-draft-textarea'
              placeholder='Draft your message...'
              autoFocus
              name='message'
              value={message}
              onChange={this.handleChange}/>
          </Form>
        </div>
        }
        {!hideButtons && type === 'REQUESTER' && this.renderRequesterActions()}
        {!hideButtons && type === 'APPROVER' && this.renderApproverActions()}
      </div>
    );
  }
}


export default ChatForm;
