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

import LoginForm from './LoginForm';


describe('LoginForm component', () => {

  const props = {
    submit: (username, password) => { },
  };
  const wrapper = shallow(<LoginForm {...props} />);

  it('renders without crashing', () => {
    const div = document.createElement('div');

    ReactDOM.render(
      <BrowserRouter><LoginForm {...props} /></BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });

  test('username form', () => {
    wrapper.find('#next-username-form').simulate('submit');
    wrapper.find('#next-username-input').simulate('change',
      { event: {} }, { name: 'username', value: '' });
    wrapper.find('#next-username-input').simulate('change',
      { event: {} }, { name: 'password', value: '' });
    wrapper.find('#next-username-input').simulate('change',
      { event: {} }, { name: 'resetEmail', value: '' });
  });

  test('password form', () => {
    wrapper.find('#next-password-form').simulate('submit');
  });

  test('form back button click event', () => {
    wrapper.find('#next-login-form-back-button').simulate('click');
  });

  test('reset password form', () => {
    wrapper.find('#next-login-form-reset-password').simulate('submit');
  });


  test('form email back button', () => {
    wrapper.find('#next-login-reset-email-back-button').simulate('click');
  });

  test('forgot password button click', () => {
    wrapper.find('#next-login-form-forgot-password').simulate('click');
  });

});
