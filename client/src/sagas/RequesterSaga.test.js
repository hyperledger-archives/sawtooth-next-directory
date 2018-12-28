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


import { put } from 'redux-saga/effects';


import FixtureAPI from 'services/FixtureApi';
import RequesterActions from 'redux/RequesterRedux';
import { getBase,
  fetchPack,
  fetchRole,
  fetchProposal,
  getAllRoles,
  roleAccess,
  packAccess } from 'sagas/RequesterSaga';


const stepper = (fn) => (mock) => fn.next(mock).value;


test('getBase: success path', () => {
  const res = { ok: true, data: {} };

  const step = stepper(getBase(FixtureAPI));

  step();
  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(RequesterActions.baseSuccess(res)));
});


test('fetchRole: success Path', () => {
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const res = { ok: true, data: {data: ''}};

  const step = stepper(fetchRole(FixtureAPI, id));
  step();
  const stepRes = step(res);

  expect(stepRes).toEqual(put(RequesterActions.roleSuccess(res.data.data)));
});


test('fetchRole: failure path', () => {
  const res = { ok: false, data: {} };
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const step = stepper(fetchRole(FixtureAPI, id));

  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(RequesterActions.roleFailure(res.data.error)));
});


test('fetchPack: success Path', () => {
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const res = { ok: true, data: {data: ''}};

  const step = stepper(fetchPack(FixtureAPI, id));
  step();
  const stepRes = step(res);

  expect(stepRes).toEqual(put(RequesterActions.packSuccess(res.data.data)));
});


test('fetchPack: failure path', () => {
  const res = { ok: false, data: {} };
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const step = stepper(fetchPack(FixtureAPI, id));

  step();
  const stepRes = step(res);
  expect(stepRes).toEqual(put(RequesterActions.packFailure(res.data.error)));
});


test('getAllRoles: success Path', () => {

  const res = { ok: true, data: {data: ''}};

  const step = stepper(getAllRoles(FixtureAPI));
  step();
  step();
  const stepRes = step(res);

  expect(stepRes).toEqual(put(RequesterActions.allRolesSuccess(res.data.data)));
});


test('getAllRoles: failure Path', () => {

  const res = { ok: false, data: {error: '', data: ''}};

  const step = stepper(getAllRoles(FixtureAPI));
  step();
  step();
  const stepRes = step(res);

  expect(stepRes)
    .toEqual(put(RequesterActions.allRolesFailure(res.data.error)));
});


test('roleAccess: success Path', () => {

  const res = { ok: true, data: {data: ''}};

  const step = stepper(roleAccess(FixtureAPI, {
    id: '',
    userId: '',
    reason: '',
  }));
  step();

  const stepRes = step(res);

  expect(stepRes)
    .toEqual(put(RequesterActions.roleAccessSuccess(res.data.data)));
});


test('roleAccess: failure Path', () => {

  const res = { ok: false, data: {data: ''}};

  const step = stepper(roleAccess(FixtureAPI, {
    id: '',
    userId: '',
    reason: '',
  }));
  step();

  const stepRes = step(res);

  expect(stepRes)
    .toEqual(put(RequesterActions.roleAccessFailure(res.data.data)));
});

test('packAccess: success Path', () => {

  const res = { ok: true, data: {data: ''}};

  const step = stepper(packAccess(FixtureAPI, {
    id: '',
    userId: '',
    reason: '',
  }));
  step();

  const stepRes = step(res);

  expect(stepRes)
    .toEqual(put(RequesterActions.packAccessSuccess(res.data.data)));
});


test('packAccess: failure Path', () => {

  const res = { ok: false, data: {data: ''}};

  const step = stepper(packAccess(FixtureAPI, {
    id: '',
    userId: '',
    reason: '',
  }));
  step();

  const stepRes = step(res);

  expect(stepRes)
    .toEqual(put(RequesterActions.packAccessFailure(res.data.data)));
});

test('fetchProposal: success Path', () => {
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const res = { ok: true, data: {data: ''}};

  const step = stepper(fetchProposal(FixtureAPI, id));
  step();
  const stepRes = step(res);

  expect(stepRes)
    .toEqual(put(RequesterActions.proposalSuccess(res.data.data)));
});


test('fetchProposal: failure path', () => {
  const res = { ok: false, data: {} };
  const id = 'e15a71ee-58d2-49e8-a8e4-21888144be1f';

  const step = stepper(fetchProposal(FixtureAPI, id));

  step();
  const stepRes = step(res);
  expect(stepRes)
    .toEqual(put(RequesterActions.proposalFailure(res.data.error)));
});
