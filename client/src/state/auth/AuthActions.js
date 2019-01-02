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


import { createActions } from 'reduxsauce';
import Immutable from 'seamless-immutable';


const { Types, Creators } = createActions({
  loginRequest:     ['username', 'password'],
  loginSuccess:     ['isAuthenticated', 'payload'],
  loginFailure:     ['error'],

  signupRequest:    ['name', 'username', 'password', 'email'],
  signupSuccess:    ['isAuthenticated', 'payload'],
  signupFailure:    ['error'],

  logoutRequest:    null,
  logoutSuccess:    null,
  logoutFailure:    ['error'],
});


export const AuthTypes = Types;
export default Creators;


export const INITIAL_STATE = Immutable({
  isAuthenticated:  null,
  fetching:         null,
  error:            null,
  user:             null,
});
