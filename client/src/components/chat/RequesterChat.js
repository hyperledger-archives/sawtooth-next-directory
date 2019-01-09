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
import { Header, Icon } from 'semantic-ui-react';


import './RequesterChat.css';
import ChatMessage from './ChatMessage';


/**
 *
 * @class         RequesterChat
 * @description   Component encapsulating the requester chat view
 *
 */
export default class RequesterChat extends Component {

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { title } = this.props;
    return (
      <div>
        { title &&
          <Header id='next-chat-header' size='small' inverted>
            {title}
            <Icon link name='pin' size='mini' className='pull-right'/>
          </Header>
        }
        <div id='next-chat-messages-container'>
          <ChatMessage {...this.props}/>
        </div>
      </div>
    );
  }

}
