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

Chat messages
Component encapsulating chat messages */


import React, { Component } from 'react';
import { Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';


export default class ChatMessage extends Component {

  static propTypes = {
    messages: PropTypes.array,
  }


  isMe = (message) => {
    return false;
  };


  render () {
    const { messages } = this.props;

    if (!messages) return null;

    return (
      messages &&
      messages.map((message, index) => (
        this.isMe(message) ?
          <Segment compact inverted
            floated='right'
            color='blue'
            className='clear next-chat-message-right'
            size='small'
            key={index}>
            <div>{message.text}</div>
          </Segment> :
          <Segment compact
            floated='left'
            className='clear next-chat-message-left'
            size='small'
            key={index}>
            <div>{message.text}</div>
          </Segment>
      ))
    );
  }

}
