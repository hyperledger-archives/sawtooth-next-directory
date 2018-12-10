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


import Create from './Create';
import Chat from '../../chat/Chat';


describe('Create component', () => {

    it('renders without crashing', () => {
        const div = document.createElement('div');

        ReactDOM.render(
            <BrowserRouter><Create /></BrowserRouter>, div
        );

        ReactDOM.unmountComponentAtNode(div);
    });

});

describe('<Create/>', () => {

    describe('handleChange', () => {

        const props = {
            submit: () => { }
        };
        const wrapper = shallow(<Create {...props} />);

        test('calls setState validFields false when no email/password', () => {
            const argsEmail = [{ target: { name: 'username', value: '' } }, { target: { name: 'password', value: '' } }]
            argsEmail.forEach(element => {
                wrapper.instance().handleChange(element);
            });
            expect(wrapper.state().validFields).toEqual(false)
        })

        test('calls setState validFields true when email/password are ok', () => {
            const argsEmail = [{ target: { name: 'username', value: 'abcd@gmail.com' } }, { target: { name: 'password', value: 'password' } }]
            argsEmail.forEach(element => {
                wrapper.instance().handleChange(element);
            });
            expect(wrapper.state().validFields).toEqual(true)
        });

        it('calls handle open', () => {
            wrapper.instance().handleOpen();
        });

        it('calls handle close on close modal button click', () => {
            wrapper.find('#next-modal-close-button').simulate('click');
        });

        it('calls handle submit on submit modal button click', () => {
            wrapper.find('#next-modal-submit-button').simulate('click');
        });

    });

});
