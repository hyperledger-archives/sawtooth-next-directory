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


import FixtureAPI from './FixtureApi';


describe('FixtureApi Service', () => {

  test('get requester base', () => {
    FixtureAPI.getRequesterBase();
  });

  test('get role by id', () => {
    FixtureAPI.getRole('default');
    FixtureAPI.getRole('e15a71ee-58d2-49e8-a8e4-21888144be1f');
    FixtureAPI.getRole('539d9dd3-6b4d-4136-ab67-b6ff6b307c9f');
    FixtureAPI.getRole('d1ea7166-9c0f-428a-b684-9d73935e9211');
    FixtureAPI.getRole('3e542e8d-2e04-4125-b7f6-5b362dcc8a60');
    FixtureAPI.getRole('d7fc25f9-eb50-4b51-bb62-a8eb6e89f1f0');
  });

  test('get role by id', () => {
    FixtureAPI.getConversation('default');
    FixtureAPI.getConversation('490d7d4c-6e07-4795-b785-7a0146d4ec0f');
    FixtureAPI.getConversation('bf42a57b-6fe4-41ce-9f2a-f6f7dab54e8b');
  });

  test('send message', () => {
    FixtureAPI.sendMessage('new message found');
  });

  test('login', () => {
    FixtureAPI.login('username', 'password');
  });

  test('logout', () => {
    FixtureAPI.logout();
  });

  test('get roles', () => {
    FixtureAPI.getRoles();
  });

  test('get pack', () => {
    const id= ['e15a71ee-58d2-49e8-a8e4-21888144be1f',
      '539d9dd3-6b4d-4136-ab67-b6ff6b307c9f',
      'd1ea7166-9c0f-428a-b684-9d73935e9211',
      '3e542e8d-2e04-4125-b7f6-5b362dcc8a60',
      'd7fc25f9-eb50-4b51-bb62-a8eb6e89f1f0',
      '',
    ];
    id.map((i) => FixtureAPI.getPack(i));

  });

});
