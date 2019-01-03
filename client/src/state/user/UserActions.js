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
  meRequest:       null,
  meSuccess:       ['me'],
  meFailure:       ['error'],

  usersRequest:    ['ids'],
  userRequest:     ['id'],
  userSuccess:     ['user'],
  userFailure:     ['error'],

  allUsersRequest: ['start', 'limit'],
  allUsersSuccess: ['users', 'usersTotalCount'],
  allUsersFailure: ['error'],

  resetAll:        null,
});


export const UserTypes = Types;
export default Creators;


export const INITIAL_STATE = Immutable({
  fetchingMe:       null,
  fetchingUser:     null,
  fetchingUsers:    null,
  fetchingAllUsers: null,

  error:            null,
  me:               null,
  users:            null,
});
