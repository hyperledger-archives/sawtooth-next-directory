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


import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { shallow } from 'enzyme';
import { BrowserRouter } from 'react-router-dom';


import * as customStore from 'customStore';
import Header from './Header';


const store = customStore.create();


describe('Header component', () => {

  it('renders without crashing', () => {
    const div = document.createElement('div');
    const props = {
      id: '1234',
      isSocketOpen: () => {},
      me: { name: 'username' },
      openProposalsCount: 5,
      renderMenu: () => {  },
      logout: () => { },
      users: [],
    };
    ReactDOM.render(
      <Provider store={store}>
        <BrowserRouter>
          <Header {...props}/>
        </BrowserRouter>
      </Provider>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });

  it('calls logout function', () => {
    const props = {
      isSocketOpen: () => {},
      me: { name: 'username' },
      openProposalsCount: 5,
      renderMenu: () => {  },
      logout: () => { },
    };

    const wrapper = shallow(
      <Header.WrappedComponent {...props} store={store}/>
    );

    wrapper.instance().logout();
  });

});
