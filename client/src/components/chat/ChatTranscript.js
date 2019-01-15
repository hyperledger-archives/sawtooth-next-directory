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
import { Header, Loader, Image, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';

import './ChatTranscript.css';
import chatbotAvatar from 'images/chatbot-avatar.png';
import Avatar from 'components/layouts/Avatar';


/**
 *
 * @class         ChatTranscript
 * @description   Component encapsulating the chat messages
 *
 */
class ChatTranscript extends Component {

  static propTypes = {
    messages:                 PropTypes.array,
    socketError:              PropTypes.bool,
    socketMaxAttemptsReached: PropTypes.bool,
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
    const {
      activePack,
      activeRole,
      fetching,
      messages,
      messagesById,
      socketError,
      socketMaxAttemptsReached,
      type } = this.props;

    if (type === 'REQUESTER' && socketMaxAttemptsReached) {
      return (
        <div id='next-chat-message-error-container'>
          <Header
            as='h2'
            content='Nex is feeling shy...'
            subheader={`In the meantime, you can draft a message
                        and request access for a role or pack below.`}/>
        </div>
      );
    }

    if (!messages) {
      return (
        <Loader
          active={(!socketMaxAttemptsReached && socketError) || !messages}
          size='large'>
        </Loader>
      );
    }
    const resourceId = (activePack && activePack.id) ||
      (activeRole && activeRole.id);
    const transcript = type === 'REQUESTER' ?
      messagesById(resourceId) :
      messages;

    return (
      <div>
        { fetching &&
          <div className={`next-chat-message-left next-chat-message-loading
            next-chat-transcript-animation-loading`}>
            <Image src={chatbotAvatar} size='mini'/>
            <Segment compact
              floated='left'
              size='small'>
              <div id='next-chat-message-loading-indicator'>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </Segment>
          </div>
        }
        <div
          id='next-chat-messages'
          className={`${fetching ?
            'next-chat-transcript-animation-send' :
            'next-chat-transcript-animation-receive'}`}>
          { !socketError && transcript &&
              transcript.map((message, index) =>
                this.isMe(message) ?
                  message.text &&
                  <div className={`next-chat-message-right ${index === 0 ?
                    'next-chat-message-animation-send' : ''}`} key={index}>
                    <Segment compact inverted
                      floated='right'
                      color='purple'
                      size='small'>
                      <div>
                        {message.text}
                      </div>
                    </Segment>
                  </div> :
                  <div className={`next-chat-message-left ${index === 0 ?
                    'next-chat-message-animation-receive' : ''}`} key={index}>
                    <div>
                      { message.from ?
                        <Avatar
                          userId={message.from}
                          size='small'
                          {...this.props}/> :
                        <Image src={chatbotAvatar} size='mini'/>
                      }
                    </div>
                    <Segment compact
                      floated='left'
                      size='small'>
                      <div dangerouslySetInnerHTML={{__html: message.text}}>
                      </div>
                    </Segment>
                  </div>
              )
          }
        </div>
      </div>
    );
  }
}


export default ChatTranscript;
