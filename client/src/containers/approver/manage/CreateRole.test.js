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
import { BrowserRouter } from 'react-router-dom';
import { shallow } from 'enzyme';


import * as customStore from 'customStore';
import CreateRole from './CreateRole';


const store = customStore.create();
describe('CreateRole component', () => {
  const props = {
    submit: (username, password) => { },
    createRole: {
      name: 'name',
      owners: 'id1',
      administrators: 'id2',
    },
    createRole: () => {},
    id: 'abc',
  };
  const wrapper = shallow(<CreateRole {...props}/>);

  it('renders without crashing', () => {
    const div = document.createElement('div');

    ReactDOM.render(
      <Provider store={store}>
        <BrowserRouter>
          <CreateRole/>
        </BrowserRouter>
      </Provider>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });
  wrapper.find('#next-approver-manage-create-role-form').simulate('change',
    { event: {} }, { name: 'name', value: '' });
  wrapper.instance().createRole(props);
});
