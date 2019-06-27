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


import { createActions } from 'reduxsauce';
import Immutable from 'seamless-immutable';


const { Types, Creators } = createActions({
  createRoleRequest:          ['payload'],
  createRoleSuccess:          ['role'],
  createRoleFailure:          ['error'],

  createPackRequest:          ['payload'],
  createPackSuccess:          ['pack'],
  createPackFailure:          ['error'],

  deletePackRequest:          ['id'],
  deletePackSuccess:          ['pack'],
  deletePackFailure:          ['error'],

  delegationsRequest:         ['id'],
  delegationsSuccess:         ['delegations'],
  delegationsFailure:         ['error'],

  approveProposalsRequest:    ['ids'],
  approveProposalsSuccess:    ['closedProposals'],
  approveProposalsFailure:    ['error'],
  rejectProposalsRequest:     ['ids'],
  rejectProposalsSuccess:     ['closedProposals'],
  rejectProposalsFailure:     ['error'],

  openProposalsRequest:       ['id'],
  openProposalsSuccess:       ['openProposals'],
  openProposalsFailure:       ['error'],
  confirmedProposalsRequest:  ['id'],
  confirmedProposalsSuccess:  ['confirmedProposals'],
  confirmedProposalsFailure:  ['error'],
  rejectedProposalsRequest:   ['id'],
  rejectedProposalsSuccess:   ['rejectedProposals'],
  rejectedProposalsFailure:   ['error'],

  organizationRequest:        ['id', 'isMe'],
  organizationSuccess:        ['organization', 'isMe'],
  organizationFailure:        ['error'],

  roleExistsRequest:          ['name'],
  roleExistsSuccess:          ['exists'],
  roleExistsFailure:          null,
  resetRoleExists:            null,

  packExistsRequest:          ['name'],
  packExistsSuccess:          ['exists'],
  packExistsFailure:          null,
  resetPackExists:            null,

  resetAll:                   null,
  onBehalfOfSet:              ['id'],
  feedReceive:                ['payload'],
});


export const ApproverTypes = Types;
export default Creators;


export const INITIAL_STATE = Immutable({
  confirmedProposals:         null,
  createdPacks:               null,
  createdRoles:               null,
  delegations:                null,
  deletingPack:               null,
  directReports:              null,
  error:                      null,
  fetching:                   null,
  fetchingOrganization:       null,
  openProposals:              null,
  organization:               null,
  onBehalfOf:                 null,
  packExists:                 null,
  rejectedProposals:          null,
  roleExists:                 null,
});
