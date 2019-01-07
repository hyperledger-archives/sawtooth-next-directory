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
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { shallow } from 'enzyme';


import * as customStore from 'customStore';
import Approved from './Approved';


const store = customStore.create();


describe('Approved component', () => {
  const props = {
    getConfirmedProposals: () => {},
    roleFromId: () => {},
    userFromId: () => {},
    getRoles: () => {},
    getUsers: () => {},
    selectedProposal: [{object: ''}],
    confirmedProposals: [{ id: 'proposal-123', opener: 'opener-123' }],
    roles: [{ id: 'role' }],
    userFromId: (userId) => {
      return { email: '' };
    },
    users: [],
  };
  const newProps = {
    getConfirmedProposals: () => {},
    roleFromId: () => {},
    userFromId: () => {},
    getRoles: () => {},
    getUsers: () => {},
    selectedProposal: [{id: 'qwerty'}],
    confirmedProposals: [{ id: 'proposal-123', opener: 'opener-123' }],
    userFromId: (userId) => {
      return { email: '' };
    },
  };
  const wrapper = shallow(<Approved {...props} store={store}/>);


  it('renders without crashing', () => {
    const div = document.createElement('div');

    ReactDOM.render(
      <BrowserRouter>
        <Approved {...props} store={store}/>
      </BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });
  wrapper.dive().instance().componentDidUpdate(props);
  wrapper.dive().instance().componentDidUpdate(newProps);
  wrapper.dive().instance().userEmail(props);
  wrapper.dive().instance().handleSort();
  wrapper.dive().instance().setSelectedProposal(props);
});
