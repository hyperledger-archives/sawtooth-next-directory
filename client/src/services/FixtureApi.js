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


import conversation1 from 'mocks/conversation1.json';
import conversation2 from 'mocks/conversation2.json';
import organization from 'mocks/organization.json';
import pack1 from 'mocks/pack1.json';
import pack2 from 'mocks/pack2.json';
import pack3 from 'mocks/pack3.json';
import pack4 from 'mocks/pack4.json';
import pack5 from 'mocks/pack5.json';


export default {
  getConfirmedProposals: () => ({ ok: true, data: [] }),
  getOpenProposals: (id) => ({ ok: true, data: [] }),
  getProposal: () => ({ ok: true, data: [] }),
  getRecommended: () => ({ ok: true, data: [] }),
  getRejectedProposals: () => ({ ok: true, data: [] }),
  getRelationships: (id) => ({ ok: true, data: organization }),
  getRole: (id) => ({ ok: true, data: {} }),
  getUser: (id) => ({ ok: true, data: {} }),
  login: (username, password) => ({ ok: true, data: {} }),
  logout: () => ({ ok: true, data: {} }),
  me: () => ({ ok: true, data: {} }),
  requestPackAccess: () => ({ ok: true, data: [] }),
  requestRoleAccess: () => ({ ok: true, data: [] }),
  sendSocket: (message) => ({ ok: true, data: message }),
  signup: (username, password, name, email) => ({ ok: true, data: {} }),


  getPack: (id) => {
    let data;
    switch (id) {
      case 'e15a71ee-58d2-49e8-a8e4-21888144be1f':
        data = pack1;
        break;
      case '3e542e8d-2e04-4125-b7f6-5b362dcc8a60':
        data = pack2;
        break;
      case 'd7fc25f9-eb50-4b51-bb62-a8eb6e89f1f0':
        data = pack3;
        break;
      case '539d9dd3-6b4d-4136-ab67-b6ff6b307c9f':
        data = pack4;
        break;
      case 'd1ea7166-9c0f-428a-b684-9d73935e9211':
        data = pack5;
        break;
      default:
        data = {};
        break;
    }
    return { ok: true, data };
  },


  getConversation: (id) => {
    let data;
    switch (id) {
      case '490d7d4c-6e07-4795-b785-7a0146d4ec0f':
        data = conversation1;
        break;
      case 'bf42a57b-6fe4-41ce-9f2a-f6f7dab54e8b':
        data = conversation2;
        break;
      default:
        data = { messages: [] };
        break;
    }
    return { ok: true, data };
  },


  getPacks: () => ({
    ok: true,
    data: { data: [], paging: {} },
  }),


  getRoles: () => ({
    ok: true,
    data: { data: [], paging: {} },
  }),


  getUsers: (id) => ({
    ok: true,
    data: {
      data: [],
      paging: {},
    },
  }),
};
