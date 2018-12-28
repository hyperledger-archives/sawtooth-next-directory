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


import StackedAvatar from './StackedAvatar';


describe('StackedAvatar component', () => {

  it('Renders more than 3 components', () => {
    const div = document.createElement('div');
    const list = ['one', 'two', 'three', 'four', 'five'];

    const props = {
      users: [],
    };

    ReactDOM.render(
      <StackedAvatar list={list} {...props}/>, div
    );
    ReactDOM.render(
      <StackedAvatar list={[]} {...props}/>, div
    );

    ReactDOM.unmountComponentAtNode(div);
  });

});
