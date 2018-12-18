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


import ChatForm from './ChatForm';


describe('ChatForm component', () => {
  const props = {
    submit: (username, password) => { },
    send: () => {},
  };
  const wrapper = shallow(<ChatForm {...props} />);
  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(
      <BrowserRouter><ChatForm {...props} /></BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });

  test('chat submit form', () => {
    wrapper.find('#next-placeholder-chat').simulate('submit');
  });

  test('form  button click event', () => {
    wrapper.find('#next-name-chat-submit').simulate('click');
  });

});
