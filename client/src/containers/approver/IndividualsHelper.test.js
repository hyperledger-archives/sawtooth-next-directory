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

import { syncAll, syncFromCategory, syncFromItem,
  syncUsers } from './IndividualsHelper';

describe('Individuals helper test', () => {
  it('should call syncAll function', function () {
    const checked = true, roleId = 'roleID',
      proposalId = 'proposalID', userId = 'userID';
    let self = this;
    self.props = { openProposalsByRole: { 'roleID': [] } };
    self.state = { selectedProposals: '', selectedRoles: '' };

    const generator = syncAll.call(
      self,
      checked,
      roleId,
      proposalId,
      userId,
    );

    expect(generator.next().value).toEqual({ 'proposals': '',
      'roles': ['roleID'] });
  });

  it('should call syncFromCategory function', function () {
    const checked = true, roleId = 'roleID',
      proposalId = 'proposalID', userId = 'userID';
    let self = this;
    self.props = { openProposalsByRole: { 'roleID': [{ id: 'userID' }] } };
    self.state = { selectedProposals: '', selectedRoles: '' };

    const generator = syncFromCategory.call(
      self,
      checked,
      roleId,
      proposalId,
      userId,
    );

    expect(generator.next().value).toEqual({ 'changedUsers': [undefined],
      'proposals': ['userID'], 'roles': ['roleID'] });
  });

  it('should call syncFromItem function', function () {
    const checked = true, proposalId = 'proposalID', userId = 'userID';
    let self = this;
    self.props = { openProposalsByUser: { 'userID': [{ id: '' }] },
      openProposalFromId: () => { } };
    self.state = { selectedProposals: '', selectedRoles: '' };

    const generator = syncFromItem.call(
      self,
      checked,
      null,
      userId,
    );

    expect(generator.next().value).toEqual({ changedUsers: ['userID'],
      'proposals': '', 'roles': [undefined] });
  });

  it('should call syncUsers function', function () {
    const checked = true, proposalId = 'proposalID', userId = 'userID';
    let self = this;
    self.props = { openProposalsByUser: { 'userID': [{ id: '' }] },
      openProposalFromId: () => { } };
    self.state = { selectedUsers: '' };

    const generator = syncUsers.call(
      self,
      checked,
      ['userID'],
      proposalId,
    );

    expect(generator.next().value).toEqual({ users: ['userID'] });
  });

});
