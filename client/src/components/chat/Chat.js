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


import ChatForm from '../forms/ChatForm';
import ChatMessage from './ChatMessage';
import './Chat.css';


/**
 * 
 * @class Chat
 * Component encapsulating the chat widget
 * 
 */
export default class Chat extends Component {

  /**
   * 
   * Switch chat context when active pack changes 
   * 
   */
  componentWillReceiveProps (newProps) {
    const { activePack, getConversation } = this.props;

    if (newProps.activePack !== activePack) {

      // TODO: Normalize all JSON objects behind a schema
      getConversation(newProps.activePack['conversation_id']);
    }
  }


  send (message) {
    const { sendMessage } = this.props;

    // TODO: Retrieve user from session
    const payload = {
      body: message,
      from: { id: '519909ec-f0c8-4be9-ac62-d340161507b3', name: 'John Doe' }
    };
  
    sendMessage(payload);
  }


  render () {
    const { messages } = this.props;

    return (
      <div id='next-chat-container'>
        <div>
          { messages &&
            <ChatMessage {...this.props}/>
          }

          { messages && messages.length === 0 &&
            <Segment inverted color='violet'>
              <p>Approv is here to help you get access to groups,
              approvals and everything in between.</p>
              <p>I will recommended groups you should be a part of.
              Tips ... faster approvals from managers!</p>
            </Segment>
          }
        </div>


        <div id='next-chat-conversation-dock'>
          <ChatForm submit={(message) => this.send(message)}/>
        </div>
      </div>
    );
  }

}
