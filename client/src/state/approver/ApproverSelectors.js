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


import * as utils from 'services/Utils';


export const ApproverSelectors = {
  confirmedProposals:    (state) => state.approver.confirmedProposals,
  openProposals:         (state) => state.approver.openProposals,
  openProposalsByUser:   (state) =>
    utils.groupBy(state.approver.openProposals, 'opener'),
  openProposalsByRole:   (state) =>
    utils.groupBy(state.approver.openProposals, 'object'),
  openProposalsCount:    (state) => {
    return (
      state.user.me &&
      state.approver.openProposals &&
      state.approver.openProposals
        .filter(proposal => proposal.approvers.includes(state.user.me.id))
        .length
    ) || null;
  },
  openProposalFromId:    (state, id) =>
    state.approver.openProposals &&
    state.approver.openProposals.find(proposal => proposal.id === id),
  organization:          (state) => state.approver.organization,
  onBehalfOf:            (state) => state.approver.onBehalfOf,
  ownedPacks:            (state) => {
    if (!state.user.me) return null;
    return utils.merge(
      (state.approver.createdPacks || []).map(pack => pack.id),
      state.user.me.ownerOf.packs,
    );
  },
  ownedRoles:            (state) => {
    if (!state.user.me) return null;
    return utils.merge(
      (state.approver.createdRoles || []).map(role => role.id),
      state.user.me.ownerOf.roles,
    );
  },
};
