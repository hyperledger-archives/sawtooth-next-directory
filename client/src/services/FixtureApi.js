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


import base from '../mock_data/base.json';
import roles from '../mock_data/all_roles.json';
import packs from '../mock_data/packs.json';


import cloudOnboardingPack from '../mock_data/pack_cloud_onboarding.json';
import rebellionAccessPack from '../mock_data/pack_rebellion_access.json';
import rebellionSecurityPack from '../mock_data/pack_rebellion_security.json';
import jazzPack from '../mock_data/pack_jazz_security_permissions.json';
import jazzRevPack from '../mock_data/pack_jazz_rev.json';


import onboardingConversation from '../mock_data/conversation_onboarding.json';
import approvalConversation from '../mock_data/conversation_approval.json';


export default {

  getRequesterBase: () => {
    return {
      ok: true,
      data: base,
    };
  },

  getPack: (id) => {
    let data;

    switch (id) {
      case 'e15a71ee-58d2-49e8-a8e4-21888144be1f':
        data = cloudOnboardingPack;
        break;

      case '539d9dd3-6b4d-4136-ab67-b6ff6b307c9f':
        data = rebellionAccessPack;
        break;

      case 'd1ea7166-9c0f-428a-b684-9d73935e9211':
        data = rebellionSecurityPack;
        break;

      case '3e542e8d-2e04-4125-b7f6-5b362dcc8a60':
        data = jazzPack;
        break;

      case 'd7fc25f9-eb50-4b51-bb62-a8eb6e89f1f0':
        data = jazzRevPack;
        break;

      default:
        data = {};
        break;
    }

    return {
      ok: true,
      data: data,
    };
  },

  getConversation: (id) => {
    let data;

    switch (id) {
      case '490d7d4c-6e07-4795-b785-7a0146d4ec0f':
        data = onboardingConversation;
        break;

      case 'bf42a57b-6fe4-41ce-9f2a-f6f7dab54e8b':
        data = approvalConversation;
        break;

      default:
        data = { messages: [] };
        break;
    }

    return {
      ok: true,
      data: data,
    };
  },

  sendMessage: (message) => {
    return {
      ok: true,
      data: message,
    };
  },

  login: (username, password) => {
    return {
      ok: true,
      data: {},
    };
  },

  signup: (username, password, name, email) => {
    return {
      ok: true,
      data: {},
    };
  },



  logout: () => {
    return {
      ok: true,
      data: {},
    };
  },

  getRoles: () => {
    return {
      ok: true,
      data: roles,
    };
  },
  me: () => {
    return {
      ok: true,
      data: {},
    };
  },

  getUser: (id) => {
    return {
      ok: true,
      data: {},
    };
  },

  getRole: (id) => {
    return {
      ok: true,
      data: {},
    };
  },
  getPacks: () => {
    return {
      ok: true,
      data: packs,
    };
  },
};
