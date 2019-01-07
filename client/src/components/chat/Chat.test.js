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


import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme';
import { BrowserRouter } from 'react-router-dom';


import * as customStore from 'customStore';
import Chat from './Chat';


const store = customStore.create();


describe('Chat component', () => {

  it('renders without crashing', () => {
    const div = document.createElement('div');
    const props = {
      submit: (username, password) => { },
      title: 'defaultTitle',
      type: '1',
      selectedUsers: ['userID'],
      groupBy: 0,
      userFromId: (userId) => {  },
    };

    ReactDOM.render(
      <BrowserRouter>
        <Chat store={store} {...props}/>
      </BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });


  it('renders without crashing with different props', () => {
    const div = document.createElement('div');
    const props = {
      isSocketOpen: () => {},
      submit: (username, password) => { },
      title: 'defaultTitle',
      type: '1',
      selectedUsers: [{ user: 'roleid' }],
      selectedRoles: [{ role: 'roleid' }],
      groupBy: 1,
      userFromId: (userId) => {
        return { name: '' };
      },
    };
    const newProps = {
      isSocketOpen: () => {},
      type: '1',
      groupBy: 1,
      selectedRoles: [{ id: 'roleid' }],
      roleFromId: (roleId) => {
        return { name: '' };
      },
    };

    ReactDOM.render(
      <BrowserRouter>
        <Chat store={store} {...props}/>
      </BrowserRouter>, div
    );

    ReactDOM.render(
      <BrowserRouter>
        <Chat store={store} title='defaultTitle' type={'0'} {...props}/>
      </BrowserRouter>, div
    );

    ReactDOM.render(
      <BrowserRouter>
        <Chat {...newProps} store={store}/>
      </BrowserRouter>, div
    );

    ReactDOM.render(
      <BrowserRouter>
        <Chat type={'0'} {...props} store={store}/>
      </BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });


  test('expect send function to be called', () => {
    const props = {
      sendMessage: () => { },
      type: '0',
      activeRole: { id: 'abc' },
      activePack: { id: 'abc' },
      me: { id: 'asdf' },
      requestAccess: () => { },
      roleFromId: (roleId) => {
        return { name: '' };
      },
      userFromId: (userId) => {
        return { name: '' };
      },
      requestRoleAccess: () => {},
      requestPackAccess: () => {},
      approveProposals: () => { },
      selectedProposals: () => {},
      reset: () => { },
      rejectProposals: () => {},
      selectedUsers: [{ user: 'roleid' }],
      selectedRoles: [{ role: 'roleid' }],
    };

    const newProps = {
      sendMessage: () => { },
      type: '1',
      activeRole: { id: 'abc' },
      me: { id: 'asdf' },
      approveProposals: () => { },
      selectedProposals: () => {},
      reset: () => { },
      rejectProposals: () => {},
    };

    const wrapper = shallow(<Chat {...props}  store={store}/>);
    const newWrapper = shallow(<Chat {...newProps} store={store}/>);

    wrapper.dive().instance().send(props, { type: 0 });
    wrapper.dive().instance().send(props, { type: 1 });
    wrapper.dive().instance().send(props, { type: null });
    newWrapper.dive().instance().send(newProps, { type: 0 });
    wrapper.dive().instance().manualRequestRole(props);
    wrapper.dive().instance().manualRequestPack(props);
    wrapper.dive().instance().manualApprove(props);
    wrapper.dive().instance().manualReject(props);
  });

});
