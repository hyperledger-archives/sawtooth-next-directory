
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
import Delegated from './Delegated';


const store = customStore.create();
const props = {
  getOpenProposals: () => { },
  userFromId: () => { },
  openProposals: [''],
};

const newprops = {
  getOpenProposals: () => { },
  userFromId: () => { },
  openProposals: [],
};
const wrapper = shallow(<Delegated {...props} store={store} />);


it('renders without crashing', () => {
  const div = document.createElement('div');

  ReactDOM.render(
    <Provider store={store}>
      <BrowserRouter><Delegated {...props} /></BrowserRouter>
    </Provider>, div
  );

  ReactDOM.render(
    <Provider store={store}>
      <BrowserRouter><Delegated {...newprops} /></BrowserRouter>
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
