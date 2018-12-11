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
import { BrowserRouter } from 'react-router-dom';
import { shallow } from 'enzyme';


import RoleList from './RoleList';


describe('RoleList component', () => {

  it('renders without crashing', () => {
    const div = document.createElement('div');

    const props = {
      getUsers: (collection) => { },
      openProposalsByUser: { proposal1: '', proposal2: '' },
      users: [{ id: 'proposal1' }],
      openProposalsByRole: { roleProposal1: [{ id: 'roleid' }] },
      handleChange: () => { },
      selectedProposals: ['roleid'],
      selectedRoles: ['roleid'],
      roleFromId: () => {  },
    };

    ReactDOM.render(
      <BrowserRouter><RoleList {...props} /></BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
    const wrapper = shallow(
      <RoleList {...props} />);
    wrapper.instance().componentDidUpdate(props);
  });

});
