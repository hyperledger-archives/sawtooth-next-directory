import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme';
import { BrowserRouter } from 'react-router-dom';


import SignupForm from './SignupForm';


describe('SignupForm component', () => {
  const props = {
    submit: (username, password) => { }
  }
  const wrapper = shallow(<SignupForm {...props} />);


  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(
      <BrowserRouter><SignupForm {...props} /></BrowserRouter>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });


  test('username form', () => {
    wrapper.find('#next-signup-form-1').simulate('submit');
    wrapper.find('#next-name-signupInput').simulate('change', { event: {} }, { name: 'name', value: '' });
    wrapper.find('#next-email-signupInput').simulate('change', { event: {} }, { name: 'email', value: '' });
    wrapper.find('#next-username-signupInput').simulate('change', { event: {} }, { name: 'username', value: '' });
    wrapper.find('#next-password-signupInput').simulate('change', { event: {} }, { name: 'password', value: '' });
  });

  test('password form', () => {
    wrapper.find('#next-password-signupForm').simulate('submit');
  });

  test('form back button click event', () => {
    wrapper.find('#next-signup-form-back-button').simulate('click');
  });
});
