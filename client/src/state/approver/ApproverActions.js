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

  delegationsRequest:         ['id'],
  delegationsSuccess:         ['delegations'],
  delegationsFailure:         ['error'],

  approveProposalsRequest:    ['ids'],
  approveProposalsSuccess:    ['closedProposal'],
  approveProposalsFailure:    ['error'],
  rejectProposalsRequest:     ['ids'],
  rejectProposalsSuccess:     ['closedProposal'],
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

  organizationRequest:        ['id'],
  organizationSuccess:        ['organization'],
  organizationFailure:        ['error'],

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
  error:                      null,
  fetching:                   null,
  openProposals:              null,
  organization:               null,
  onBehalfOf:                 null,
  rejectedProposals:          null,
});
