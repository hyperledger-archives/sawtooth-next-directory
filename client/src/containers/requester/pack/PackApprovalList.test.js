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

import PackApprovalList from './PackApprovalList';


describe('PackApprovalList component', () => {
  const props = {
    proposals: [{appprovers: []}],
    getUser: () => {},
    users: [{ id: 'proposal2'}],
    userFromId: (userId) => {
      return { email: ''};
    },
  };
  const wrapper = shallow(<PackApprovalList {...props}/>);

  it('renders without crashing', () => {
    const div = document.createElement('div');

    ReactDOM.render(
      <BrowserRouter>
        <PackApprovalList/>
      </BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });
  wrapper.instance().componentDidUpdate(props);
  wrapper.instance().renderUserInfo(props);
});
