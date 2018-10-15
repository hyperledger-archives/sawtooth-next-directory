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
import { Segment } from 'semantic-ui-react';


/**
 * 
 * @class ChatMessage
 * Component encapsulating the chat message
 * 
 */
export default class ChatMessage extends Component {

  /**
   * 
   * @todo Retrieve from auth session
   * 
   * 
   */
  isMe (message) {
    return message.from.id === '519909ec-f0c8-4be9-ac62-d340161507b3';
  }


  render () {
    const { messages } = this.props;

    return (
      messages.map((message, index) => (
        this.isMe(message) ?
        
         <Segment compact inverted
           floated='right'
           color='blue'
           className='clear next-chat-message-right'
           size='small'
           key={index}>
           <div>{message.body}</div>
         </Segment> :      
         <Segment compact raised
           floated='left'
           className='clear next-chat-message-left'
           size='small'
           key={index}>
           <div>{message.body}</div>
         </Segment>
      ))
    );
  }

}
