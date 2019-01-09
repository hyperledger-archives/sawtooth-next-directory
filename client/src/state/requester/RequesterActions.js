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
  allPacksRequest:      ['start', 'limit'],
  allPacksSuccess:      ['packs', 'packsTotalCount'],
  allPacksFailure:      ['error'],
  allRolesRequest:      ['start', 'limit'],
  allRolesSuccess:      ['roles', 'rolesTotalCount'],
  allRolesFailure:      ['error'],

  packRequest:          ['id'],
  packsRequest:         ['ids'],
  packSuccess:          ['pack'],
  packFailure:          ['error'],
  roleRequest:          ['id'],
  rolesRequest:         ['ids'],
  roleSuccess:          ['role'],
  roleFailure:          ['error'],

  baseRequest:          null,
  baseSuccess:          ['base'],
  baseFailure:          ['error'],

  proposalRequest:      ['id'],
  proposalSuccess:      ['proposal'],
  proposalFailure:      ['error'],
  proposalsRequest:     ['ids'],

  packAccessRequest:    ['id', 'userId', 'reason'],
  packAccessSuccess:    null,
  packAccessFailure:    null,
  roleAccessRequest:    ['id', 'userId', 'reason'],
  roleAccessSuccess:    null,
  roleAccessFailure:    null,

  resetAll:             null,
});


export const RequesterTypes = Types;
export default Creators;


export const INITIAL_STATE = Immutable({
  activeProposal:       null,
  activeRole:           null,
  error:                null,
  fetching:             null,
  fetchingAllRoles:     null,
  fetchingAllPacks:     null,
  packs:                null,
  recommended:          null,
  requests:             null,
  roles:                null,
  rolesTotalCount:      null,
  packsTotalCount:      null,
});
