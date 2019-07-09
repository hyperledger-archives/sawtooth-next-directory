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
import { Header } from 'semantic-ui-react';


import './RequesterChat.css';
import ChatTranscript from './ChatTranscript';
import * as utils from 'services/Utils';


/**
 *
 * @class         RequesterChat
 * @description   Component encapsulating the requester chat view
 *
 */
class RequesterChat extends Component {

  /**
   * Entry point to perform tasks required to render component
   */
  componentDidMount () {
    this.init();
  }


  /**
   * Called whenever Redux state changes
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const {
      activePack,
      activeRole,
      isSocketOpen,
      recommendedPacks,
      recommendedRoles } = this.props;

    if (prevProps.isSocketOpen('chatbot') !== isSocketOpen('chatbot'))
      this.init();

    if (!utils.arraysEqual(prevProps.recommendedRoles, recommendedRoles))
      this.init();

    if ((activeRole && recommendedRoles &&
          prevProps.activeRole.id !== activeRole.id) ||
        (activePack && recommendedPacks &&
          prevProps.activePack.id !== activePack.id))
      this.init();
  }


  /**
   * Send intent message to chatbot for a given role or pack.
   * Update the chatbot tracker with the current context when
   * the current role or pack changes.
   */
  init () {
    const {
      activePack,
      activeRole,
      expired,
      id,
      isSocketOpen,
      me,
      messagesCountById,
      memberOf,
      ownerOf,
      recommendedPacks,
      recommendedRoles,
      sendMessage } = this.props;

    const resource = activePack || activeRole;
    if (!resource) return;

    if ((recommendedPacks || recommendedRoles) && isSocketOpen('chatbot')) {
      const payload = {
        resource_id: resource.id,
        next_id: id,
      };
      const slots = {
        resource_name: resource.name,
        resource_type: activePack ? 'PACK' : 'ROLE',
      };
      const update = messagesCountById(resource.id) > 0 && 'update';

      if (activeRole) payload.approver_id = activeRole.owners[0];
      if (expired && expired.includes(resource.id)) {

        // Construct intent message given role membership
        // is expired
        payload.text = `/${update || 'expired'}${JSON.stringify(
          {...slots, member_status: 'NOT_MEMBER'})}`;

      } else if (memberOf && memberOf.find(
        item => item.id === resource.id)
      ) {

        // Construct intent message given user is a member
        // of the current pack or role
        payload.text = `/${update || 'member'}${JSON.stringify(
          {...slots, member_status: 'MEMBER'})}`;

      } else if (ownerOf.includes(resource.id)) {

        // Construct intent message given user is an owner
        // of the current pack or role

        if (memberOf && memberOf.find(
          item => item.id === resource.id)
        ) {
          payload.text = `/${update || 'owner'}${JSON.stringify(
            {...slots, owner_status: 'OWNER'})}`;
        } else {
          payload.text = `/${update || 'owner'}${JSON.stringify(
            {...slots, owner_status: 'OWNER', member_status: 'NOT_MEMBER'})}`;
        }

      } else if (me && me.proposals.find(
        proposal => proposal.object_id === resource.id &&
          proposal.status === 'OPEN')
      ) {

        // Construct intent message given user has previously
        // requested access to the current pack or role
        payload.text = `/${update || 'pending'}${JSON.stringify(
          {...slots, member_status: 'PENDING'})}`;

      } else if ([
        ...(recommendedPacks || []),
        ...(recommendedRoles || [])]
        .map(item => item.id || item).includes(resource.id)
      ) {

        // Construct intent message given user is not a member
        // of the current recommended role or pack
        payload.text = `/${update || 'recommend'}${JSON.stringify(
          {...slots, member_status: 'NOT_MEMBER'})}`;

      } else if (resource.owners && resource.owners.length === 0) {

        // Construct intent message given role has no owner(s)
        if (update) return;
        payload.text = '/no_owner';

      } else {

        // Construct intent message given user is not a member
        // of the current role or pack
        slots.member_status = 'NOT_MEMBER';
        payload.text = `/${update || 'offer'}${JSON.stringify(
          {...slots, member_status: 'NOT_MEMBER'})}`;

      }
      sendMessage(payload);
    }
  }


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
            {/* <Icon link name='pin' size='mini' className='pull-right'/> */}
          </Header>
        }
        <div id='next-requester-chat-transcript-container'>
          <ChatTranscript {...this.props}/>
        </div>
      </div>
    );
  }

}


export default RequesterChat;
