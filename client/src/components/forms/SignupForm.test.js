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


import SignupForm from './SignupForm';


describe('SignupForm component', () => {

  const props = {
    submit: (username, password) => { },
  };
  const wrapper = shallow(<SignupForm {...props}/>);


  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(
      <BrowserRouter>
        <SignupForm {...props}/>
      </BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });


  test('username form', () => {
    wrapper.find('#next-signup-form-1').simulate('submit');
    wrapper.find('#next-name-signup-input').simulate('change',
      { event: {} }, { name: 'name', value: '' });
    wrapper.find('#next-email-signup-input').simulate('change',
      { event: {} }, { name: 'email', value: '' });
    wrapper.find('#next-username-signup-input').simulate('change',
      { event: {} }, { name: 'username', value: '' });
    wrapper.find('#next-password-signup-input').simulate('change',
      { event: {} }, { name: 'password', value: '' });
  });


  test('password form', () => {
    wrapper.find('#next-password-signup-form').simulate('submit');
  });


  test('form back button click event', () => {
    wrapper.find('#next-signup-form-back-button').simulate('click');
  });

});
