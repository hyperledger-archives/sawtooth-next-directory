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
import { Image, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import chatbotAvatar from '../../images/chatbot-avatar.png';


/**
 *
 * @class         ChatMessage
 * @description   Component encapsulating the chat messages
 *
 */
class ChatMessage extends Component {

  static propTypes = {
    messages: PropTypes.array,
  }


  /**
   * Determine if comment is from user or external source
   * @param {object} message Message object
   * @returns {boolean}
   */
  isMe = (message) => {
    return !message.recipient_id && !message.from;
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { messages } = this.props;
    if (!messages) return null;

    return (
      messages &&
      messages.map((message, index) =>
        this.isMe(message) ?
          message.text &&
          <div className='next-chat-message-right' key={index}>
            <Segment compact inverted
              floated='right'
              color='purple'
              size='small'>
              <div>{message.text}</div>
            </Segment>
          </div> :
          <div className='next-chat-message-left' key={index}>
            { message.from ?
              <Image src='http://i.pravatar.cc/150' size='mini' avatar/> :
              <Image src={chatbotAvatar} size='mini'/>
            }
            <Segment compact
              floated='left'
              size='small'>
              <div>{message.text}</div>
            </Segment>
          </div>
      )
    );
  }
}


export default ChatMessage;
