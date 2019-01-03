
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
import PeopleApproval from './PeopleApproval';


const store = customStore.create();
const props = {
  getOpenProposals: () => { },
  userFromId: () => { },
  getUser: () => {},
  openProposals: [''],
  match: { params: {} },
};

const newprops = {
  getOpenProposals: () => { },
  userFromId: () => { },
  getUser: () => {},
  openProposals: [],
  match: { params: {} },
};
const wrapper = shallow(<PeopleApproval {...props} store={store}/>);


it('renders without crashing', () => {
  const div = document.createElement('div');

  ReactDOM.render(
    <Provider store={store}>
      <BrowserRouter>
        <PeopleApproval {...props}/>
      </BrowserRouter>
    </Provider>, div
  );

  ReactDOM.render(
    <Provider store={store}>
      <BrowserRouter>
        <PeopleApproval {...newprops}/>
      </BrowserRouter>
    </Provider>, div
  );

  ReactDOM.unmountComponentAtNode(div);
});

it('calls reset function', () => {
  wrapper.dive().instance().reset();
});

it('calls setFlow function', () => {
  wrapper.dive().instance().setFlow();
});
